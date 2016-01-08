# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import config


class ChatViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # Greetings
            ('^(' + config.bot_name + ')[\s,-](?:'
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
             ')[\s,-](' + config.bot_name + ').*$', self.greet),

            # "Vai-te" offenses
            ('^' + config.bot_name +
             '[\s,-](?:vai|p(?:o|ó)|p(?:a|á)|para).*?(?:'
             'caralho|'
             'merda|'
             'puta.*?pariu|'
             'levar.*?(?:cu|cú)|'
             'foder'
             ').*$', self.go_to),

            # "You are a" offenses
            ('^' + config.bot_name +
             '[\s,-](?:es|és).*?(?P<what>'
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
             'caralh(?:ote|inho|ito)?|'
             'colh(?:a|ã)o|'
             'anormal|'
             'est(?:u|ú)pido|'
             'parv(o|inho|alh(?:a|ã)o)|'
             'idiota|'
             'asno|'
             'anta|'
             'burr(?:o|inho|ito)|'
             'merda|'
             'c(?:ó|o)c(?:ó|o)|'
             'azeiteiro|'
             'bimbo|'
             '(x|ch)unga|'
             'imbecil|'
             '(e|i)nerg(ú|u)men(o|e)|'
             'b(á|a)sico'
             ').*$', self.you_are),

            # "Faz-me" offenses
            ('^' + config.bot_name +
             '[\s,-](?:faz|chupa|mama|lambe|esfrega|massaja).*?(?:'
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
             'bola(?:s)?|'
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
             'marmelo(s)?'
             ').*$', self.make_me),

            # Compliments
            # Hardcoded bot name, for some reason can't concatenate vars in this pattern
            (r'^(?=.*\bjarbas\b)(?=.*\b(fixe|espectacular|fant(á|a)stico|extraordin(á|a)rio|magn(í|i)fico|inteligente|esperto|amigo|amig(á|a)vel|elegante|brutal|bom|perfeito|(ó|o)ptimo|am(á|a)vel|grande|generoso|(ú|u)nico|precioso|bonito|lindo|forte|belo|f(á|a)cil|especial|brilhante|estonteante|(ú|u)til|agrad(á|a)vel|simp(á|a)tico)).*$', self.thanks)
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

    def thanks(self, message, match):
        op = message.getNotify()
        # what = match.group(1).lower().decode('utf-8')
        # msg = u'%s, obrigado, tu também és %s' % (op, what)
        msg = 'Obrigado %s!' % op
        return TextMessageProtocolEntity(msg, to=message.getFrom())
