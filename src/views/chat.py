# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import config


class ChatViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # Greetings
            ('^(' + config.bot_name + ').*?(?:'
             'ol(?:á|a)|'
             'oi|'
             'boas|'
             'bom dia|'
             'boa tarde|'
             'boa(?:s)? noite(?:s)?|'
             '(?:tudo|td) (b(?:e|o)m|fixe)|'
             '(?:como|cm) vais'
             ').*$', self.greet),

            ('^(?:'
             'ol(?:á|a)|'
             'oi|'
             'boas|'
             'bom dia|'
             'boa tarde|'
             'boa(?:s)? noite(?:s)?|'
             '(?:tudo|td) (b(?:e|o)m|fixe)|'
             '(?:como|cm) vais'
             ')(\s' + config.bot_name + ').*$', self.greet),

            # "Vai-te" offenses
            ('^' + config.bot_name +
             '.*?vai.*?(?:'
             'caralho|'
             'merda|'
             'puta.*?pariu|'
             'levar.*?(?:cu|cú)|'
             'foder'
             ').*$', self.go_to),

            # "You are a" offenses
            ('^' + config.bot_name +
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
            ('^' + config.bot_name +
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
        op = message.getNotify().decode('utf-8')
        msg = u'%s, vai tu! \U0001F595' % op
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def you_are(self, message, match):
        op = message.getNotify().decode('utf-8')
        what = match.group('what').lower().decode('utf-8')
        msg = u'%s, %s és tu!  \U0001F595' % (op, what)
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def make_me(self, message, match):
        op = message.getNotify()
        msg = '%s, mas que falta de educação, eu não faço essas coisas!' % op
        return TextMessageProtocolEntity(msg, to=message.getFrom())

    def greet(self, message, match):
        op = message.getNotify().decode('utf-8')
        msg = u'Ola %s! Se precisares de ajuda escreve /ajuda para ver uma lista de comandos \U0001F603' % op
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())
