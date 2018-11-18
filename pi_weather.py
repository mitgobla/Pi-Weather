# -*- coding: utf-8 -*-
import os
from time import sleep
from papirus import PapirusComposite
from weather import Weather, Unit

directory_path = os.path.dirname(os.path.realpath(__file__))

ink_display = PapirusComposite(False)
first_iteration = True

while True:
    weather = Weather(unit=Unit.CELSIUS)
    lookup = weather.lookup_by_location('llandysul')

    sunrise = lookup.astronomy.sunrise
    sunset = lookup.astronomy.sunset

    visibility = lookup.atmosphere.visibility+lookup.units.distance
    pressure = lookup.atmosphere.pressure+lookup.units.pressure
    wind_speed = lookup.wind.speed+lookup.units.speed
    wind_direction = lookup.wind.direction

    humidity = str(lookup.atmosphere.humidity)+"%"+" rH"
    temperature = lookup.condition.temp+"°"+lookup.units.temperature
    weather_type = lookup.condition.text
    weather_code = lookup.condition.code
    if first_iteration:
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(weather_code)+'.png'), 0, 0, (48, 48), Id = "WeatherIcon")
        ink_display.AddText(weather_type, 48, 0, size=16, Id="WeatherText")
        ink_display.AddText(temperature+"    "+humidity, 48, 16, size=16, Id="TempHumdText")
    else:
        ink_display.UpdateImg("WeatherIcon", os.path.join(directory_path, 'images', 'weather', str(weather_code)+'.png'))
        ink_display.UpdateText("WeatherText", weather_type)
        ink_display.UpdateText("TempHumdText", temperature+"    "+humidity)
    ink_display.WriteAll()
    sleep(60)
