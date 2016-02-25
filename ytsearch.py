#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: ytsearch.py
# author: Frank Chang <frank@csie.io>

import youtube
import sys

from youtube import YouTube

youtube.search(sys.argv[1])

