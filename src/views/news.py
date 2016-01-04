# -*- coding: utf-8 -*-
import feedparser
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from pyshorteners import Shortener
import config


class NewsViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # Latest news
            ('^' + config.cmd_prefix + '(?:ultimas|últimas|noticias|notícias|news)\s?(?P<cat>[^$]+)?$', self.get_latest_news),
        ]

    def get_latest_news(self, message, match):
        try:
            cat = match.group('cat').lower()

            if cat in('desporto', 'sport', 'o jogo', 'ojogo', 'jogo'):
                src = 'O Jogo'
            elif cat in('jn', 'jornal de notícias', 'jornal de noticias', 'jornal noticias', 'jornal notícias'):
                src = 'Jornal de Notícias'
            else:
                src = 'Público'
        except AttributeError:
            src = 'Público'

        news_src = config.news_sources[src]
        feed = feedparser.parse(news_src)
        titles = []
        intro = 'As últimas do "%s":\n\n' % src

        shortener = Shortener('IsgdShortener')

        for i, t in enumerate(feed['entries']):
            num = i + 1
            title = t['title']
            link = shortener.short(t['link'])
            category = t['category']

            if i < config.max_news:
                line = '%d. %s - %s [%s]\n' % (num, title, link, category)
                titles.append(line.encode('utf-8'))

        titles_formatted = intro + '\n'.join(titles)

        return TextMessageProtocolEntity(titles_formatted, to=message.getFrom())
