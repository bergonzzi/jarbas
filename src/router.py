"""
    The Route Layer.
    Here the message is routed to its proper view.
    The routes are defined with regular expressions and callback functions (just like any web framework).
"""
import threading
import re
import logging

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback

from views import basic_views
from views.media import MediaViews
from views.super_views import SuperViews
from views.group_admin import GroupAdminViews
from views.google import GoogleViews
from views.weather import WeatherViews
from views.news import NewsViews
from views.cinema import CinemaViews
from views.chat import ChatViews
from views.movie import MovieViews
from views.bing import BingViews
from views.currency import CurrencyViews
from views.grammar_nazi import GrammarViews
from views.wiki import WikiViews


# Basic regex routes
routes = [("^/ping", basic_views.ping),
          ("^/e(cho)?\s(?P<echo_message>[^$]+)$", basic_views.echo)]


class RouteLayer(YowInterfaceLayer):
    def __init__(self):
        """
            The definition of routes and views (callbacks)!

            For the simple message handling, just calls the callback function, and expects a message entity to return.
            For more complex handling, like asynchronous file upload and sending, it creates a object passing 'self',
            so the callback can access the 'self.toLower' method
        """
        super(RouteLayer, self).__init__()

        # Google views to handle tts, search and youtube
        routes.extend(GoogleViews(self).routes)

        # Media views to handle url print screen and media download
        routes.extend(MediaViews(self).routes)

        # adds super fun views
        routes.extend(SuperViews(self).routes)

        # group admin views disabled by default.
        # read the issue on: https://github.com/joaoricardo000/whatsapp-bot-seed/issues/4
        # enable on your own risk!
        # routes.extend(GroupAdminViews(self).routes)

        # Weather views
        routes.extend(WeatherViews(self).routes)

        # News views
        routes.extend(NewsViews(self).routes)

        # Cinema views
        routes.extend(CinemaViews(self).routes)

        # Chat views
        routes.extend(ChatViews(self).routes)

        # Movie views
        routes.extend(MovieViews(self).routes)

        # Bing views to handle image search
        routes.extend(BingViews(self).routes)

        # Currency views for exchange rates
        routes.extend(CurrencyViews(self).routes)

        # View for wiki search
        routes.extend(WikiViews(self).routes)

        # View for grammar corrections, needs to come last as it's a catch-all pattern
        routes.extend(GrammarViews(self).routes)

        self.views = [(re.compile(pattern, re.IGNORECASE), callback) for pattern, callback in routes]

    def route(self, message):
        """Get the text from message and tests on every route for a match"""
        text = message.getBody()
        for route, callback in self.views:
            match = route.match(text)
            if match:  # in case of regex match, the callback is called, passing the message and the match object
                threading.Thread(target=self.handle_callback, args=(callback, message, match)).start()
                break

    def handle_callback(self, callback, message, match):
        try:
            # A bit hacky but avoids logging every single message since the nazi route matches everything
            if not callback.__name__ == 'nazi':
                # log message request
                if message.isGroupMessage():
                    logging.info("(GROUP)[%s]-[%s]\t%s" % (message.getParticipant(), message.getFrom(), message.getBody()))
                else:
                    logging.info("(PVT)[%s]\t%s" % (message.getFrom(), message.getBody()))
            # execute callback request
            data = callback(message, match)
            if data: self.toLower(data)  # if callback returns a message entity, sends it.
        except Exception as e:
            logging.exception("Error routing message: %s\n%s" % (message.getBody(), message))

    @ProtocolEntityCallback("message")
    def on_message(self, message):
        """Executes on every received message"""
        self.toLower(message.ack())  # Auto ack
        self.toLower(message.ack(True))  # Auto ack (double blue check symbol)
        # Routing only text type messages, for now ignoring other types. (media, audio, location...)
        if message.getType() == 'text':
            self.route(message)

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        """Auto ack for every message receipt confirmation"""
        self.toLower(entity.ack())
