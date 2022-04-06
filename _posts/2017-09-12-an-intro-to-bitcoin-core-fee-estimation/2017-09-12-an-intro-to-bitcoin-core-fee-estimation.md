---
layout: post
title: "An Introduction to Bitcoin Core Fee Estimation"
category: blog
excerpt: How Bitcoin Core estimates fee rates based on historical mempool and block data.
---

<img src="./abacus.jpeg" alt="abacus" class="center-img">

### Why we have fees

Space in the Bitcoin blockchain is a limited resource, and
given a low enough price, demand for that space will far exceed the supply. If
block space is free, people will find all kinds of uses for it — decentralised
gambling, uploading an entire copy of the Bitcoin whitepaper, and timestamping
individual documents are just a few examples we’ve seen in the past.

To make sure that the limited space in the blocks is allocated to those who
value it most and who are prepared to pay the most for it, Bitcoin has a fee
market. In effect, the mempool acts as a decentralized clearinghouse — users
place bids for block space into the mempool (in the form of transactions with
fee attached), and miners will take transactions and place them in the next
block based on the fee attached. The larger your fee, the more likely it is
that your transaction outbids the competing transactions and that the miner
selects your transaction for inclusion in the next block.

### Why fee estimation is a hard problem

How does a user know what an appropriate fee is? It turns out that’s a really
difficult question to answer, for a few reasons:

* **Supply is unpredictable.** Over long time horizons, supply is predictable.
  There’s approximately 2MB of space every 10 minutes (or to be more precise,
  there’s 4M block weight every 10 minutes). But because of the Poisson
  distribution of block discovery, that supply is lumpy and unpredictable over
  shorter time periods. One in a hundred blocks is discovered within 7 seconds of
  the previous block, and one in a hundred takes over 45 minutes to find. That
  means that there might be a ‘lucky’ run where several blocks are discovered
  within a few minutes, and all the high fee transactions are drained out of the
  mempool. On the other hand, there might be no block discovered for half an hour
  or more, in which case the mempool will slowly fill with higher fee paying
  transactions.  

* **Demand is also unpredictable.** We definitely see cyclicity in
  transaction flow — weekends are generally quieter than week days, so the
  mempool is emptier and fees are lower. However, just like the supply side,
  demand is unpredictable in the short run. For example, even on weekends, demand
  tends to spike during rapid changes in bitcoin price.

* **Different users have different requirements.** Like any market, each
  participant has their own reasons for wanting to ‘buy’ block space. I might
  have a really urgent transaction that needs to be confirmed in the next half
  hour, or maybe I need to close an expiring smart contract in the next 6 hours,
  or perhaps I need to timestamp something and I’m happy as long as it gets
  confirmed some time in the next week. A one-size-fits-all model for fee
  estimation is not able to capture all of those different use-cases.  Estimating
  the correct fee for a given circumstance is therefore difficult, but it’s a
  really important aspect of having a usable system. If your fee estimation is
  too high, then you’re wasting money every time you send a Bitcoin transaction.
  If it’s too low, then you won’t get your transaction confirmed as quickly as
  you’d like, and using the system becomes really frustrating.

We can base our fee estimation on various data points. Let’s have a look at
them in turn. Note that these fee estimation techniques will be used on a full
validating node. We need our own mempool and full blockchain to be able to make
estimates based on observed events on the network.

#### Fee Estimation based on current mempool

A naive fee estimation algorithm would look at your mempool and set your
transaction fee at a level that puts it in the highest-paying 2MB of
transactions. You might expect that strategy to get your transaction confirmed
in the next block. Unfortunately, it’s not quite as simple as that for a number
of reasons:

* Very recent transactions may not make it into the next block. Miners are
  already working on the next block when you submit your transaction. Depending
  on how they refresh the block as they work on it, they may not include your
  transaction.

* Whatever time you send your transaction into the mempool, the
  expected time you’ll have to wait for the next block is 10 minutes. This is a
  fundamental (and often misunderstood) property of the Poisson distribution that
  block discovery follows. If you place your transaction into the mempool 8
  minutes after the previous block, the expected time you’ll need to wait isn’t 2
  minutes — it’s _another 10 minutes_. Therefore you’re not just competing against
  what’s in the mempool now, you’re competing against what’s going to appear in
  the mempool over the next (probably) 10 minutes.

* Looking at a snapshot of the
  mempool doesn’t take into account the fact that there will be lucky runs of
  blocks and slow runs of blocks in the future. It might give you some
  information about how much fee you need for your transaction to be included in
  the next block or two, but can’t tell you anything about how much fee you need
  if you want your transaction included in the next 100 or 200 blocks.

