---
title: "What's New in Bitcoin Core V0.15 - Part 2"
date: 2017-09-15T00:00:00-04:00
draft: true
---

This article continues the series on enhancements and new features in Bitcoin
Core v0.15. Yesterday I talked about a low-level technical change that results
in dramatic performance wins. Today, I’ll cover something much more visible to
users — significantly improved fee estimation.

Better Fee Estimation (PR 10199)


I recently wrote about Bitcoin Core fee estimation in v0.14. It’s a huge
subject and I was only able to scratch the surface. I recommend you take a look
at that article first to familiarise yourself with the concepts and terminology
used in Bitcoin Core’s fee estimation.

Bitcoin Core v0.15 takes the same framework and makes some substantial
improvements that makes fee estimation a lot more accurate and reactive to
changes in prevailing fee rates. Here’s a high-level summary of the changes:

The algorithm is smarter about making sure enough data has been gathered in
order to return a valid estimate. This means that fee estimation is less
sensitive to extreme outliers skewing the estimates. If not enough data has
been gathered, then the algorithm will return a fallback default fee.  The fee
rate buckets are smaller, which means that the fee estimate returned by the
algorithm should be more precise.  Estimates are now tracked on 3 different
time horizons, which means the estimates adjust more quickly to changes in
conditions, and also allow targets of up to 1008 blocks (~1 week). Previously
only targets of up to 25 blocks could be used. This change is really useful for
users who want their transaction included at some point, but are prepared to
wait for a few days to substantially reduce their fee.  Fee estimates can now
be conservative or economical. Conservative estimates use longer time horizons
to produce an estimate which is less susceptible to rapid downward changes in
fee conditions. Economical estimates use shorter time horizons and will be more
affected by short-term changes in fee conditions. Economical estimates may be
considerably lower during periods of low transaction activity (for example over
weekends), but may result in transactions being unconfirmed if prevailing fees
increase rapidly. For transactions that are marked as replaceable, the wallet
will use an economical estimate by default, since the fee can be ‘bumped’ if
the fee conditions change rapidly (See PR 10589).  A new estimaterawfee RPC has
been added so that advanced users can implement their own fee estimates using
the raw data collected by Bitcoin Core.  There are a number of changes under
the covers that allow these improvements to be exposed to the user:

The whole algorithm is repeated three times over different time horizons: Short
history (for targets up to 12 blocks), Medium history (for targets up to 48
blocks) and Long history (for targets up to 1008 blocks).  For the longer time
horizons, Bitcoin Core uses ranges of confirmation targets rather than keeping
track of every target-bucket pair.  The estimateSmartFee() calculation
previously used a success rate of 95% at the target number of blocks. That’s
changed to now requires a 60% success rate at half the target, an 85% rate at
target and a 95% rate at double the target.  The estimateSmartFee() calculation
has also been improved so that if it fails to hit the success threshold for a
certain target-bucket, it will see if it can get back above the threshold by
continuing to add datapoints from lower fee rate buckets. This makes the
algorithm more robust against outliers skewing the results.  The fee buckets
are now spaced at 5% intervals instead of 10%. This is made possible by the
above change, since the algorithm is now less susceptible to small datasets in
a target-bucket pair resulting in a bad estimate.  Transactions which leave the
mempool due to eviction or other non-confirmed reasons are now taken into
account by the fee estimation logic, leading to more accurate fee estimates.
The estimateSmartFee() interface now takes a conservative/economical argument.
Conservative estimates require a 95% success threshold for double the target to
be met at longer time horizons.  As explained in my previous article, the
Bitcoin Core fee estimation algorithm simply records and reports meaningful
statistics about past events in order to give the user a reasonable estimate of
how much fee they need to attach. It doesn’t attempt to be forward-looking and
by design does not try to be too smart.

The changes in v0.15 continue this philosophy. The v0.15 algorithm isn’t trying
to be too clever, but simply extends the existing algorithm to improve
performance under a range of circumstances.

For full details of the algorithmic changes, see Alex Morcos’s gist and the
Pull Request.

Thanks to Matt Corallo, Alex Morcos and Jimmy Song for input and feedback.

Want to get curated Technical Bitcoin News? Sign up for the Bitcoin Tech Talk
newsletter!
