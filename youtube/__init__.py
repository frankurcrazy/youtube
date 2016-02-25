#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Frank Chang

import requests
from requests.compat import urljoin
from lxml import html
from urllib import quote_plus
import json

class YouTubeResult(object):
    def __init__(self, title, desc, link, likes, dislikes, shorten):
        self._title = title
        self._desc = desc
        self._link = link
        self._likes = likes
        self._dislikes = dislikes
        self._shorten = shorten

    def __repr__(self):
        return u"<Result title=\"{title}\" link=\"{link}\" desc=\"{desc}\" likes={likes} dislikes={dislikes}>".format(title=self._title, link=self._shorten, desc=self._desc, likes=self._likes, dislikes=self._dislikes).encode('utf-8')
class YouTube(object):
    youtube_url = "https://www.youtube.com"

    def __init__(self):
        pass

    def __getinfo(self, link):
        req = requests.get(link)
        span = html.fromstring(req.text).xpath('//span[@class="like-button-renderer "]')[0]
        likes = span.xpath('(.//span[@class="yt-uix-button-content"])[1]/text()')[0]
        dislikes = span.xpath('(.//span[@class="yt-uix-button-content"])[4]/text()')[0]
        return {'likes': likes, 'dislikes': dislikes}

    def __shorten(self, link):
        req = requests.get("https://developer.url.fit/api/shorten?long_url={}".format(quote_plus(link)))
        link = urljoin("http://url.fit", (json.loads(req.text))['url'])
        return link

    def search(self, keyword, **kwargs):
        if (len(keyword) == 0): return None
        else:
            var = {
                'keyword': quote_plus(keyword),
                'page': 1 if 'page' not in kwargs else kwargs['page'],
            }
            req = requests.get("https://www.youtube.com/results?search_query={keyword}&page={page}".format(**var))
            result = []
            for c in html.fromstring(req.text).xpath('//div[@class="yt-lockup-content"]'):
                params = {}
                params['title'] = c.xpath("./h3[@class='yt-lockup-title ']/a/text()")[0]
                params['link'] = urljoin(self.youtube_url, \
                           c.xpath("./h3[@class='yt-lockup-title ']/a/@href")[0])
                if 'watch' not in params['link']: continue
                desc = c.xpath("./div[@class='yt-lockup-description yt-ui-ellipsis yt-ui-ellipsis-2']/text()")
                if len(desc) > 0:
                    params['desc'] = u"\n".join(desc)
                else:
                    params['desc'] = None

                info = self.__getinfo(params['link'])
                params.update(info)
                params['shorten'] = self.__shorten(params['link'])
                result += [YouTubeResult(**params)]
            return result

def search(keyword, **kwargs):
    youtube = YouTube()
    r = youtube.search(keyword, **kwargs)
    for result in r:
        print result

