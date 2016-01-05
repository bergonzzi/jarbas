# -*- coding: utf-8 -*-
import re

vai = re.compile('^jarbas'
                 '.*?vai.*?('
                 '?:caralho|'
                 'merda|'
                 'puta.*?pariu|'
                 'levar.*?(?:cu|cú)|'
                 'foder'
                 ').*$', re.IGNORECASE)

youare = re.compile(
                    '^jarbas'
                    '.*?('
                    'cabr(?:a|ã)o|'
                    'porco|'
                    'fdp|'
                    'filh(?:o|a)(?:\s|-)d(?:a|e)(?:\s|-)puta|'
                    'homossexual|'
                    'bich(on)?a|'
                    'abichanado|'
                    'panasc((a|ã)o|a)|'
                    'paneleiro|'
                    'rabeta|'
                    'roto|'
                    'panilas|'
                    'froxo|'
                    'maricas|'
                    'gay(?:zola(?:s)?)?|'
                    'fufa|'
                    'caralho(?:te)?|'
                    'anormal|'
                    'est(?:u|ú)pido|'
                    'parv(o|inho|alh(?:a|ã)o)|'
                    'idiota|'
                    'asno|'
                    'anta|'
                    'burro|'
                    'merda|'
                    'c(?:ó|o)c(?:ó|o)'
                    ').*$', re.IGNORECASE)

print '\nTestes "vai para...":\n--------------------------'
print re.match(vai, 'jarbas vai po caralho').group()
print re.match(vai, 'jarbas vai à merda').group()
print re.match(vai, 'jarbas vai para a puta que te pariu').group()
print re.match(vai, 'jarbas vai levar no cú').group()
print re.match(vai, 'jarbas, vai levar no cu seu paneleiro').group()
print re.match(vai, 'jarbas vai-te foder').group()

print '\nTestes "és um...":\n--------------------------'
print re.match(youare, 'jarbas es um cabrão').group(1) + ' és tu!'
print re.match(youare, 'jarbas, seu paneleiro').group(1) + ' és tu!'
print re.match(youare, 'jarbas és mesmo anormal!').group(1) + ' és tu!'
print re.match(youare, 'jarbas seu parvalhão!').group(1) + ' és tu!'
print re.match(youare, 'jarbas meu grande fdp!').group(1) + ' és tu!'
print re.match(youare, 'jarbas meu grande filha da puta!').group(1) + ' és tu!'
print re.match(youare, 'jarbas meu gayzolas').group(1) + ' és tu!'
print re.match(youare, 'jarbas meu panascão').group(1) + ' és tu!'
