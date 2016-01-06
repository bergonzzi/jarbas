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
        return TextMessageProtocolEntity(ABOUT_TEXT, to=message.getFrom())

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


HELP_TEXT = """Sou um bot um bocado limitado, mas percebo estes comandos:

/ajuda - Mostra esta mensagem
/tempo [cidade] - Meteorologia
/previsao [cidade] - Previsão do tempo
/cinema [local] - Sessões para o cinema escolhido
/cinema lista - Lista de cinemas disponíveis
/search [pesquisa] - Pesquisa no Google e envia o 1º resultado
/youtube [link] - Envia o video do youtube
/dados - Lança os dados

Funções automáticas:
- Url (http://...) - Envia um screenshot do url
- Url de imagem (jpg, gif, png) - Envia a imagem
- Url de video (mp4, webm, youtube) - Envia o video
"""

ABOUT_TEXT = "Sou o Jarbas, o meu mestre é o André Bergonse e estou aqui para te servir."
