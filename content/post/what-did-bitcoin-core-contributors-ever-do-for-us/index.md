---
title: "What Did Bitcoin Core Contributors Ever Do for Us?"
date: 2017-07-21T00:00:00-04:00
summary: A short summary of work that Bitcoin Core developers have contributed to the project.
---

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">When you fire core, I presume you&#39;re also going to ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888506387030003712?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

This afternoon, I tweeted a response to the strange suggestion that we
**fire core**. I’ve ignored the fact that Bitcoin Core isn’t a person or an
organization (in the traditional sense), and that everyone is perfectly free to
run their own re-implementation of Bitcoin, but instead focused on a few of the
things you’d need to do if you were serious about rejecting the work of the
Bitcoin Core contributors.

I’ve included a mix of enhancements that have been around for one or more
releases, stuff that’s going in to 0.15 right now, and longer-term development
or research work. People who don’t actively follow the
[bitcoin core github repository][bitcoin core github repo] probably aren’t
aware of the wide range of work that the contributors are doing. Hopefully this
gives some insight into that world.

[bitcoin core github repo]: https://github.com/bitcoin/bitcoin/

Full disclosure: I contribute to Bitcoin Core.

So here goes, what have Bitcoin Core developers ever done for us?

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... switch back from Pieter&#39;s libsecp256k1 to OpenSSL, so your transaction signing/validation is 5x slower and less secure ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888506710649950208?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

[libsecp256k1][libsecp] is a heavily optimized library for doing elliptic curve math over
Bitcoin’s secp256k1 curve. Elliptic curve math is used for creating signatures
to spend transactions, and for validating signatures in transactions that you
receive from the network. In addition to being several times faster than
OpenSSL, libsecp256k1 has much better protection against timing,
derandomization and side-channel attacks. Bottom line: transaction
signing/validation is faster and more secure.

libsecp256k1 was mostly written by Pieter Wuille, Andrew Poelstra, Peter
Dettman and Greg Maxwell, and [started being used][libsecp PR] by Bitcoin Core in v0.12.
Pieter, Andrew, Peter and Greg continue to maintain and make improvements to
libsecp256k1.

[libsecp]: https://github.com/bitcoin-core/secp256k1
[libsecp PR]: https://github.com/bitcoin/bitcoin/pull/6954

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... remove Suhas&#39;s pruning code, so you need to store tens of GBs of dead data if you want to run a full node ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888506811845922816?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Pruning allows a full node to discard old blockchain data, while still fully
validating all the consensus rules. It means that users can run a Bitcoin Core
node on diskspace-constrained hardware and enjoy the **exact same** security of
running a full node. The blockchain is now over 125GB, but a pruning node can
be fully synced to the network with just 2–3GB of disk storage.

[Automatic pruning functionality][pruning PR] was added in Bitcoin Core V0.11. The code was
mostly written by Suhas Daftuar, Alex Morcos, Adam Weiss and Brad Andrews.
Pruning was further improved in V0.14 to [allow pruning to be run manually by the user][manual pruning PR].
Principal contributors were Brad Andrews and Russ Yanofsky.

[pruning PR]: https://github.com/bitcoin/bitcoin/pull/5863
[manual pruning PR]: https://github.com/bitcoin/bitcoin/pull/7871

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... revert Luke&#39;s multiwallet so you can only access a single wallet on your node ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888506895941615616?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Multiwallet is a long-requested and wanted feature that has finally been merged
in v0.15 🎉. This allows users to have completely segregated wallets, for
use-cases such as separating business and personal accounts or having wallets
for different purposes running concurrently. We don’t yet have separate
authentication for different users, but future versions may allow multiple
users to safely access different wallets on the same Bitcoin node.

Luke Dashjr contributed [multiwallet][multiwallet PR] in V0.15. The
[RPC interface][multiwallet RPC] was provided by Jonas Schnelli.

[multiwallet PR]: https://github.com/bitcoin/bitcoin/pull/8694
[multiwallet RPC]: https://github.com/bitcoin/bitcoin/pull/10849

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... undo Cory&#39;s net refactor so your transactions and blocks take longer to propagate across the network ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888506982570876928?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Having a fast, efficient networking layer is essential for quick
block/transaction propagation and the overall health of the network. The faster
that blocks are able to propagate through the network, the lower the stale
block rate, and the more secure the network is.

Cory Fields has been doing continued work to refactor the networking code for
several releases, with a [major and significant improvement][Net speedup PR]
delivered in V0.14.  V0.15 and future releases will continue to see
improvements in cleaning up and isolating the network code from the server
code.

[Net speedup PR]: https://github.com/bitcoin/bitcoin/pull/9441

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... throw out Greg&#39;s signature aggregation research so your blocks will contain fewer transactions and take 2-4x longer to validate ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888507085071282176?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

One of the most exciting [benefits of segregated witness][segwit benefits] is
that it gives us the ability to upgrade the scripting language. There are
several exciting script upgrades under investigation, but the one that will
probably get most attention in upcoming releases is Schnorr signature support.
Schnorr signatures are an alternative signature scheme to the currently used
ECDSA which allow multiple signatures to be added together or ‘aggregated’.
This is a win for scalability (since if multiple signature are added together,
the aggregated signatures takes up only as much space as one of input
signatures), validation cost (since only one signature needs to be validated
instead of many) and privacy (since an aggregated signature doesn’t reveal
whether the input was a single signature or many signatures).

