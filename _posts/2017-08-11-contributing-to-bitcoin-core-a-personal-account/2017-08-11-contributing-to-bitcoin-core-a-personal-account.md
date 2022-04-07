---
layout: post
title: "Contributing to Bitcoin Core, a Personal Account"
category: blog
excerpt: Lessons from my first six months of contributing to Bitcoin Core.
---

In January of this year, I moved to New York to take a job contributing full
time to open source Bitcoin projects. These are some of my experiences in those
first few months.

First of all, I recognize that I’m incredibly fortunate. Not only do I have
tremendous freedom to work on what I think is important or interesting, I get
to sit alongside and work directly with brilliantly talented and motivated
people. All the work I do is open source, and I’m contributing to a fascinating
technology which will be hugely important over the coming years. There’s almost
nothing more I could ask for, and I often need to remind myself that this is
real, and that somehow this is my living.

But in more practical terms, what have I actually learned since I’ve been here?

#### Start small

<img src="./acorn.jpeg" class="center-img">

I’m the first to admit that I’m not the best or most experienced programmer. I
started my professional career as a software developer but very quickly moved
into a support role, managing customer projects and support teams. I made that
choice because that was what would let me meet interesting people and travel to
exotic places. That seemed much more intriguing than working on code, and as a
result I’ve spent the last few years working with customers and teams, rather
than writing and debugging code.

Bitcoin is a very complex project, one which runs on multiple platforms in
multiple environments, and which at its heart is a consensus engine — where
each participant must walk forward in lockstep, or else the whole system will
partition and fall apart. In fact, in bitcoin’s early days this came close to
happening on more than one occasion. Needless to say, any changes to those
parts of the code need to be made extremely carefully, and there are really
only a few people in the world who understand the system well enough to be able
to safely work in those areas. Other people have tried to make changes to
consensus, and more often than not they’ve failed spectacularly.

So as a noob, what to do? Well, although I’m no C++ wizard, I can hold my own
in Python, which is what the bitcoin functional test framework is written in. I
was able to clean up some of that code, fix bugs in the tests, and uncover and
fix bugs in the product code. Through working on the tests, I was slowly able
to get exposure to other parts of the codebase — the RPC server and client, the
wallet, the build system, and so on, which I’m now able to make modest
contributions to.

