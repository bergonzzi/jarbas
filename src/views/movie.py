# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from tmdb3 import set_key, set_cache, searchMovie, Movie
import numbers
import config


class MovieViews(object):
    def __init__(self, interface_layer):
        self.movie_list = []
        self.api_key = set_key(config.tmdb_api_key)
        self.routes = [
            ('^' + config.cmd_prefix + '(?:searchmovie|(?:procura|pesquisa)r?\s?filme)\s(?P<movie>[^$]+)$', self.search_movie),
            ('^' + config.cmd_prefix + '(?:movie|filme)\s(?P<movie>[^$]+)$', self.get_movie)
        ]

        set_cache(filename=config.movie_cache)

    def _get_movie_details(self, results):
        try:
            movie = results[0]
            title = movie.title.encode('utf-8')
            overview = movie.overview.encode('utf-8')
            releasedate = movie.releasedate.strftime('%Y-%m-%d').encode('utf-8')
            trailer = '\n\nTrailer: %s' % Movie(movie.id).youtube_trailers[0].geturl()

            if movie.tagline.encode('utf-8'):
                tagline = 'Tagline: %s\n\n' % movie.tagline.encode('utf-8')
            else:
                tagline = ''

            if not trailer:
                trailer = ''

            msg = '%s (%s)\n\n%sOverview: %s%s' % (title, releasedate, tagline, overview, trailer)
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
        end_tip = '\nPara ver os detalhes de um filme, basta indicar o número, por ex. "/filme 3".'

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

                    msg += '%d. %s (%s)\n' % (num, title, releasedate)
                    self.movie_list.append(title)
                elif num == config.max_movies + 1:
                    more_results = '...'

            msg = intro + msg + more_results + end_tip

        return TextMessageProtocolEntity(msg, to=message.getFrom())

    def get_movie(self, message, match):
        arg = match.group('movie').lower()

        # If user specified a number then fetch it from the last search
        if unicode(arg).isnumeric():
            movie_num = int(arg) - 1

            try:
                movie_title = self.movie_list[movie_num]
                msg = self._get_movie_details(searchMovie(movie_title))
            except IndexError:
                msg = 'O número %d não está na lista!' % (movie_num + 1)

        # Otherwise do a search by title
        else:
            msg = self._get_movie_details(searchMovie(arg))

        if not msg:
            msg = self._not_found(match.group('movie'))

        return TextMessageProtocolEntity(msg, to=message.getFrom())