* There’s no such thing as _the_ mempool. Each node will have different
  transactions in its mempool depending on factors such as how long it’s been
  running for, its connectivity to other nodes, its local mempool policies, and
  so on. What you see in your mempool might not be indicative of what miners are
  seeing in theirs.  For those reasons, just a snapshot of the current mempool
  isn’t going to give us enough information to properly estimate the required
  fee.

#### Fee Estimation based on historic blocks

This appears to be a better way to estimate fees at first glance, since the
blockchain is an immutable history of exactly which transactions were included.
However, if we only looked at historic blocks, our fee estimation algorithm
would be trivially gameable by miners. A miner could stuff his block with
private, high fee rate transactions.  Fee estimators that only looked at
historic blocks would be fooled into increasing their estimates because it
would appear that a large fee is required to be confirmed in a block.

This is a very cheap attack for miners, since the cost to them is just the
opportunity cost of excluding real, fee-paying transactions. If our fee
estimator requires that transactions be seen in the mempool before they’re
included in a block, then the cost increases dramatically and the attack
becomes infeasible. The miner would have to broadcast his high fee rate
transactions and risk having to pay those fees to another miner.

#### Fee Estimation based on mempool history

Bitcoin Core therefore considers the historic data for transactions in the
mempool _and_ in recent blocks. If we have a large enough sample of past
transactions, we can make a good model of what fee would have been required to
be included within a certain target number of blocks.

### How Bitcoin Core estimates fees (before v0.15)

_Note 1: fee estimation in Bitcoin Core is rather complex. This article can
only give an overview of the concepts behind the fee estimation algorithm and
makes a few simplifications.  For more details, see Alex Morcos’s [high level description of the fee estimation algorithm][high level desc] 
 or for all the gory details take a look at [the code itself][code]._

[high level desc]: https://gist.github.com/morcos/d3637f015bc4e607e1fd10d8351e9f41
[code]: https://github.com/bitcoin/bitcoin/blob/fd29d3df299bd06c0e6bb218863e0c855b3b91af/src/policy/fees.h

_Note 2: This article describes the fee estimation algorithm from Bitcoin Core
v0.14. There are a number of changes in v0.15 which I’ll cover in a future
article._

#### Concepts: buckets and targets

We’ll start by defining a couple of concepts that are used by the algorithm:
_buckets_ and _targets_.

Bitcoin transactions fee rates fall within an almost continuous range from 1
satoshi per byte up to many hundreds of satoshis per byte, and even higher for
some extreme outliers (See [Jochen Hoenicke’s visualisation][joho] for an idea of what
the current mempool looks like). Keeping track of every fee rate attached to
every transaction would require a lot of computation and storage, so the first
thing Bitcoin Core does is group those transaction fee rates into _buckets_,
where each bucket corresponds to a range of fee rates. That’s a bit like how
Jochen’s visualisation groups the transactions into different colored bands.

[joho]: https://core.jochen-hoenicke.de/queue/#24h

Bitcoin Core wants to be able to make estimates over a very large range of fee
rates, so the lowest bucket starts at 1s/B and extends to 1.1 s/B (10% higher).
The next bucket is from 1.1 s/B to 1.21 s/B (10% higher than 1.1). The next
bucket is from 1.21 to 10% higher than that, and so on. These
exponentially-spaced intervals are extended all the way up to 10,000 s/B. The
last bucket is anything at 9,400s/B and above. At todays exchange rate ($4200),
that’s approximately $88 for a median sized transaction (225 bytes).

The second concept is the number of blocks between a transaction entering the
mempool and being accepted in a block. We’ll call that the target (since we’ll
use this when calculating how much fee we need to attach in order to be
included within a target number of blocks). In v0.14, Bitcoin Core keeps track
of targets from 1 block up to 25 blocks.

#### Keeping track

To estimate how much fee a transaction requires in order to be
confirmed within a certain number of blocks, Bitcoin Core stores a historic
record of the transactions it’s seen in the mempool and blocks. It keeps:

- **A**. the number of transactions that entered the mempool in each fee rate bucket;
and

- **B**. for each bucket-target pair, the number of transactions that successfully
made it into the blockchain within the target number of blocks.

For any target-bucket pair, Bitcoin Core is then able to find the probability
that a transaction with that fee rate would have been included within that
target number of blocks by dividing **B** by **A**.

#### Responding to changes in prevailing fee rate

The Bitcoin network is a dynamic system and prevailing fee rates change over
time (if this wasn’t true, we wouldn’t need fee estimation at all!). We want
our fee estimator to be reactive to changes in prevailing fee rate and to give
more weight to recent events than older events, since they’re more likely to be
indicative of future fee rates.

