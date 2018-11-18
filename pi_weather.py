# -*- coding: utf-8 -*-
import os
from time import sleep
from papirus import PapirusComposite
from weather import Weather, Unit

directory_path = os.path.dirname(os.path.realpath(__file__))

ink_display = PapirusComposite(False)
first_iteration = True
compass_dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

while True:
    weather = Weather(unit=Unit.CELSIUS)
    lookup = weather.lookup_by_location('llandysul')

    sunrise = lookup.astronomy.sunrise
    sunset = lookup.astronomy.sunset

    visibility = lookup.atmosphere.visibility+lookup.units.distance
    pressure = lookup.atmosphere.pressure+lookup.units.pressure
    wind_speed = lookup.wind.speed+lookup.units.speed
    wind_direction_degrees = lookup.wind.direction
    ix = int((int(wind_direction_degrees) + 11.25)/22.5 - 0.02)
    wind_direction_compass = compass_dirs[ix % 16]

    humidity = str(lookup.atmosphere.humidity)+"%"
    temperature = lookup.condition.temp+"°"+lookup.units.temperature
    weather_type = lookup.condition.text
    weather_code = lookup.condition.code
    forecast = lookup.forecast

    if first_iteration:
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            weather_code)+'.png'), 0, 0, (48, 48), Id="WeatherIcon")
        ink_display.AddText(weather_type, 48, 0, size=15, Id="WeatherText", fontPath='/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf')
        ink_display.AddText(temperature+"    "+humidity, 48,
                            16, size=15, Id="TempHumdText")
        ink_display.AddText(wind_speed+"  "+wind_direction_compass+" ("+wind_direction_degrees+"°)", 48, 32, size=13, Id="WindText")

        ink_display.AddText(forecast[0].day, 3, 49, size=12, Id="ForecastDayOne")
        ink_display.AddText(forecast[1].day, 35, 49, size=12, Id="ForecastDayTwo")
        ink_display.AddText(forecast[2].day, 68, 49, size=12, Id="ForecastDayThree")
        ink_display.AddText(forecast[3].day, 101, 49, size=12, Id="ForecastDayFour")
        ink_display.AddText(forecast[4].day, 135, 49, size=12, Id="ForecastDayFive")
        ink_display.AddText(forecast[5].day, 167, 49, size=12, Id="ForecastDaySix")

        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            forecast[0].code)+'.png'), 1, 63, (32, 32), Id="ForecastIconOne")
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            forecast[1].code)+'.png'), 34, 63, (32, 32), Id="ForecastIconTwo")
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            forecast[2].code)+'.png'), 67, 63, (32, 32), Id="ForecastIconThree")
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            forecast[3].code)+'.png'), 100, 63, (32, 32), Id="ForecastIconFour")
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            forecast[4].code)+'.png'), 133, 63, (32, 32), Id="ForecastIconFive")
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(
            forecast[5].code)+'.png'), 166, 63, (32, 32), Id="ForecastIconSix")
    else:
        ink_display.UpdateImg("WeatherIcon", os.path.join(
            directory_path, 'images', 'weather', str(weather_code)+'.png'))
        ink_display.UpdateText("WeatherText", weather_type)
        ink_display.UpdateText("TempHumdText", temperature+"    "+humidity)
        ink_display.UpdateText("WindText", wind_speed+"  "+wind_direction_compass+" ("+wind_direction_degrees+"°)")

        ink_display.UpdateText("ForecastDayOne", forecast[0].day)
        ink_display.UpdateText("ForecastDayTwo", forecast[1].day)
        ink_display.UpdateText("ForecastDayThree", forecast[2].day)
        ink_display.UpdateText("ForecastDayFour", forecast[3].day)
        ink_display.UpdateText("ForecastDayFive", forecast[4].day)
        ink_display.UpdateText("ForecastDaySix", forecast[5].day)

        ink_display.UpdateImg("ForecastIconOne", os.path.join(directory_path, 'images', 'weather', str(forecast[0].code)+'.png'))
        ink_display.UpdateImg("ForecastIconTwo", os.path.join(directory_path, 'images', 'weather', str(forecast[1].code)+'.png'))
        ink_display.UpdateImg("ForecastIconThree", os.path.join(directory_path, 'images', 'weather', str(forecast[2].code)+'.png'))
        ink_display.UpdateImg("ForecastIconFour", os.path.join(directory_path, 'images', 'weather', str(forecast[3].code)+'.png'))
        ink_display.UpdateImg("ForecastIconFive", os.path.join(directory_path, 'images', 'weather', str(forecast[4].code)+'.png'))
        ink_display.UpdateImg("ForecastIconSix", os.path.join(directory_path, 'images', 'weather', str(forecast[5].code)+'.png'))
    ink_display.WriteAll()
    sleep(60)