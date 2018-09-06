---
title: "What's New in Bitcoin Core V0.15 - Part 3"
date: 2017-09-16T00:00:00-04:00
---

Yesterday, I wrote about [how fee estimation is better in
v0.15](https://johnnewbery.com/post/whats-new-in-bitcoin-core-v0.15-pt2/),
but what happens if you send a transaction without enough fee to be included in
a block? Somehow you need to encourage miners to include your transaction, or
it’ll be stuck in limbo forever (or at least until it drops out of nodes’
mempools). There are two ways to ‘unstick’ your transaction and get it into a
block:

* *Child Pays For Parent (CPFP)* — a new transaction which spends the outputs of
the stuck transaction. This child transaction attaches enough fee to pay for
itself *and* its parent transactions to be included in a block. Since v0.13, the
Bitcoin Core mining code is intelligent enough to consider ‘packages’ of
transactions when filling a block, and will look at the total fee-rate across
the ancestors and descendant (this feature should rightly be called
Descendants-Pay-For-Ancestors since the mining code considers chains of
transactions up to 25 in length). That means that if you create a descendant
transaction with a high fee, the miner will include both the ancestors and
descendant transactions in the next block so that it can collect the large total
fee for the transaction chain.
* *Replace By Fee (RBF)* — a new transaction which essentially double-spends the
stuck transaction. The signer of the original transaction creates a new
replacement transaction that spends the same inputs but pays additional fee
(usually by reducing the amount of bitcoin for the change output and leaving the
extra bitcoin as fee for the miner). If the replacement transaction attaches
enough fee, then miners will be incentivized to include it in a block.

**Replace-by-fee in the GUI (PRs
[9592](https://github.com/bitcoin/bitcoin/pull/9592) and
[9697](https://github.com/bitcoin/bitcoin/pull/9697))**

<img align="middle" src="./hands_cash.jpeg" alt="hands_cash">

Since v0.12, Bitcoin Core has supported ‘opt-in RBF’. This is where a
transaction signals that it is replaceable and other nodes will allow RBF
transactions to replace the original if enough additional fee is attached. Since
v0.14, Bitcoin Core has also included a `bumpfee` command which will create a
replacement transaction for an unconfirmed transaction. v0.15 brings this
functionality into the GUI. New transactions can be marked as ‘opt-in RPF’ and
stuck transactions can be bumped.

This is great news for end-users who interact with Bitcoin Core through the GUI
rather than through the Command Line. For the first time they’ll be able to mark
transactions as replaceable and then create RBF transactions if they get stuck.
The end result should be users not over-paying transaction fees. That’s good for
the individual user and also for the fee market overall — if all users are able
to pitch their fee rate more accurately, the block space will be allocated more
efficiently to those who value it.
