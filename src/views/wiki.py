# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import requests
import config


class WikiViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            ('^' + config.cmd_prefix + '(?:w|wiki|wikipedoa)\s(?P<term>[^$]+)$', self.wiki)
        ]

    def wiki(self, message, match):
        term = match.group('term')
        url = 'https://en.wikipedia.org/w/api.php?' \
              'format=json&' \
              'action=query&' \
              'prop=extracts|info&' \
              'inprop=url&' \
              'exintro=&' \
              'explaintext=&' \
              'redirects=&' \
              'exchars=500&' \
              'titles=%s' % term
        r = requests.get(url).json()
        msg = ''

        for k, v in r.iteritems():
            if k == 'query':
                for x, y in v['pages'].iteritems():
                    title = y['title'].encode('utf-8')
                    url = y['fullurl'].encode('utf-8')
                    extract = y['extract'].encode('utf-8')
                    msg = '{title}\n{url}\n\n{extract}'.format(title=title, url=url, extract=extract)

        return TextMessageProtocolEntity(msg, to=message.getFrom())
