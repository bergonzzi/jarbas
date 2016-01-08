# -*- coding: utf-8 -*-
import logging
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from tmdb3 import set_key, set_cache, searchMovie
import config


class MovieViews(object):
    def __init__(self, interface_layer):
        self.api_key = set_key(config.tmdb_api_key)
        self.routes = [
            ('^' + config.cmd_prefix + '(?:searchmovie|(?:procura|pesquisa)r?\s?filme)\s(?P<movie>[^$]+)$', self.search_movie),
            ('^' + config.cmd_prefix + '(?:movie|filme)\s(?P<movie>[^$]+)$', self.get_movie)
        ]

        set_cache(filename=config.movie_cache)

    def _get_movie_details(self, results):
        try:
            res = results[0]
            title = res.title.encode('utf-8')
            releasedate = res.releasedate.strftime('%Y-%m-%d').encode('utf-8')

            if res.tagline.encode('utf-8'):
                tagline = 'Tagline: %s\n\n' % res.tagline.encode('utf-8')
            else:
                tagline = ''

            overview = res.overview.encode('utf-8')
            msg = '%s (%s)\n\n%sOverview: %s' % (title, releasedate, tagline, overview)
        except IndexError:
            msg = False

        return msg

    def _not_found(self, title):
        msg = 'Não encontrei nenhum filme com o título "%s", vê lá se não te enganaste a escrever - experimenta ' \
              'separar palavras, remover pontuação ou o ano do filme, por exemplo.' % title
        return msg

    def search_movie(self, message, match):
        arg = match.group('movie').lower()
        res = searchMovie(arg)
        msg = ''
        intro = 'Filmes encontrados para "%s"\n\n' % match.group('movie')
        more_results = ''
        end_tip = '\n\nPara ver os detalhes de um filme, copia o nome da lista acima e envia "/filme titulo" numa mensagem ' \
                  '(não incluas ano).'

        if not res:
            msg = self._not_found(match.group('movie'))
        elif len(res) == 1:
            # If only 1 result show the details immediately
            msg = self._get_movie_details(res)
        else:
            for i, movie in enumerate(res):
                num = i + 1

                if num < config.max_movies:
                    title = movie.title.encode('utf-8')

                    # Sometimes a unicode object is returned instead of a datetime
                    try:
                        releasedate = movie.releasedate.strftime('%Y').encode('utf-8')
                    except AttributeError:
                        releasedate = movie.releasedate.encode('utf-8')

                    msg += '%s (%s)\n' % (title, releasedate)
                elif num == config.max_movies + 1:
                    more_results = '...'

            msg = intro + msg + more_results + end_tip

        return TextMessageProtocolEntity(msg, to=message.getFrom())

    def get_movie(self, message, match):
        arg = match.group('movie').lower()
        msg = self._get_movie_details(searchMovie(arg))

        if not msg:
            msg = self._not_found(match.group('movie'))

        return TextMessageProtocolEntity(msg, to=message.getFrom())
