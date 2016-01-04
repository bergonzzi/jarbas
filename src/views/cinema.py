# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.cinema_scraper import movies
import config


class CinemaViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            ('^' + config.cmd_prefix + '(?:cinemas?|filmes)\s?(?P<cinema>[^$]+)$', self.get_movies)
        ]

    def get_movies(self, message, match):
        cinema = match.group('cinema').lower()
        return TextMessageProtocolEntity(movies(cinema), to=message.getFrom())
