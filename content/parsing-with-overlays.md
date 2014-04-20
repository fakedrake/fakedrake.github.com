title: Parsing with overlays
date: 2014-04-14 22:17
tags: python, nlp, parsing
category: python
slug: parsing-with-overlays
author: Chris Perivolaropoulos
status: hidden
summary: Findin patterns in free text is is one of those things that
most of the time there is no right answer as to how to do it. Here is
how I pull dates out of wikipedia.

So I was faced with the task of finding dates and date ranges in free
text. It sounded like a straightforward problem so I expected that
many many people have solved it before me. And they have. Well not
'many many' but there is [dateutil] and some other less popular
solutions, all of which however failed miserably on dates before epoch
(1/1/1970). Mourning the hours I spent trying to monkey-patch dateutil
into working with BC dates I decided I had to man up and write my own
parser. My first attempt to it was to build regular expressions
incrementally by sewing regular expressions together. That worked for
the simplest of cases but it was ugly, unmaintainable and worst of all
when the time came after a couple of days to put some more date
templates everything went to hell.

So I decided to build a smarter system, still based on regex, but
being able to handle the complexity of the task in a straightforward
way. My number one goal was simplicity and I think I did quite well,
so here is the basic idea.

The
