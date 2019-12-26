---
title: "What's New in Bitcoin Core V0.15 - Part 5"
date: 2017-09-18T00:00:00-04:00
summary: "What's new in Bitcoin Core part 5 of 5: script caching."
---

This is the final article in [this
series](https://johnnewbery.com/post/whats-new-in-bitcoin-core-v0.15-pt1/)
about features and improvements in Bitcoin Core v0.15. Today I’ll talk about a
small implementation change by Matt Corallo that gives a huge boost in
performance for nodes that are in sync and keeping up with the blockchain.

<img src="./fast.jpeg" class="center-img">
<p style="text-align:center">*Block validation: now up to 50% faster!*</a>

**Script Caching ([PR 10192](https://github.com/bitcoin/bitcoin/pull/10192))**

This is another great performance improvement, this time in new block validation
time when the node is up to date with to the chain tip. Under normal
circumstances, blocks will now validate around 40–50% faster.

How can we achieve such a dramatic speed-up? It starts from the observation that
once your node has been up and running for some time, every time it receives a
block it will already have seen the majority of transactions within that block.
That’s because the miner who created the block is collecting the transactions
for the block from the same P2P network that your node is connected to, and so
your node already will have seen the transactions as they were being propagated
across that network.

In early versions of Bitcoin Core, almost every transaction would therefore be
validated twice — first when it was received as an unconfirmed transaction and
accepted into your mempool, and again when it was received in a block. Doing the
same computational task twice is an obvious target for optimization, and the
first big improvement here was the addition of a [signature
cache](https://github.com/bitcoin/bitcoin/pull/1349) in v0.7. Signature
validation involves elliptic curve math and is the most expensive part of script
validation, so if we can save having to do a signature validation twice, that’s
a big win. After v0.7, if Bitcoin Core received an unconfirmed transaction that
validated and was accepted into the mempool, it would cache the result of the
signature validations. Then, if it received a block containing that same
transaction, instead of validating the signatures again, it would just look up
the result in its cache.

This small change results in a huge performance improvement in block validation
times.

The obvious question is: why not cache the validity of the entire transaction?
Wouldn’t that be an even bigger performance win? Unfortunately, that’s not
possible since transaction validity is *context-specific*. That’s to say that a
transaction can be valid in one block, but invalid in a different block. Here’s
one way that a consensus failure could occur if we cached the transaction
validity:

1.  The main chain tip is at height 1000
2.  Transaction A is received with nLockTime set to block 1001. It is evaluated as
valid since the next block will be height 1001.
3.  A miner re-orgs block 1000 out of the main chain by building block 1000’ on top
of block 999. Block 1000’ includes transaction A.

The result is a chain-split. Those nodes that first saw transaction A before the
re-org consider block 1000’ to be valid since they already evaluated transaction
A as valid. Those nodes that didn’t see transaction A before the re-org see
block 1000’ as invalid since transaction A is invalid in any block before 1001.

So we can’t simply cache the transaction validity without introducing the risk
of a consensus failure, but we can (*and do*) cache the signature validity. Matt
observed that we can do something between the two: we can cache the validity of
the scripts within a transaction, without caching the validity of the entire
transaction. Crucially, within a Bitcoin transaction, validity of the scriptSigs
is not contextual of any outside information. This is a really important point,
and the recent CLTV (Check Locktime Verify) and CSV (Check Sequence Verify) BIPs
were very carefully designed to preserve this property.

Matt’s change adds a script cache in addition to the signature cache, so from
v0.15, if we receive an unconfirmed transaction we’ll cache both the results
from the ECDSA signature validations, and the results from the input script
evaluations.

Unlike Pieter’s per-output chainstate db change, this wasn’t a particularly
large code change (+449 lines, -43 lines compared to +1109 lines, -1055 lines
for Pieter’s change), but don’t underestimate the difficulty. People have
attempted to do similar things to this before and introduced consensus bugs like
the one described above. See [PR
6077](https://github.com/bitcoin/bitcoin/pull/6077) and [PR
5835](https://github.com/bitcoin/bitcoin/pull/5835) for example. The value of
Matt’s contribution is that he has a deep understanding of the consensus code
and more experience in writing and maintaining that code than almost anyone
else. Very few people could have implemented something like this without
introducing consensus bugs.

The result of this change is that new block validation is roughly 40–50% faster
on average. A huge improvement!

**Conclusion**

Bitcoin Core v0.15 final was released this week and is available for download
from [bitcoincore.org](http://www.bitcoincore.org/). This release brings a few
really nice new user features and some significant performance improvements, as
well as laying the groundwork for further improvements and features in v0.16.
There’s a whole slew of smaller changes that I haven’t included here. Check [the
release notes](https://bitcoincore.org/en/releases/0.15.0/) if you want a
complete listing.

*Thanks to Matt Corallo and Jimmy Song for feedback and input.*

_originally posted at https://bitcointechtalk.com/_
