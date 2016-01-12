# -*- coding: utf-8 -*-
from utils.grammar_dict import grammar
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import string


class GrammarViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            ('^.*?$', self.nazi)
        ]

    def nazi(self, message, match):
        msg = ''.join([s.translate(None, string.punctuation) for s in message.getBody()]).split()

        for w in msg:
            if grammar.get(w):
                if w in msg:
                    response = 'Did you mean %s?' % grammar.get(w)
                    return TextMessageProtocolEntity(response, to=message.getFrom())
