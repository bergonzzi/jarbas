# -*- coding: utf-8 -*-
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.openweathermap import weather, forecast
import config


class WeatherViews(object):
    def __init__(self, interface_layer):
        self.routes = [
            # Current weather
            ("^" + config.cmd_prefix + "(?:tempo|weather|meteorologia) (?P<location>[^$]+)(\?)?$", self.get_weather),

            # Weather forecast
            ("^" + config.cmd_prefix + "(?:previs(?:a|ã)o|forecast) (?P<location>[^$]+)(\?)?$", self.get_forecast)
        ]

    def get_weather(self, message, match):
        location = match.group("location")
        w = weather(location)
        return TextMessageProtocolEntity(w, to=message.getFrom())

    def get_forecast(self, message, match):
        location = match.group("location")
        f = forecast(location)
        return TextMessageProtocolEntity(f, to=message.getFrom())
