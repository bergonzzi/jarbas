# -*- coding: utf-8 -*-
from __future__ import division
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from xml.etree import ElementTree as ET
import requests
import config


class CurrencyViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            ("^" + config.cmd_prefix + "(?:cambio|câmbio|rate)\s(?P<code>[^$]+)(\?)?$", self.get_rate)
        ]

        self.rates = {
            'USD': {'rate': 0, 'country': 'Estados Unidos', 'name': 'Dólar dos Estados Unidos', 'symbol': '$', 'synonyms': ''},
            'IDR': {'rate': 0, 'country': 'Indonésia', 'name': 'Rupia indonésia', 'symbol': 'Rp', 'synonyms': ''},
            'BGN': {'rate': 0, 'country': 'Bulgária', 'name': 'Lev búlgaro', 'symbol': 'лв', 'synonyms': ''},
            'ILS': {'rate': 0, 'country': 'Israel', 'name': 'Novo siclo israelita', 'symbol': '₪', 'synonyms': ''},
            'GBP': {'rate': 0, 'country': 'Reino Unido', 'name': 'Libra esterlina', 'symbol': '£', 'synonyms': ''},
            'DKK': {'rate': 0, 'country': 'Dinamarca', 'name': 'Coroa dinamarquesa', 'symbol': 'kr', 'synonyms': ''},
            'CAD': {'rate': 0, 'country': 'Canadá', 'name': 'Dólar canadiano', 'symbol': '$', 'synonyms': ''},
            'MXN': {'rate': 0, 'country': 'México', 'name': 'Peso mexicano', 'symbol': '$', 'synonyms': ''},
            'HUF': {'rate': 0, 'country': 'Hungria', 'name': 'Florim húngaro', 'symbol': 'Ft', 'synonyms': ''},
            'RON': {'rate': 0, 'country': 'Roménia', 'name': 'Leu romeno', 'symbol': 'lei', 'synonyms': ''},
            'MYR': {'rate': 0, 'country': 'Malásia', 'name': 'Ringuite malaio', 'symbol': 'RM', 'synonyms': ''},
            'SEK': {'rate': 0, 'country': 'Suécia', 'name': 'Coroa sueca', 'symbol': 'kr', 'synonyms': ''},
            'SGD': {'rate': 0, 'country': 'Singapura', 'name': 'Dólar de Singapura', 'symbol': '$', 'synonyms': ''},
            'HKD': {'rate': 0, 'country': 'Honguecongue', 'name': 'Dólar de Honguecongue', 'symbol': '$', 'synonyms': ''},
            'AUD': {'rate': 0, 'country': 'Austrália', 'name': 'Dólar australiano', 'symbol': '$', 'synonyms': ''},
            'CHF': {'rate': 0, 'country': 'Suíça', 'name': 'Franco suíço', 'symbol': 'Fr', 'synonyms': ''},
            'KRW': {'rate': 0, 'country': 'Coreia do Sul', 'name': 'Won sul-coreano', 'symbol': '₩', 'synonyms': ''},
            'CNY': {'rate': 0, 'country': 'China, República Popular da', 'name': 'Iuane chinês', 'symbol': '¥ ou 元', 'synonyms': ''},
            'TRY': {'rate': 0, 'country': 'Turquia', 'name': 'Lira turca', 'symbol': '', 'synonyms': ''},
            'HRK': {'rate': 0, 'country': 'Croácia', 'name': 'Kuna croata', 'symbol': 'kn', 'synonyms': ''},
            'NZD': {'rate': 0, 'country': 'Nova Zelândia', 'name': 'Dólar da Nova Zelândia', 'symbol': '$', 'synonyms': ''},
            'THB': {'rate': 0, 'country': 'Tailândia', 'name': 'Baht tailandês', 'symbol': '฿', 'synonyms': ''},
            'NOK': {'rate': 0, 'country': 'Noruega', 'name': 'Coroa norueguesa', 'symbol': 'kr', 'synonyms': ''},
            'RUB': {'rate': 0, 'country': 'Rússia', 'name': 'Rublo russo', 'symbol': 'руб.', 'synonyms': ''},
            'INR': {'rate': 0, 'country': 'Índia', 'name': 'Rupia indiana', 'symbol': '', 'synonyms': ''},
            'JPY': {'rate': 0, 'country': 'Japão', 'name': 'Iene japonês', 'symbol': '¥', 'synonyms': ''},
            'CZK': {'rate': 0, 'country': 'Checa, República', 'name': 'Coroa checa', 'symbol': 'Kč', 'synonyms': ''},
            'BRL': {'rate': 0, 'country': 'Brasil', 'name': 'Real brasileiro', 'symbol': 'R$', 'synonyms': ''},
            'PLN': {'rate': 0, 'country': 'Polónia', 'name': 'Zlóti polaco', 'symbol': 'zł', 'synonyms': ''},
            'PHP': {'rate': 0, 'country': 'Filipinas', 'name': 'Peso filipino', 'symbol': '₱', 'synonyms': ''},
            'ZAR': {'rate': 0, 'country': 'África do Sul', 'name': 'Rand sul-africano', 'symbol': 'R', 'synonyms': ''}
        }

    def update_rates(self):
        # With the help of:
        # http://stackoverflow.com/questions/17250660/how-to-parse-xml-file-from-european-central-bank-with-python
        r = requests.get('http://www.ecb.int/stats/eurofxref/eurofxref-daily.xml', stream=True)
        tree = ET.parse(r.raw)
        root = tree.getroot()
        namespaces = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}

        for cube in root.findall('.//ex:Cube[@currency]', namespaces=namespaces):
            self.rates[cube.attrib['currency']]['rate'] = float(cube.attrib['rate'])

    def get_rate(self, message, match):
        self.update_rates()
        code = match.group('code').upper()

        if code.lower() in ('ajuda', 'help', 'lista', 'list'):
            msg = 'Aqui está a lista de moedas disponíveis para conversão (fonte: Banco Central Europeu):\n\n'

            for k, v in self.rates.iteritems():
                msg += '%s - %s (%s)\n' % (k, v['name'], v['symbol'])
        else:
            try:
                rate = self.rates[code]['rate']
                reverse_rate = 1 / rate
                msg = '1 EUR = {:.4f} {code}\n1 {code} = {:.4f} EUR'.format(rate, reverse_rate, code=code)
            except KeyError:
                msg = '{code}? Isso é a moeda de onde, Marte?'.format(code=code)

        return TextMessageProtocolEntity(msg, to=message.getFrom())