Here’s my first merged code commit to Bitcoin Core: [adding extra testing for
the bitcoin-tx utility](https://github.com/bitcoin/bitcoin/pull/8829). A modest
contribution, but we all need to start somewhere!

#### Hold yourself accountable

<img src="./clock.jpeg" class="center-img">

As my experience of the code base has increased, so too has the surface over
which I can work. Every day, the list of things that I think I could or should
work on, and the number of projects I think would be a worthwhile use of my
time, increases rather than decreases. With such freedom, it’s very easy to
spread oneself too thin, or to constantly pick up and then drop projects. I’ve
done this myself and found it to be ultimately unsatisfying.

Furthermore, an open-source project isn’t like a normal job. There aren’t
management lines holding you to account and enforcing deadlines from the top
down. Any contribution you make is down to you, and if you start something and
then drop it later, there’s really nothing anyone else can do about it.
Everything you contribute is voluntary.

I’ve found it useful to pick a more challenging longer-term project and commit
to seeing it through. In the first few months, for me that project was
[refactoring the functional test framework into using a TestNode
class](https://github.com/bitcoin/bitcoin/pull/10082), which I very much hope
will be finished in the next couple of weeks. It’s been a long and at times
frustrating journey to get this far, but I think ultimately the test framework
will be in a much better shape when I’m finished. My next goal is to push
forward wallet-server separation starting
[here](https://github.com/bitcoin/bitcoin/pull/10762), and lay the groundwork
for full hardware wallet integration in v0.16 or v0.17. Having a goal, sharing
it with other people, and holding yourself accountable to it is a really useful
exercise.

#### Sharpen the tools

<img src="./tools.jpeg" class="center-img">

Always, always, always be sharpening your tools and adding new skills and
techniques. When I landed this gig in October last year, I knew that my basic
skills weren’t up to scratch. So I read the pro git book cover to cover, and
the vim bible, and a tmux primer, and a linux overview. Currently I’m working
through Understanding Cryptography. Next up is a book on Elliptic Curves, and
then a treatment of the automake system. I’ll also re-read some C++ text books
to remind myself of everything I’ve forgotten.

(aside: if you haven’t read the Pro Git and Practical Vim books, go out and do
that now. The time spent mastering git concepts like interactive rebase, rerere
and filter-branch, and making your vim life more efficient will repay the
invested time with interest)

I’ve also instigated a whitepaper Wednesday at work. Each week one of us will
read and present an interesting whitepaper or technical topic to the group.

The pace of technical innovation in Bitcoin is breakneck, so to be a useful
contributor and to be able to keep up with the latest developments we all need
to be constantly refreshing our skills and learning new concepts.

#### Offer help and ask for help

<img src="./help.jpeg" class="center-img">

I’m not the best C++ programmer, but thanks to my time with Pro Git, I’m pretty
handy with branches and commits. I’ve been able to help take load off
long-standing contributors by rebasing and tidying up PRs (eg
[here](https://github.com/bitcoin/bitcoin/pull/7729) and
[here](https://github.com/bitcoin/bitcoin/pull/10830)). If that frees up
their time to work on more important stuff, then it’s a useful contribution. At
the other end of the spectrum, there are first-time contributors who often trip
up over basic concepts like squashing commits and rebasing PRs. Spending a bit
of time helping those people is definitely a good use of time if it gets the PR
unblocked, and even more so if it encourages the contributor to come back and
contribute to the project again.

Conversely, I’ve been very happily surprised by the amount of help
long-standing bitcoin contributors have been prepared to give me and the time
they’ve spent teaching me things. I’m always blown away by how much time sipa
is prepared to spend teaching and explaining (take a look at [his Stack Exchange
profile](https://bitcoin.stackexchange.com/users/208/pieter-wuille) if you
don’t believe me). Cory Fields has also been extremely generous with his time,
explaining the build system to me even when I’ve had the most basic questions.
Matt Corallo, Suhas Daftuar and Alex Morcos deserve special mention for getting
me started on my Bitcoin developer journey in September last year and bringing
me up to speed on the code and how to be a useful contributor.

Bitcoin has an unfair reputation for being an unwelcoming environment for new
contributors. The one thing that all of the long-standing contributors share is
that they care deeply about the project. If you genuinely want to help, and are
respectful of their time, then most will be more than happy to share expertise
with you.

#### Be a contributor, not a developer

<img src="./castel.jpeg" class="center-img">

One part of being a useful contributor to an open source project is writing
good code, but there are many more: understanding what other people want from
the project and working in the same direction as them rather than against them;
enticing people to review and merge your PRs; making your communications in PRs
and reviews clear, convincing and respectful; structuring your PRs to make the
reviewers job easier; and cultivating good relationships with other
contributors are just some. Work on those skills. It’s no good writing awesome
code if it’s doing something that people don’t want in the project, or if you
can’t get anyone to review it. This is especially important if you’re a
newcomer and haven’t built up a reputation in the project — try to make it easy
for people to review and ACK your PRs and you’re more likely to get a good
response.

#### Interested?

My list isn’t complete and is no way prescriptive. Open source is a broad
church, and everyone contributes in their own way.

If you want a more practical primer on how to get started on contributing to
Bitcoin Core, Jimmy Song has written a [superb introduction](https://bitcointechtalk.com/a-gentle-introduction-to-bitcoin-core-development-fdc95eaee6b8).

Please reach out to me if have any thoughts or suggestions of your own, or if
you want help getting started. I’m always happy to help people get their first
commit merged!

_originally posted at [https://bitcointechtalk.com/](https://bitcointechtalk.com)_
