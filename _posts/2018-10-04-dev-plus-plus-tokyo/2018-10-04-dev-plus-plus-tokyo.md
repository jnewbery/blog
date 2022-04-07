---
layout: post
title: "Bitcoin Edge Dev++ Tokyo - Digital Signatures and Script"
category: talk
excerpt: Two educational talks at the second iteration of Bitcoin Edge Dev++ at Keio university in Tokyo.
---

I gave two educational talks at the second iteration of
[Bitcoin Edge Dev++][devplusplus] at Keio university in Tokyo, immediately preceeding the
[Scaling Bitcoin Conference][scaling].

I covered the following topics:

#### Digital signatures - finite fields, elliptic curves, Schnorr signatures and ECDSA

- [slides][signatures slides]
- [transcript][signatures transcript]
- [video][signatures vid]

Corrections:

- The slide on Cyclic Groups said "The integers modulo p for any number p is a cyclic group". It should say "The integers modulo p for any *prime* p is a cyclic group". (If p is composite, ie p = ab, then the order of a in G is b, so G is not cyclic).
- during the talk, I was asked _“how does the verifier know `K` in the non-interactive schnorr identification protocol?”_ I said that `K` can be provided by the prover. That’s wrong. In fact, the verifier calculates `K` himself and then checks that `e` is the hash of `K`. The verification step is checking that `e` does in fact commit to `K`.

The slides above are corrected.

#### Bitcoin script

- [slides][script slides]
- [transcript][script transcript]
- [video][script vid]

[devplusplus]: https://keio-devplusplus-2018.bitcoinedge.org/
[scaling]: https://scalingbitcoin.org/
[signatures slides]: ./signatures.pdf
[signatures transcript]: http://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/digital-signatures/
[signatures vid]: https://www.youtube.com/watch?v=DcGm_4-ig1o
[script slides]: ./script.pdf
[script transcript]: http://diyhpl.us/wiki/transcripts/scalingbitcoin/tokyo-2018/edgedevplusplus/scripts-general-and-simple/
[script vid]: https://www.youtube.com/watch?v=np-SCwkqVy4
