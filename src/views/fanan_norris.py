# -*- coding: utf-8 -*-
import random
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.fanan_norris import fanan_quotes


class FananViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            (r'^.*?\b(fanan|fanã)\b.*?$', self.quote)
        ]

    def quote(self, message, match):
        msg = random.choice(fanan_quotes)
        return TextMessageProtocolEntity(msg, to=message.getFrom())
