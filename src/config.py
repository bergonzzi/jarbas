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

# Path to download the media requests
# (audio recordings, printscreens, media and youtube videos)
media_storage_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'media/')) + '/'

# Logging configuration.
# By default only logs the command messages.
# If logging_level set to logging.DEBUG, yowsup will log every protocoll message exchange with server.
log_format = '_%(filename)s_\t[%(levelname)s][%(asctime)-15s] %(message)s'
logging_level = logging.INFO
