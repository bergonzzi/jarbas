# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity


class ChatViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # "Vai-te" offenses
            ('^jarbas'
             '.*?vai.*?(?:'
             'caralho|'
             'merda|'
             'puta.*?pariu|'
             'levar.*?(?:cu|cú)|'
             'foder'
             ').*$', self.go_to),

            # "You are a" offenses
            ('^jarbas'
             '.*?(?:es|és).*?(?P<what>'
             'cabr(?:a|ã)o|'
             'porco|'
             'fdp|'
             'filh(?:o|a)(?:\s|-)d(?:a|e)(?:\s|-)puta|'
             'homossexual|'
             'bich(on)?a|'
             'abichanado|'
             'panasc((a|ã)o|a)|'
             'panisga|'
             'panuco|'
             'paneleiro|'
             'rab(?:eta|o)|'
             'rabolho|'
             'roto|'
             'panilas|'
             'froxo|'
             'maricas|'
             'gay(?:zola(?:s)?)?|'
             'boiola|'
             'larilas|'
             'veado|'
             'l(?:e|é)sbica'
             'fufa|'
             'caralho(?:te)?|'
             'colh(?:a|ã)o|'
             'anormal|'
             'est(?:u|ú)pido|'
             'parv(o|inho|alh(?:a|ã)o)|'
             'idiota|'
             'asno|'
             'anta|'
             'burro|'
             'merda|'
             'c(?:ó|o)c(?:ó|o)'
             ').*$', self.you_are),

            # "Faz-me" offenses
            ('^jarbas'
             '.*?(?:faz|chupa|mama|lambe|esfrega|massaja).*?(?:'
             'broche|'
             'bico|'
             'mamada|'
             'minete|'
             'caralho|'
             'mastro|'
             'pau|'
             'pi(?:ch|x|ss|c|ç)(?:a|o|ota)|'
             'bacamarte|'
             'mars(?:a|á)pio|'
             'verga(?:lho)?|'
             'cacete|'
             'besugo|'
             'bola(s)?|'
             'colh(?:o|õ)es|'
             'tomate(s)?|'
             'test(?:i|í)culos|'
             'escroto|'
             'saco|'
             'carpete|'
             'cona(ssa|ça|ca)?|'
             'coninha|'
             'crica|'
             'pito|'
             'rata|'
             'entrefolho(s)?|'
             'pa(?:ch|x)a(?:ch|x)a|'
             'passarinha|'
             'patareca|'
             'b(?:o|u)ceta|'
             'seio(s)?|'
             'teta(s)?|'
             'tetinha(s)?|'
             'mama(s)?|'
             'marmelo(s)?|'
             ').*$', self.make_me),
        ]

    def go_to(self, message, match):
        op = message.getNotify()
        msg = '%s, vai tu!' % op
        return TextMessageProtocolEntity(msg, to=message.getFrom())

    def you_are(self, message, match):
        op = message.getNotify()
        what = match.group('what').lower()
        msg = '%s, %s és tu!' % (op, what)
        return TextMessageProtocolEntity(msg, to=message.getFrom())

    def make_me(self, message, match):
        op = message.getNotify()
        msg = '%s, mas que falta de educação, eu não faço essas coisas!' % op
        return TextMessageProtocolEntity(msg, to=message.getFrom())

