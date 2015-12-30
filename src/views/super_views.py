# -*- coding: utf-8 -*-
from utils.media_sender import UrlPrintSender
from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
import random
import config


class SuperViews(object):
    def __init__(self, interface_layer):
        self.interface_layer = interface_layer
        self.url_print_sender = UrlPrintSender(self.interface_layer)
        self.routes = [
            ("^" + config.cmd_prefix + "(?:help|ajuda)", self.help),
            ("^" + config.cmd_prefix + "(?:about|sobre)", self.about),
            ("^" + config.cmd_prefix + "(?:roll|dados)", self.roll),
            ("^" + config.cmd_prefix + "(?P<evenOrOdd>even|odd)$", self.even_or_odd),
        ]

    def about(self, message=None, match=None, to=None):
        self.url_print_sender.send_by_url(message.getFrom(), "https://github.com/joaoricardo000/whatsapp-bot-seed", ABOUT_TEXT)

    def roll(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity("[%d]" % random.randint(1, 6), to=message.getFrom())

    def even_or_odd(self, message=None, match=None, to=None):
        is_odd = len(match.group("evenOrOdd")) % 2
        num = random.randint(1, 10)
        if (is_odd and num % 2) or (not is_odd and not num % 2):
            return TextMessageProtocolEntity("[%d]\nYou win." % num, to=message.getFrom())
        else:
            return TextMessageProtocolEntity("[%d]\nYou lose!" % num, to=message.getFrom())

    def help(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity(HELP_TEXT, to=message.getFrom())


HELP_TEXT = """ [HELP]
- Commands
/ajuda - Mostra esta mensagem
/tempo [cidade] - Meteorologia
/previsao [cidade] - Previsão do tempo
/s(earch) [keyword] - Tira um screenshot do 1º resultado do Google
/dados - Lança os dados

Funções automáticas:
- Url (http://...) - Envia um screenshot do url
- Url de imagem (jpeg, gif, png) - Envia a imagem
- Url de video (mp4, webm, youtube) - Envia o video
"""

INACTIVE = """
/i(mage) [keyword] - I'm lucky with image!
/t(ts) - Text to speech.
"""

ABOUT_TEXT = """ [Whatsapp Bot Seed]
A small open source python framework to create a whatsapp bot, with regex-callback message routing.
https://github.com/joaoricardo000/whatsapp-bot-seed
"""
