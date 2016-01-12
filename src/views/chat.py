# -*- coding: utf-8 -*-
import random
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import config
import emoji


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
             '.*?(?:es|és|continuas|sejas|foste|eras|fosses).*?(?P<what>'
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
             '.*?(?:faz|chupa|mama|lambe|esfrega|massaja).*?(?P<what>'
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
            (r'^(?=.*\bjarbas\b)(?=.*\b(maior|fixe|porreiro|espectacular|fant(á|a)stico|extraordin(á|a)rio|magn(í|i)fico|inteligente|esperto|amigo|amig(á|a)vel|elegante|brutal|bom|perfeito|(ó|o)ptimo|am(á|a)vel|grande|generoso|(ú|u)nico|precioso|bonito|lindo|forte|belo|especial|brilhante|estonteante|(ú|u)til|agrad(á|a)vel|simp(á|a)tico)).*$', self.thanks),

            # Others
            (r'^(?=.*\bqual\b)(?=.*\bsignificado\b(?=.*\bvida)).*$', self.meaning_life)
        ]

    def go_to(self, message, match):
        op = message.getNotify().decode('utf-8')
        msg = emoji.emojize(u'%s, vai tu! :reversed_hand_with_middle_finger_extended:' % op)
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def you_are(self, message, match):
        op = message.getNotify().decode('utf-8')
        what = match.group('what').lower().decode('utf-8')
        msg = emoji.emojize(u'%s, %s és tu! :reversed_hand_with_middle_finger_extended:' % (op, what))
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def make_me(self, message, match):
        op = message.getNotify().decode('utf-8')
        what = match.group('what').lower()
        answers = [
            'Mas que falta de educação %s, eu não faço essas coisas!' % op,
            '%s? Onde é que aprendeste isso?' % what.capitalize(),
            'Que classe %s... que classe!' % op,
            'Acho que o meu mestre não gostar disso %s!' % op,
            '%s, só pensas em %s, queres falar sobre isso?' % (op, what),
            '%s, é isso que esperas de um bot?' % op
        ]
        msg = random.choice(answers)
        return TextMessageProtocolEntity(msg, to=message.getFrom())

    def greet(self, message, match):
        op = message.getNotify().decode('utf-8')
        msg = emoji.emojize(u'Ola %s! Se precisares de ajuda escreve /ajuda para ver uma lista de comandos :smiley:' % op, use_aliases=True)
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def thanks(self, message, match):
        op = message.getNotify().decode('utf-8')
        what = match.group(1).lower()
        answers = [
            u'Obrigado %s, às vezes também és %s :blush:' % (op, what),
            u'Obrigado %s (mas sabes que sou um bot não sabes?) :blush:' % op,
            u'Até me fazes corar %s, afinal sabes dizer coisas bonitas :blush:' % op,
            u'Se não fosse um bot também podia sentir isso por ti %s :blush:' % op,
            u'Obrigado %s, embora já soubesse :blush:' % op,
            u'Obrigado %s, se dissesses isso mais vezes talvez as pessoas gostassem mais de ti :blush:' % op,
        ]
        msg = emoji.emojize(random.choice(answers), use_aliases=True)
        return TextMessageProtocolEntity(msg.encode('utf-8'), to=message.getFrom())

    def meaning_life(self, message, match):
        msg = '42'
        return TextMessageProtocolEntity(msg, to=message.getFrom())