For that reason, Bitcoin Core uses an _[exponentially weighted moving average][ema]_, or
put more simply, we pay more attention to recent blocks than older blocks.
Every time Bitcoin Core receives a block it multiplies its counters for old
blocks by a _decay value_ of 0.998 (equating to a _half-life_ of 346 blocks). That
means that as a block recedes into the past, it counts for less and less in our
fee estimation algorithm. A block from 2.4 days ago carries approximately half
the weight of the most recent block. A block from 4.8 days ago carries about
one quarter of the weight, a block from 7.2 days ago carries about one eighth
the weight, and so on.

[ema]: https://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average

Note that this moving average is independent from the 24 block target range
mentioned earlier. We’re interested in up to 24 blocks for transaction
inclusion, but we’ll use historical data going back over many blocks.

#### estimateSmartFee(): a usable interface

To make a useful interface, we need to
know what question the user is asking. Bitcoin users almost certainly aren’t
asking:

> If I attach a fee rate in bucket X to my transaction, what’s the exact
> probability of it confirming in Y blocks?

Instead, they need to know:

> I want my transaction confirmed within Y blocks. How much fee should I attach
> to make that likely to happen?

Enter **estimateSmartFee()**, which is designed to do just that.
**estimateSmartFee()** works as follows:

1. The user provides a target number of blocks that they want the transaction to
   confirm within.

2. For that target number, look at the largest bucket (anything above 9,400
   s/B) and verify that for that fee, the probability of being confirmed in
   that number of transactions is at least 95%. (if this fails, then we’re really
   in trouble — it’s saying that even paying the astronomical fee of 9,400 s/B is
   probably not going to be enough. Remember, that’s about $88 for a normal-sized
   transaction at today’s prices).

3. Look at the next highest fee bucket (roughly 8,600–9,400 s/B) and verify
   that for that fee, the probability of being confirmed in that number of
   blocks is at least 95%

4. Keep working down the buckets until we find one where the probability of
   being confirmed is less than 95%

5. Take the previous bucket (the lowest value bucket that had a probability of
   at least 95% of being included) and return the median fee of all
   transactions in that bucket.

When calculating the probabilities for each
target-bucket, the algorithm is smart enough to make sure that there’s a large
enough sample size of transactions. That means that if there’s a small number
high-fee transactions which weren’t confirmed for some reason, the fee
estimation algorithm won’t get thrown off.

We use a high threshold of 95% because we want the fee estimator to be able to
tell us that a transaction at a certain fee rate would almost certainly have
been included within target blocks. The fee estimator does not have perfect
knowledge of why transactions were included in a block (for example, there may
have been out-of-band payments to the miner to get a certain class of
transactions confirmed quicker than other transactions with the same or lower
fee rate), so we set the bar high but not at 100% to give us a high confidence
in our estimate.

**estimateSmartFee()** is used by the **estimatesmartfee**, **sendtoaddress**
and sendmany RPCs, and when sending a transaction in the GUI.

### Conclusion

Fee estimation is a difficult problem. A fee estimator is essentially trying to
answer a question about the future based on an incomplete picture of the past.
It’s not clear how well we can measure the success of different fee estimation
algorithms, in part because different users have very different requirements of
the system. Furthermore, the fee market in Bitcoin is constantly changing, and
a fee estimation algorithm that is successful in today’s Bitcoin environment
may not be successful in the event of large systemic changes (eg the emergence
of another coin that mines using SHA-256, the roll out of segregated witness
transactions, secular changes in overall demand and mempool congestion, and so
on). Bitcoin Core provides a fee estimation algorithm that is appropriate for a
large number of users in a wide variety of fee market circumstances. Other
wallets may have very different approaches to fee estimation which could be
more successful for certain users in certain circumstances.

Bitcoin Core’s fee estimation doesn’t try to be too smart. It simply records
and reports meaningful statistics about past events, and uses that data to give
the user a reasonable estimate of how much fee they need to attach in order to
have their transaction included within N blocks. It doesn’t try to be
forward-looking, and it’s easy to describe exactly why a given estimate has
been produced based on past statistics. It can react to changes in the
prevailing fee market and give reasonable estimates in a wide range of
conditions.

A more sophisticated algorithm may attempt to be more forward-looking. However,
the more complex the algorithm, the more difficult it becomes to describe its
operation and results, and the more difficult it is to argue that the algorithm
is safe against manipulation.

There are cases where the Bitcoin Core fee estimator does not perform well,
notably when there are very rapid changes in the prevailing fee market. The fee
estimations in Bitcoin Core v0.15 builds on the same framework as the v0.14
algorithm, but has many improvements to make it more robust in the case of
changing circumstances and outlier events. I’ll describe what those changes are
in a future blog post.

_originally posted at [https://bitcointechtalk.com/](https://bitcointechtalk.com/)_
