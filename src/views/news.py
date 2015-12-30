# -*- coding: utf-8 -*-
import feedparser
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from pyshorteners import Shortener
import config



class NewsViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # Current weather
            ("^" + config.cmd_prefix + "(?:ultimas|últimas)$", self.get_latest_news),
        ]

    def get_latest_news(self, message, match):
        url = 'http://feeds.feedburner.com/PublicoRSS?format=xml'
        feed = feedparser.parse(url)
        titles = []

        shortener = Shortener('IsgdShortener')

        for i, t in enumerate(feed['entries']):
            line = "%d. %s - %s\n" % (i + 1, t['title'], shortener.short(t['link']))
            titles.append(line.encode('utf-8'))

        titles_formatted = '\n'.join(titles)

        return TextMessageProtocolEntity(titles_formatted, to=message.getFrom())
