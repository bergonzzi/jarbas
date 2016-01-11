# -*- coding: utf-8 -*-
from utils.media_sender import UrlPrintSender
from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
import random
import config
import emoji


class SuperViews(object):
    def __init__(self, interface_layer):
        self.interface_layer = interface_layer
        self.url_print_sender = UrlPrintSender(self.interface_layer)
        self.routes = [
            ("^" + config.cmd_prefix + "(?:help|ajuda)", self.help),
            ("^" + config.cmd_prefix + "(?:about|sobre)", self.about),
            ("^" + config.cmd_prefix + "(?:roll|dado(?:s)?)", self.roll),
            ("^" + config.cmd_prefix + "(?P<evenodd>even|odd)$", self.even_or_odd),
            ("^" + config.cmd_prefix + "(moeda(?:s)?|coin(?:s)?)\s(?P<moeda>cara|coroa)+$", self.coin),
        ]

    def about(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity(ABOUT_TEXT, to=message.getFrom())

    def roll(self, message=None, match=None, to=None):
        msg = emoji.emojize(':game_die:... %d' % random.randint(1, 6))
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def even_or_odd(self, message=None, match=None, to=None):
        is_odd = len(match.group("evenodd")) % 2
        num = random.randint(1, 10)
        if (is_odd and num % 2) or (not is_odd and not num % 2):
            return TextMessageProtocolEntity("%d - You win." % num, to=message.getFrom())
        else:
            return TextMessageProtocolEntity("%d - You lose!" % num, to=message.getFrom())

    def coin(self, message, match):
        op = message.getNotify().decode('utf-8')
        coins = ['cara', 'coroa']
        choice = match.group('moeda').lower()
        result = random.choice(coins)

        if result == choice:
            msg = emoji.emojize('%s, escolheste "%s" e saiu "%s", ganhaste! :grinning:' % (op, choice, result), use_aliases=True)
        else:
            msg = emoji.emojize('%s, escolheste "%s" mas saiu "%s", perdeste! :confused:' % (op, choice, result), use_aliases=True)

        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def help(self, message=None, match=None, to=None):
        return TextMessageProtocolEntity(HELP_TEXT.encode('utf-8'), to=message.getFrom())


HELP_TEXT = u"""Sou um \U0001F47E um bocado limitado, mas percebo estes comandos:

/ajuda - Mostra esta mensagem
/tempo cidade - Meteorologia
/previsao cidade - Previsão do tempo
/noticias (desporto) - Últimas notícias gerais ou desporto apenas
/cinema local - Sessões para o cinema escolhido
/cinema lista - Lista de cinemas disponíveis
/procurafilme filme - Procura de filmes
/filme título - Mostra resumo do filme
/url link - Envia um screenshot do site
/search pesquisa - Pesquisa no Google e envia o 1º resultado
/imagem pesquisa - Pesquisa imagens e envia o 1º resultado
/youtube link - Envia o video do youtube
/dados - Lança os dados
/moeda cara/coroa - Moeda ao ar

Funções automáticas:
- Url de imagem (jpg, gif, png) - Envia a imagem
- Url de video (mp4, webm) - Envia o video
- Url de gif - Envia o video
"""

ABOUT_TEXT = "Sou o bot Jarbas, o meu mestre é o André Bergonse e estou aqui principalmente para o servir."
