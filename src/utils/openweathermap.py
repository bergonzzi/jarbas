# -*- coding: utf-8 -*-
import pyowm
import locale
from datetime import datetime
from string import capwords
import config

owm = pyowm.OWM(API_key=config.owm_api_key, language=config.owm_lang)


def weather(location):
    obs = owm.weather_at_place(location)
    w = obs.get_weather()
    temp = round(w.get_temperature("celsius")["temp"], 1)
    temp_min = round(w.get_temperature(config.owm_unit)['temp_min'], 1)
    temp_max = round(w.get_temperature(config.owm_unit)['temp_max'], 1)
    humidity = w.get_humidity()
    detail = capwords(w.get_detailed_status())
    loc = obs.get_location().get_name()
    obs_time = datetime.fromtimestamp(w.get_reference_time(timeformat='unix')).strftime('%a %d')
    msg = u'Tempo para "%s": %s, temperatura de %sº, mínima de %sº, máxima de %sº e humidade de %s%%.' \
          % (loc, detail, temp, temp_min, temp_max, humidity)
    return msg.encode('utf-8')


def forecast(location):
    locale.setlocale(locale.LC_TIME, 'pt_PT')
    fc = owm.daily_forecast(location, limit=5)

    if fc:
        f = fc.get_forecast()
        loc = f.get_location().get_name()
        weathers = f.get_weathers()
        title = u'Previsão do tempo para "%s":\n' % loc

        weather_out = [title.encode('utf-8')]

        for w in weathers:
            date = datetime.fromtimestamp(w.get_reference_time(timeformat='unix')).strftime('%a %d')
            status = w.get_detailed_status().encode('utf-8')
            temp_min = round(w.get_temperature(config.owm_unit)['min'], 1)
            temp_max = round(w.get_temperature(config.owm_unit)['max'], 1)
            weather_str = '%s - %s, min: %sº, max: %sº' % (date, status, temp_min, temp_max)

            weather_out.append(weather_str)

        out_str = '\n'.join(weather_out)
    else:
        out_str = 'Das duas uma: ou eu não estou a funcionar bem, ou estás a gozar comigo!'

    return out_str
