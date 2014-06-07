title: Programmatically add search engines to firefox
date: 2014-06-07 15:21
tags: firefox, javascript
category: firefox
slug: programmatically-add-search-engines-to-firefox
author: Chris Perivolaropoulos
status: draft
summary:

_This article is hidden. Remove status: hidden or make it status:
published to be able to publish_

First of all let;s see what we can find out without looking at code.

	:::console
	(py)fakedrake@monolith ~/.mozilla/firefox/gsz5q06m.default $ find -name "*search*"
	./search-metadata.json
	./search.json
	./searchplugins

*search.json* has some general info about the engines and seems to be
 pointing firefox to *searchplugins/* for more details.

	:::console
	(py)fakedrake@monolith ~/.mozilla/firefox/gsz5q06m.default $ ls searchplugins
	duckduckgo.xml  imdb.xml  spotify1.xml  youtube.xml

Right what I was looking for. Let's take a look inside one of them

	:::xml
	<SearchPlugin xmlns="http://www.mozilla.org/2006/browser/search/" xmlns:os="http://a9.com/-/spec/opensearch/1.1/">
	<os:ShortName>DuckDuckGo</os:ShortName>
	<os:Description>Search DuckDuckGo</os:Description>
	<os:InputEncoding>UTF-8</os:InputEncoding>
	<os:Image width="16" height="16">data:image/x-icon;base64,AAABAAMAEBAAAA[...]</os:Image>
	<os:Url type="text/html" method="GET" template="https://duckduckgo.com/">
	  <os:Param name="q" value="{searchTerms}"/>
	</os:Url><os:Url type="application/x-suggestions+json" method="GET" template="https://duckduckgo.com/ac/">
	  <os:Param name="q" value="{searchTerms}"/>
	  <os:Param name="type" value="list"/>
	</os:Url>
	</SearchPlugin>

Awesome, now lets see what interfaces we can get to loading this
code. We will need access to the
[search service](https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM/Reference/Interface/nsIBrowserSearchService), so

	:::javascript
	var bss = Cc["@mozilla.org/browser/search-service;1"].getService(Ci.nsIBrowserSearchService)

Now to me at least the documentation was not extremely obvious so I
had to check out the
[implementation](https://github.com/mozilla/gecko-dev/blob/master/toolkit/components/search/nsSearchService.js)
which I encourage you to take a look at but it wont be really
necessary. After snooping around a bit I came up with.

	:::javascript
	bss.addEngine("file:///home/fakedrake/Projects/Javascript/spotify.xml", Ci.nsISearchEngine.DATA_XML, null, null)

Where the contents of *spotify.xml* are

	:::xml
	<SearchPlugin xmlns="http://www.mozilla.org/2006/browser/search/" xmlns:os="http://a9.com/-/spec/opensearch/1.1/">
	<os:ShortName>Spotify</os:ShortName>
	<os:Description>Search Spotify</os:Description>
	<os:InputEncoding>UTF-8</os:InputEncoding>
	<os:Url type="text/html" method="GET" template="https://play.spotify.com/search/{searchTerms}"/>
	</SearchPlugin>


And to my delight vimperator recognizes my custom spotify search engine!

![Spoify search engine](http://i.imgur.com/yukAwWr.png)

And not only that, but firefox was kind enough to add my xml to the
right place so it is permanent.

	:::console
	(py)fakedrake@monolith ~/.mozilla/firefox/gsz5q06m.default/searchplugins $ ls
	duckduckgo.xml  imdb.xml  spotify.xml  youtube.xml

Now if you need more direct control over this. An equivalent to the
above would be:

	:::javascript
	bss.addEngineWithDetails("Spotify",null, "spot", "Search spotify", "GET", "https://play.spotify.com/search/{searchTerms}")

This does exactly the same thing as having the data in an XML file and
loading it with `add Engine()`. If you want to remove an engine you
can do it with:

	:::javascript
	bss.removeEngine(bss.getEngineByAlias("spot"))
