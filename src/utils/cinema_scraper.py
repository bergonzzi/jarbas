import logging
import requests
import config
from lxml import html


def movies(cinema):
    src = ''
    cinema_name = ''

    for k, v in config.cinema_sources.iteritems():
        if cinema in v['synonyms']:
            src = v['url']
            cinema_name = v['name']

    logging.debug(src)

    r = requests.get(src)
    tree = html.fromstring(r.content)

    all_movies = tree.xpath('//ul[@class="unstyled column-group gutters poster-list internal"]/li')
    movie_list = {}
    msg = ''
    intro = cinema_name + ':\n\n'
    version = ''
    subject = ''
    duration = ''

    for movie in all_movies:
        sessions = []

        try:
            title = movie.xpath('.//p[@class="quarter-bottom-space original"]/text()')[0]
        except IndexError:
            title = 'N/A'

        try:
            version = ' (' + movie.xpath('.//span[@class="version"]/text()')[0] + ')'
            if version == ' (VO)':
                version = ''
        except IndexError:
            version = ''

        try:
            subject = movie.xpath('.//span[@class="subject"]/text()')[0]
        except IndexError:
            subject = ''

        try:
            duration = movie.xpath('.//div[contains(@class,"details")]/ul[contains(@class, "info")]/li/p[contains(text(), "min")]/text()')[0]
        except IndexError:
            duration = ''

        for session in movie.xpath('.//ul[@class="sessions quarter-vertical-space inline unstyled"]/li'):
            sessions.append(session.xpath('.//p/text()')[0].strip())

        movie_list[title] = {
            'version': version,
            'subject': subject,
            'duration': duration,
            'sessions': ' / '.join(sessions)
        }

    # print movie_list

    for movie, values in movie_list.iteritems():
        msg += '%s%s\n%s, %s\n%s\n\n' % \
               (movie.encode('utf-8'),
                values['version'].encode('utf-8'),
                values['subject'].encode('utf-8'),
                values['duration'].encode('utf-8'),
                values['sessions'].encode('utf-8'))

    return intro + msg
