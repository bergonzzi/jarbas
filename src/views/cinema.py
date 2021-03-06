# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.cinema_scraper import movies
import config


class CinemaViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            ('^' + config.cmd_prefix + '(?:cinemas?|filmes|sess(?:o|õ)es)\s?(?P<cinema>[^$]+)$', self.get_movies)
        ]

    def get_movies(self, message, match):
        arg = match.group('cinema').lower()

        if arg in ('lista', 'list', 'ajuda', 'help', 'salas'):
            msg = 'Podes ver as sessões disponíveis em qualquer um destes cinemas (podes usar um nome mais curto, por ex. /cinema alegro):\n\n'

            for k, v in config.cinema_sources.iteritems():
                msg += v['name'] + '\n'
        else:
            msg = movies(arg)

        return TextMessageProtocolEntity(msg, to=message.getFrom())
