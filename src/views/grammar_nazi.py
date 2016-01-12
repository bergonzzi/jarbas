# -*- coding: utf-8 -*-
from utils.grammar_dict import grammar
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import emoji
import logging


class GrammarViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            ('^.*?$', self.nazi)
        ]

    def nazi(self, message, match):
        op = message.getNotify().decode('utf-8')

        # Same as string punctuation only without dashes since those are important
        symbols = '!#$%&\()*+,./:;<=>?@[\\]^_`{|}~'
        punctuation = symbols + "'" + '"'

        msg = ''.join([s.translate(None, punctuation) for s in message.getBody()]).split()

        for w in msg:
            if grammar.get(w) and w in msg:
                response = u'%s, foste apanhado pelo Grammar Nazi! :smiling_face_with_horns: Querias dizer "%s"?' % (op, grammar.get(w).decode('utf-8'))

                # Log message request here only if there's a match with the grammar dict
                if message.isGroupMessage():
                    logging.info("(GROUP)[%s]-[%s] [grammar nazi]\t%s" % (message.getParticipant(), message.getFrom(), message.getBody()))
                else:
                    logging.info("(PVT)[%s] [grammar nazi]\t%s" % (message.getFrom(), message.getBody()))

                return TextMessageProtocolEntity(emoji.emojize(response).encode('utf-8'), to=message.getFrom())