Greg Maxwell, Pieter Wuille and Andrew Poesltra have been
[investigating Schnorr signature aggregation][sig agg], particularly working to
make sure that the aggregation scheme is safe from the signature cancellation
problem.

[segwit benefits]: https://bitcoin.org/en/release/v0.13.1#segregated-witness-soft-fork
[sig agg]: https://bitcoincore.org/en/2017/03/23/schnorr-signature-aggregation/

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... get rid of Russ&#39;s process separation groundwork, so your signing code will be in the same memory space as your network code ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888507180793581568?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Currently, Bitcoin Core exists as a single process, with shared memory access
between the network code, consensus code, wallet code and user interface code.
Ideally we’d like to separate the wallet into a separate process, so if the
networking function was hacked or compromised, your wallet function and private
keys would be safer.

Russ Yanofsky has been [doing the groundwork for process separation][process separation]
during V0.15. Look out for further progress in this area in V0.16 and V0.17.

[process separation]: https://github.com/bitcoin/bitcoin/pull/10102

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... erase Alex&#39;s fee estimation improvements so you pay too much for your transactions...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888507260196069380?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Every transaction submitted to the Bitcoin network attaches a user-chosen fee,
which goes to the miner who confirms that transaction in a block. Set the fee
too low and your transaction won’t get confirmed in a block. Set it too high
and you’ve donated money to the miner unnecessarily. Between those two extremes
is a continuum of where to set your fee — a high fee will probably get you
confirmed in the next block, a slightly lower fee might see your transaction
confirmed in the next 3 or 4 blocks, and even lower than that and your
transaction could take a few hours to get confirmed. Choosing the correct fee
for your transaction is a hard problem, requiring knowledge of the current
state of the network and some smarts to predict what will happen depending on
where you set the fee.

Alex Morcos has [spent a lot of time thinking about and analyzing fee strategies][fee estimation gist]
and [significantly improved the fee logic][better fee estimation] in V0.15.

[fee estimation gist]: https://gist.github.com/morcos/d3637f015bc4e607e1fd10d8351e9f41
[better fee estimation]: https://github.com/bitcoin/bitcoin/pull/10199

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... back out Matt&#39;s multithreading and scheduling refactors, so your node is mostly limited to running a single process ...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888507364265119747?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Bitcoin Core runs multiple threads so different tasks can be run in parallel on
a multi-core computer. However, a lot of the functions grab a ‘global lock’
before doing their work, and other threads need to wait for that global lock to
be released before they can continue with their work. Result: Bitcoin Core is
not as able to do as much work in parallel as we’d like. If we can reduce the
places where that global lock is grabbed and held, then Bitcoin Core would be
able to things like run wallet tasks, validate blocks and serve blocks and
transactions to peers simultaneously .

This is **very** delicate work and requires a deep understanding of Bitcoin Core’s
multi-threading model. Get it wrong and you could easily cause crashes or
memory corruption. Matt Corallo has done [a lot][multithread 1] of
[the][multithread 2] [plumbing][multithread 3] [work][multithread 4] for this in
V0.15. We should see some major payoff for that work in V0.16.

[multithread 1]: https://github.com/bitcoin/bitcoin/pull/9725
[multithread 2]: https://github.com/bitcoin/bitcoin/pull/9605
[multithread 3]: https://github.com/bitcoin/bitcoin/pull/10178
[multithread 4]: https://github.com/bitcoin/bitcoin/pull/10179

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... delete Jonas&#39;s and Nicolas&#39;s hardware wallet integration work, so your private keys will always be in your hot wallet...</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888507476173357064?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Several companies now offer hardware wallets, which allow you to keep your
private keys and signing code on a dedicated security device. That’s a much,
much more secure model than having your private keys on a network-connected
computer, which could potentially get hacked. Sadly there’s no standardized
interface for hardware wallets, so each vendor provides their own software
wallet to use with their hardware wallet. It’d be great if Bitcoin Core could
support hardware wallets so users could benefit from running fully
hardware-separated signing code behind the most secure Bitcoin full node.

HWW support is probably at least a couple of releases away, but Jonas Schnelli
and Nicolas Dorier have already been doing some [early][hww 1] [work][hww 2] to
make sure that Bitcoin Core is ready for HWW support. Hopefully we’ll see some
more progress on this in V0.16 or V0.17.

[hww 1]: https://github.com/bitcoin/bitcoin/pull/9728
[hww 2]: https://github.com/bitcoin/bitcoin/pull/9662

<blockquote class="twitter-tweet" data-conversation="none" data-lang="en"><p lang="en" dir="ltr">... and find someone who&#39;s prepared to do Wladimir&#39;s thankless and never-ending task of merging and preparing releases?</p>&mdash; John Newbery (@jfnewbery) <a href="https://twitter.com/jfnewbery/status/888507574273818624?ref_src=twsrc%5Etfw">July 21, 2017</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Of course, none of these code changes would be of any use at all if we didn’t
have repository maintainers to do the work of signing and merging all the
commits, making sure translations are ready, preparing release notes, and doing
all the other things that turn a bunch of code changes into a software product
that normal people can run. Wladimir van der Laan is lead maintainer and has
been tirelessly doing that work for many releases. Everyone in the Bitcoin
community owes him a huge debt of gratitude.

I’ve tried to give shout-outs to the main contributors behind each of these
features. Open-source software is a collaborative activity and there are far
more who have contributed code, review, testing time, documentation and much
more to these and other initiatives. If I’ve made any egregious omissions,
please accept my apologies and message me on twitter so I can set the record
straight!

_originally posted at https://medium.com/@jfnewbery/_
