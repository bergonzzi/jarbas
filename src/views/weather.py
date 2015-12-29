# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.openweathermap import weather, forecast
import config


class WeatherViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # Current weather
            # Tests:
            # jarbas diz me o tempo em londres
            # jarbas diz-me o tempo em londres
            # jarbas dá-me o tempo para lisboa
            # jarbas da me o tempo para lisboa sff
            # jarbas qual o tempo em paris?
            # jarbas dá me o tempo nos himalaias

            ("^{prefix}(qual|diz(\s|-)?me|d(á|a)(\s|-)?me)? (o )?tempo (?:em|para|na|no|nas|nos) (?P<location>[^$]+)(\?)?$".format(prefix=config.cmd_prefix), self.get_weather),
            ("^/tempo (?P<location>[^$]+)(\?)?$", self.get_weather),

            # Weather forecast
            ("^{prefix}previsao\s(?P<location>[^$]+)".format(prefix=config.cmd_prefix), self.get_forecast),
            ("^/previsao (?P<location>[^$]+)(\?)?$", self.get_forecast)
        ]

    def get_weather(self, message, match):
        location = match.group("location")
        w = weather(location)
        return TextMessageProtocolEntity(w, to=message.getFrom())

    def get_forecast(self, message, match):
        location = match.group("location")
        f = forecast(location)
        return TextMessageProtocolEntity(f, to=message.getFrom())
