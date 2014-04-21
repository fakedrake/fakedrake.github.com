title: Dumping tab information with vimperator
date: 2014-04-20 20:18
tags: firefox, vimperator, javascript, tabs
category: firefox
slug: dumping-tab-information-with-vimperator
author: Chris Perivolaropoulos
summary: The unmatchable might of the firefox - vimperator combo weaved into dumping tabs into a file.

To me it is quite usual that I am looking at a list of links to things
(songs, articls, books etc.) and I want to first select the ones I am
interested in and then look into them one by one. Most of the time
this does not go as smoothly as I would want it to. I wildly
underestimate the length of the list and not only do I get many many
more interesting results than I expected, but I also spend so much
time going through the entire list that I need to check them later. I
could bookmark everything and look at it later but the perfect
solution would be to dump everything in a text file and
[gist](http://gist.github.com) it or then categorize it according to
artist with Python or something else equally and needlessly nerdy.

So anyway, turns out firefox welcomes this kind of thing if you are a
core developer and have deep knowledge of it's inter-workings or if
you have vimperator to abstract the interface/service
inconvenience. And the matter is actually very simple.

    :::js
	tabdump = "";
	tabs.get().forEach(function (i) { tabdump += i.join(" ~~~ ") + \n; });
	io.File("~/Documents/tabs").write(tabdump)

If you haven't got any better way of running more than one line of
code on firefox you can use vimperator's `:js` which should go like

    :::js
	:js tabdump = ""; tabs.get().forEach(function (i) { tabdump += i.join(" ~~~ ") + \n; }); io.File("~/Documents/tabs").write(tabdump)


So in brief what does this code do, it uses vimperator's interface to
tabs to get a list of all tabs (basically tuples) and then you
concatenate those tuples together and dump them into a string (line
2). Then vimperator provides a simple way of file io with `io.File` to
throw everything into a file. And there you have it

If for example I were looking up bands going through a list and run
the above I would come up with something like

	[...]

	23 ~~~ kyuss at DuckDuckGo ~~~ https://duckduckgo.com/?q=kyuss
	24 ~~~ 311 at DuckDuckGo ~~~ https://duckduckgo.com/?q=311
	25 ~~~ high on fire at DuckDuckGo ~~~ https://duckduckgo.com/?q=high+on+fire
	26 ~~~ sleep at DuckDuckGo ~~~ https://duckduckgo.com/?q=sleep
	27 ~~~ cottonmouth kings at DuckDuckGo ~~~ https://duckduckgo.com/?q=cottonmouth+kings

	[...]

_EDIT_: If you want to reopen some of those you can easily do it with

    :::js
	:js lines = io.File("~/Documents/tabs").read().split("\n")
	:js lines.map(function (l) {return l.split(" ~~~ ")[2]}).slice(7,23).forEach(function (url) {liberator.open(url, {where: liberator.NEW_TAB})})

Which should open again tabs 7 to 22.
