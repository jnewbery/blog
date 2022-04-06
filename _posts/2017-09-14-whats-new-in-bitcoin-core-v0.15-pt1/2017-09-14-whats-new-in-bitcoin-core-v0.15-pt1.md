---
layout: post
title: "What's New in Bitcoin Core V0.15 - Part 1"
category: blog
excerpt: "What's new in Bitcoin Core: per-output chainstate database."
---

I’m very excited about the recent [Bitcoin Core v0.15
release](https://github.com/bitcoin/bitcoin/releases/tag/v0.15.0). This is the first major
release that I’ve been involved in from start to finish, and there are some
great new features and improvements. Over the next few days, I’ll present a
series of articles highlighting five of the most interesting changes to look out
for.

I’m going to dive quite deep into the technical details of these changes since I
think they’re all interesting and instructive. If you’re not interested in those
details and just want a high-level overview of what’s new, then [the release
notes](https://bitcoincore.org/en/releases/0.15.0/) are a better place to look.

We’ll start by getting under the hood and look at an implementation change.
Users shouldn’t see any changes in behaviour from this change, except for their
Bitcoin Core client performing much better.

**Per-output chainstate db ([PR
10195](https://github.com/bitcoin/bitcoin/pull/10195))**

<img src="./chain.jpeg" class="center-img">

Per-output chainstate db is a fantastic win in Initial Block Download time and
general performance, as well as being a huge improvement in code simplicity. It
also removes a potential DOS vector where an attacker could exhaust a node’s
memory with carefully constructed transactions. Users shouldn’t see any
functional difference, but it gives such a performance improvement that it’s
worth looking at in more detail.

First, a bit of blockchain theory and history. The blockchain is simply an
ordered log of the transactions that have been accepted by the network up to
certain time. Once the blocks have been validated, that blockchain data is no
longer useful to the node. What we’re actually interested in is the UTXO set —
the set of all transaction outputs that have not yet been spent. All full nodes
must keep a copy of this set so they can verify that transactions are spending
coins that actually exist and that the signatures for those transactions are
valid. In Bitcoin Core, that UTXO set is stored in a database called the
*chainstate* db. Ideally a node would store this entirely in memory for fast
lookups, but the chainstate can be flushed to disk if the node doesn’t have
enough RAM to store the entire set.

The original Bitcoin software stored the entire block tree data, transactions
and spends in a database called blkindex. Transactions would never get removed
from that database, even when all of the outputs of those transactions had been
spent. That’s fine up to a certain point, but it’s not scalable. Transactions
grow linearly over time, and as the database grows, the time it takes to seek
all the outputs for a new block in the database also grows. The result would be
that the database would continue expanding and block validation and propagation
would slow down more and more over time. If we’d kept using this model, all full
nodes would be required to keep the full blockchain (roughly 130GB at the time
of writing), and block validation would be *really* slow.

The first major change to the model came in v0.8, which included
[ultraprune](https://github.com/bitcoin/bitcoin/pull/1677). Ultraprune split up
blkindex into a blocks database (for storing the historical blockchain), and a
chainstate database (for storing transactions and outputs). The chainstate
database was structured *per-transaction*. That meant that the main entry in the
database was a list, containing *all* the outputs of a given transaction. As
soon as all the outputs from a transaction had been spent, the entire
transaction could be pruned from the chainstate database. This split also made
block pruning possible, which [was implemented in
v0.11](https://github.com/bitcoin/bitcoin/pull/5863). The result of those
changes together meant that today it’s possible to run a full validating node
with only 4–5GB of disk space.

That’s the historical context. So what’s changed in v0.15? The chainstate
database has been changed to be structured *per-output* instead of
*per-transaction*. In practice that means:

* It’s much faster to read and write individual outputs from the database, since
we don’t need to read and write all of the containing transaction’s unspent
outputs, just the output that we’re interested in. That means that validating a
block is faster.
* Memory usage is much smoother and can’t be blown up when reading/writing large
transactions from the database. That means that we can use the chainstate cache
more efficiently and flush to disk less often.
* The code is much simpler, and we can make future improvements to flushing the
chainstate database to disk.

There’s one small drawback to this:

* The chainstate database becomes slightly larger. The reason the chainstate was
initially implemented per-transaction was that it saved disk space. Instead of
storing the transaction id once for each output, it only needed to be stored
once across all the outputs in a transaction. Now, we need to store the txid
once per output. This is partially mitigated by compression in the database
layer which can avoid writing the same txid multiple times. In practice, the
chainstate database will be about 15% larger with this change.

So what’s the bottom line for users? There are some performance results in [the
Pull Request](https://github.com/bitcoin/bitcoin/pull/10195):

* Initial Block Download (IBD) and reindex is 30–40% faster
* IBD and reindex use 10–20% less memory
* IBD flushes to disk far less frequently.

30–40% speed-up in IBD is an enormous win. It means that when you start up a
fresh node, you’ll catch up to the chain tip much more quickly.

*Thanks to Pieter Wuille, Matt Corallo and Jimmy Song for input and feedback.*

_originally posted at https://bitcointechtalk.com/_
