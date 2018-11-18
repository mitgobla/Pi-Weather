# -*- coding: utf-8 -*-
import datetime
import os
from sys import argv
from time import sleep
from papirus import PapirusComposite
from weather import Weather, Unit

if len(argv) > 1:
    LOCATION = str(argv[1])
else:
    LOCATION = 'London'

DIRECTORY = os.path.dirname(os.path.realpath(__file__))

INK_DISPLAY = PapirusComposite(False)
FIRST_ITERATION = True
COMPASS_DIRS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def convert24(time, meridiem):
    """Convert hour to 24 hour format

    Arguments:
        time {list} -- Array of Hour, Minute
        meridiem {str} -- String of meridiem

    Returns:
        int -- 24 Hour format of hour
    """

    if meridiem == 'am' and time[0] == '12':
        return 0
    elif meridiem == 'am':
        return int(time[0])
    elif meridiem == 'pm' and time[0] == '12':
        return int(time[0])
    return int(time[0])+12


def main():
    """Weather Monitoring System
    """

    weather = Weather(unit=Unit.CELSIUS)
    lookup = weather.lookup_by_location(LOCATION)

    if not lookup:
        print("Invalid Location")
        exit()

    current_hour = datetime.datetime.now().hour
    current_minute = datetime.datetime.now().minute
    current_time = "%s:%s" % current_hour, current_minute

    title = lookup.title.split(' - ')[-1]

    sunrise = lookup.astronomy.sunrise
    sunrise_meridiem = sunrise.split(' ')[-1]
    sunrise_time = sunrise.split(' ')[0].split(':')
    sunrise_hour = convert24(sunrise_time, sunrise_meridiem)
    sunrise_minute = int(sunrise_time[1])
    sunrise_time_24 = str(sunrise_hour)+":"+str(sunrise_minute)

    sunset = lookup.astronomy.sunset
    sunset_meridiem = sunset.split(' ')[-1]
    sunset_time = sunset.split(' ')[0].split(':')
    sunset_hour = convert24(sunset_time, sunset_meridiem)
    sunset_minute = int(sunset_time[1])
    sunset_time_24 = str(sunset_hour)+":"+str(sunset_minute)

    visibility = lookup.atmosphere.visibility+lookup.units.distance
    pressure = lookup.atmosphere.pressure+lookup.units.pressure

    wind_speed = lookup.wind.speed+lookup.units.speed
    wind_direction_degrees = lookup.wind.direction
    ix = int((int(wind_direction_degrees) + 11.25)/22.5 - 0.02)
    wind_direction_compass = COMPASS_DIRS[ix % 16]

    humidity = str(lookup.atmosphere.humidity)+"%"
    temperature = lookup.condition.temp+"°"+lookup.units.temperature

    weather_type = lookup.condition.text
    weather_code = lookup.condition.code

    forecast = lookup.forecast

    if FIRST_ITERATION:
        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            weather_code)+'.png'), 0, 0, (48, 48), Id="WeatherIcon")
        INK_DISPLAY.AddText(weather_type, 48, 0, size=16, Id="TextLineOne",
                            fontPath='/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf')
        INK_DISPLAY.AddText(temperature+"    "+humidity, 48,
                            24, size=12, Id="TextLineTwo")
        INK_DISPLAY.AddText(wind_speed+"  "+wind_direction_compass,
                            48, 36, size=12, Id="TextLineThree")

        INK_DISPLAY.AddText(forecast[0].day, 3, 49,
                            size=12, Id="ForecastDayOne")
        INK_DISPLAY.AddText(forecast[1].day, 35,
                            49, size=12, Id="ForecastDayTwo")
        INK_DISPLAY.AddText(forecast[2].day, 68,
                            49, size=12, Id="ForecastDayThree")
        INK_DISPLAY.AddText(forecast[3].day, 101,
                            49, size=12, Id="ForecastDayFour")
        INK_DISPLAY.AddText(forecast[4].day, 135,
                            49, size=12, Id="ForecastDayFive")
        INK_DISPLAY.AddText(forecast[5].day, 167,
                            49, size=12, Id="ForecastDaySix")

        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            forecast[0].code)+'.png'), 1, 63, (32, 32), Id="ForecastIconOne")
        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            forecast[1].code)+'.png'), 34, 63, (32, 32), Id="ForecastIconTwo")
        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            forecast[2].code)+'.png'), 67, 63, (32, 32), Id="ForecastIconThree")
        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            forecast[3].code)+'.png'), 100, 63, (32, 32), Id="ForecastIconFour")
        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            forecast[4].code)+'.png'), 133, 63, (32, 32), Id="ForecastIconFive")
        INK_DISPLAY.AddImg(os.path.join(DIRECTORY, 'images', 'weather', str(
            forecast[5].code)+'.png'), 166, 63, (32, 32), Id="ForecastIconSix")
    else:
        INK_DISPLAY.UpdateImg("WeatherIcon", os.path.join(
            DIRECTORY, 'images', 'weather', str(weather_code)+'.png'))
        INK_DISPLAY.UpdateText("TextLineOne", weather_type)
        INK_DISPLAY.UpdateText("TextLineTwo", temperature+"    "+humidity)
        INK_DISPLAY.UpdateText(
            "TextLineThree", wind_speed+"  "+wind_direction_compass)

        INK_DISPLAY.UpdateText("ForecastDayOne", forecast[0].day)
        INK_DISPLAY.UpdateText("ForecastDayTwo", forecast[1].day)
        INK_DISPLAY.UpdateText("ForecastDayThree", forecast[2].day)
        INK_DISPLAY.UpdateText("ForecastDayFour", forecast[3].day)
        INK_DISPLAY.UpdateText("ForecastDayFive", forecast[4].day)
        INK_DISPLAY.UpdateText("ForecastDaySix", forecast[5].day)

        INK_DISPLAY.UpdateImg("ForecastIconOne", os.path.join(
            DIRECTORY, 'images', 'weather', str(forecast[0].code)+'.png'))
        INK_DISPLAY.UpdateImg("ForecastIconTwo", os.path.join(
            DIRECTORY, 'images', 'weather', str(forecast[1].code)+'.png'))
        INK_DISPLAY.UpdateImg("ForecastIconThree", os.path.join(
            DIRECTORY, 'images', 'weather', str(forecast[2].code)+'.png'))
        INK_DISPLAY.UpdateImg("ForecastIconFour", os.path.join(
            DIRECTORY, 'images', 'weather', str(forecast[3].code)+'.png'))
        INK_DISPLAY.UpdateImg("ForecastIconFive", os.path.join(
            DIRECTORY, 'images', 'weather', str(forecast[4].code)+'.png'))
        INK_DISPLAY.UpdateImg("ForecastIconSix", os.path.join(
            DIRECTORY, 'images', 'weather', str(forecast[5].code)+'.png'))
        INK_DISPLAY.WriteAll()
        sleep(20)
        INK_DISPLAY.UpdateText(
            "TextLineTwo", "Hi: "+forecast[0].high+"°"+lookup.units.temperature+"  Lo: "+forecast[0].low+"°"+lookup.units.temperature)
        INK_DISPLAY.UpdateText("TextLineThree", wind_speed +
                               " "+wind_direction_degrees+"°")
        INK_DISPLAY.WriteAll()
        sleep(20)
        INK_DISPLAY.UpdateText("TextLineTwo", title)
        INK_DISPLAY.UpdateText("TextLineThree", lookup.last_build_date[5:-4])
    INK_DISPLAY.WriteAll()
    sleep(20)


while True:
    main()
    FIRST_ITERATION = False
