#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Perivolaropoulos'
SITENAME = u'Batman Ph.D'
SITEURL = ''

TIMEZONE = 'Europe/Athens'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS =  (('Think Silicon Ltd', 'http://think-silicon.com/'),
          ('P-Space', 'http://p-space.gr'),
          ('START', 'http://start.mit.edu'),
          ('CSAIL MiT', 'http://www.csail.mit.edu'),
)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/drNinjaBatman'),
          ('github', 'https://github.com/fakedrake'),
          ('facebook', 'https://www.facebook.com/chris.perivolaropoulos'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "theme/"
BG_IMG = "https://exposure-2.imgix.net/production/photos/z8ilyalf54su4n291ozw4xvep8s0dx6rgvdi/original.jpg"
LOGO_IMG = "http://imgur.com/KyLzuoW.png"
SITESUBTITLE = "Procrastinating and nose picking since 1991"
EXTRA_COPYRIGHTS = "Photos by <a href=\"https://marianasioti.exposure.so/\">Maria Nasioti</a>"
PERSONAL_PHOTO = "http://i60.tinypic.com/2uesocp.jpg"
PERSONAL_INFO = """A flea lost in the haze of existential insanity. In between
procrastination sessions I may write some code too.
"""

FAVICON = "/theme/img/favicon.png"

WORK_DESCRIPTION = """On the thin line between hacking and engineering."""
TS_JOB_DESCRIPTION = """At Think-Silicon we build awesome GPUs for mobile devices."""
START_JOB_DESCRIPTION = """START is a system developed by CSAIL's InfoLab that aims to
accurately answer natural language questions. Working the wikipedia
backend."""

# work_type, work_cover_link, work_cover_style, work_title, work_description, work_link
WORK_LIST = [("http://i57.tinypic.com/2rnd9g8.png", "",
     "Software Engineer at Think-Silicon Ltd.",
     TS_JOB_DESCRIPTION, "http://www.think-silicon.com"),
    (
     "http://img2.wikia.nocookie.net/__cb20111105140719/how-i-met-your-mother/de/images/1/12/Wikipedia.png",
     "width:70%; height:70%; text-align: center; margin: 0 auto", "CSAIL's START Wikipedia backend", START_JOB_DESCRIPTION,
     "http://start.mit.edu"),
]
