#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://fakedrake.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing


GOOGLE_ANALYTICS_TRACKING_ID = 'UA-44345210-1'
GOOGLE_ANALYTICS_URL = "fakedrake.github.io"

DISQUS_SITENAME = "drninjabatman-blog"
SITEURL_DISQUS = 'http://fakedrake.github.io'
