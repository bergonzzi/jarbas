# -*- coding: utf-8 -*-
import os
import sys
import logging

"""
    Credentials to connect on Whatsapp Servers.
    (phone number, whatsapp key)

    To extract key use the yowsup-cli (using a python venv with yowsup installed):

    > yowsup-cli registration -C <CountryCode> -r sms -p <Phone Number with Country Code>
    ex.:
    yowsup-cli registration -C 55 -r sms -p 554899998888

    Then whatsapp will send a key via sms to the phone.
    Get that key then run:

    > yowsup-cli registration -C 55 -R <sms-key> -p 554899998888

    status: ok
    kind: free
    > pw: njH+QGBqGXXXXXXXOFa+Wth5riM=
    price: US$0.99
    price_expiration: 1444272405
    currency: USD
    cost: 0.99
    > login: 554899998888
    type: existing
    expiration: 1472404969

    Now just get the login and pw, and put them into env variables like this:

    export WHATSAPP_NUM=554899998888
    export WHATSAPP_PW=njH+QGBqGXXXXXXXOFa+Wth5riM=

"""

# Logging configuration.
# By default only logs the command messages.
# If logging_level set to logging.DEBUG, yowsup will log every protocoll message exchange with server.
log_format = '_%(filename)s_\t[%(levelname)s] [%(asctime)-15s] %(message)s'
logging_level = logging.INFO

# Authentication parameters are fetched from env variables
# This avoid storing them in a file
try:
    num = os.environ['WHATSAPP_NUM']
    pw = os.environ['WHATSAPP_PW']
    auth = (num, pw)
except KeyError:
    sys.exit('Missing environment variables WHATSAPP_NUM and/or WHATSAPP_PW!')

# If filter_groups is True, the bot only stays
# at groups that there is at least one admin on it.
# Otherwise will leave instantly if added.
filter_groups = False
admins = ['XXXXXXXXXXXX', ]

# Prefix required to invoke bot commands
# This is automatically added to every route
cmd_prefix = '/'

# Path to download the media requests
# (audio recordings, printscreens, media and youtube videos)
media_storage_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media/')) + '/'

# API settings for openweathermap
try:
    owm_api_key = os.environ['OPENWEATHER_API_KEY']
except KeyError:
    sys.exit('Missing environment variables OPENWEATHER_API_KEY!')

owm_lang = 'pt'
owm_unit = 'celsius'

# Pageres settings for website screenshots
pageres_params = '1440x1800 --no-crop'

# RSS feed for latest news
news_sources = {
    'Público': 'http://feeds.feedburner.com/PublicoRSS?format=xml',
    'Jornal de Notícias': 'http://feeds.jn.pt/JN-ULTIMAS',
    'O Jogo': 'http://feeds.ojogo.pt/OJ-Ultimas'
}
max_news = 10

# Cinema urls
cinema_sources = {
    'corte ingles': {
        'url': 'http://mag.sapo.pt/cinema/salas/uci-cinemas-el-corte-ingles',
        'name': 'UCI Cinemas - El Corte Inglés',
        'synonyms':
            ['uci', 'corte ingles', 'corte inglés']
    },
    'alegro': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinema-city-alegro-alfragide',
        'name': 'Cinema City Alegro Alfragide',
        'synonyms':
            ['alegro', 'allegro']
    },
    'alvalade': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinema-city-alvalade',
        'name': 'Cinema City Alvalade',
        'synonyms':
            ['alvalade']
    },
    'campo pequeno': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinema-city-campo-pequeno',
        'name': 'Cinema City Campo Pequeno',
        'synonyms':
            ['campo pequeno', 'cp pequeno', 'campo peq', 'cp peq', 'cp. peq', 'cp. peq.', 'c peq', 'campo peq.']
    },
    'alvalaxia': {
        'url': 'https://mag.sapo.pt/cinema/salas/cinemas-nos-alvalaxia',
        'name': 'Cinema NOS Alvaláxia',
        'synonyms':
            ['alvalaxia', 'alvaláxia', 'sporting']
    },
    'amoreiras': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinemas-nos-amoreiras',
        'name': 'Cinema NOS Amoreiras',
        'synonyms':
            ['amoreiras']
    },
    'colombo': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinemas-nos-colombo',
        'name': 'Cinema NOS Colombo',
        'synonyms':
            ['colombo']
    },
    'miraflores': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinemas-nos-dolce-vita-miraflores',
        'name': 'Cinema NOS Dolce Vita Miraflores',
        'synonyms':
            ['miraflores', 'dolce vita', 'dolce vitta']
    },
    'vasco da gama': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinemas-nos-vasco-da-gama',
        'name': 'Cinema NOS Vasco da Gama',
        'synonyms':
            ['vasco da gama', 'vasco gama', 'v gama', 'v. gama']
    },
    'monumental': {
        'url': 'http://mag.sapo.pt/cinema/salas/medeia-monumental',
        'name': 'Medeia Monumental',
        'synonyms':
            ['monumental', 'residence', 'saldanha']
    },
    'oeiras parque': {
        'url': 'http://mag.sapo.pt/cinema/salas/cinemas-nos-oeiras-parque',
        'name': 'Cinema NOS Oeiras Parque',
        'synonyms':
            ['oeiras parque', 'oeiras', 'oeiras park']
    }
}

