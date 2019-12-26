---
title: "What's New in Bitcoin Core V0.15 - Part 4"
date: 2017-09-17T00:00:00-04:00
summary: "What's new in Bitcoin Core part 4 of 5: multi-wallet support."
---

In this series, I’ve already covered one performance improvement ([per-output
chainstate
db](https://johnnewbery.com/post/whats-new-in-bitcoin-core-v0.15-pt1/))
and a couple of user features ([better fee
estimation](https://johnnewbery.com/post/whats-new-in-bitcoin-core-v0.15-pt2/)
and [bumpfee in the
GUI](https://johnnewbery.com/post/whats-new-in-bitcoin-core-v0.15-pt3/)).
Today I’ll talk about another user feature, multi-wallet.

**Multi-wallet Support ([PR
8694](https://github.com/bitcoin/bitcoin/pull/8694))**

<img src="./multiwallet.jpeg" class="center-img">

Multi-wallet is a feature that’s long been requested by users, and has now been
implemented in Bitcoin Core. Users are now able to load more than one wallet
when starting the software. Each wallet is completely separated from all others,
with its own keys, addresses, balance and transaction outputs.

There are many possible use-cases for multi-wallet, such as:

* Having separate ‘personal’ and ‘business’ wallets, with accounting for those
wallets completely separated.
* One user having multiple wallets for different purposes, for example a ‘savings’
wallet and a ‘checking’ wallet.
* One user having a normal transacting wallet, and an additional wallet for a 2nd
layer application such as lightning, tumblebit or joinmarket.
* Multiple users having a wallet on a shared node. Note that **there is no
authentication for individual wallets**, so the users must trust each other.
Future versions may introduce authentication for separate user access to
individual wallets.

When using multi-wallet, each wallet is available through the bitcoin-cli
command line tool and the JSON RPC interface. In v0.15 the GUI will only display
and allow transactions to be created and signed on the first wallet. However,
additional loaded wallets will continue to remain synced to the node and will
continue to keep track of their balances and transaction which involve them.
This usage pattern, called ‘wallet warming’, is useful if you want your home
node to keep track of the wallet’s transactions and balances, but transact with
that wallet on different software (eg a separate instance of Bitcoin Core).
Future versions should allow all wallets to be controlled through the GUI.

I’m excited about multi-wallet in v0.15, and I think that changes in v0.16 and
beyond will build even more functionality on top. As an example, v0.16 should
allow wallets to be dynamically loaded and unloaded during runtime, so it will
no longer be necessary to stop and restart the node in order to load a new
wallet. Loading and unloading a wallet should be as simple as opening a new
document in a word processor.

_originally posted at https://bitcointechtalk.com/_
