#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
from sys import argv
from time import sleep

from papirus import PapirusComposite
from weather import Weather

DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class PiWeather:

    def __init__(self):
        self.config = self.load_config()["weather"]

        self.unit = self.get_unit()
        self.weather = Weather(unit=self.unit)

        self.location = self.get_location()

        self.lookup = {}

        self.compass_dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                             "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        self.compass_dirs_simple = ["N", "NE", "NE", "NE", "E", "SE", "SE", "SE",
                                    "S", "SW", "SW", "SW", "W", "NW", "NW", "NW"]

    @staticmethod
    def load_config():
        """Load PiWeather Config

        Returns:
            dict -- Dictonary of config options
        """

        with open(os.path.join(DIRECTORY, 'config.json')) as config_file:
            return json.load(config_file)

    def get_unit(self):
        """Read the selected temperature unit from config

        Returns:
            str -- String of unit in lowercase
        """

        if "unit" in self.config:
            return self.config["unit"].lower()
        return "c"

    def get_location(self):
        """Read the location set in the config

        Returns:
            str -- String of the location
        """

        if len(argv) > 1:
            return str(argv[1])

        if "location" in self.config:
            return self.config["location"]

        return "London"

    def get_wind_direction(self, direction):
        """Converts the direction from degrees to compass

        Arguments:
            direction {int} -- Direction in degrees

        Returns:
            str -- Compass/Degrees direction depending on config
        """

        ix = int((int(direction) + 11.25)/22.5 - 0.02)
        if self.config["wind_direction"] == "compass":
            return self.compass_dirs[ix % 16]
        elif self.config["wind_direction"] == "simplecompass":
            return self.compass_dirs_simple[ix % 16]
        return direction

    @staticmethod
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

    def get_suntime(self, suntime):
        """Convert sunrise/set to 24 hour

        Arguments:
            suntime {str} -- String of time in 'HH:MM pm' format

        Returns:
            str -- Returns HH:MM in 24 format
        """

        meridiem = suntime.split(' ')[-1]
        suntime = suntime.split(' ')[0].split(':')
        sun_hour = self.convert24(suntime, meridiem)
        sun_minute = int(suntime[1])
        return str(sun_hour)+":"+str(sun_minute)

    def get_weather(self):
        """Get weather and populate lookup dictonary
        """

        lookup_data = self.weather.lookup_by_location(self.location)
        self.lookup = {
            "temperature": lookup_data.condition.temp+"°"+lookup_data.units.temperature,
            "humidity": lookup_data.atmosphere.humidity+"%",
            "wind": {
                "speed": lookup_data.wind.speed+lookup_data.units.speed,
                "direction": self.get_wind_direction(lookup_data.wind.direction)
            },
            "pressure": lookup_data.atmosphere.pressure+lookup_data.units.pressure,
            "visibility": lookup_data.atmosphere.visibility+lookup_data.units.distance,
            "sunrise": self.get_suntime(lookup_data.astronomy.sunrise),
            "sunset": self.get_suntime(lookup_data.astronomy.sunset),
            "weather_type": lookup_data.condition.text,
            "weather_code": lookup_data.condition.code,
            "forecast": lookup_data.forecast
        }


class PiDisplay(PiWeather):

    def __init__(self):
        PiWeather.__init__(self)
        self.display = PapirusComposite(False)

        self.unknown_icon = "3200.png"
        self.order = []
        self.gotWeather = False

        self.initalize_order()
        self.initalize_display()

    def initalize_order(self):
        """Create the order that information is displayed
        """

        for stat in self.config["stats"]:
            if self.config["stats"][stat]:
                self.order.append(stat)

    def initalize_display(self):
        """Add all the screen elements to the e-ink display
        """

        if self.config["forecast"]["enabled"]:
            self.display.AddImg(os.path.join(
                DIRECTORY, 'images', 'weather', self.unknown_icon), 0, 0, (48, 48), Id="WeatherIcon")
            self.display.AddText("Loading...", 48, 0, size=13, Id="LineOne",
                                 fontPath='/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf')
            self.display.AddText("Loading...", 48, 20, size=12, Id="LineTwo")
            self.display.AddText("Loading...", 48, 34,
                                 size=12, Id="LineThree")

            if self.config["forecast"]["sixday"]:
                self.display.AddText("...", 3, 49, size=12, Id="ForecastOne")
                self.display.AddText("...", 35, 49, size=12, Id="ForecastTwo")
                self.display.AddText(
                    "...", 68, 49, size=12, Id="ForecastThree")
                self.display.AddText(
                    "...", 101, 49, size=12, Id="ForecastFour")
                self.display.AddText(
                    "...", 135, 49, size=12, Id="ForecastFive")
                self.display.AddText("...", 167, 49, size=12, Id="ForecastSix")

                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 1, 63, (32, 32), Id="ForecastIconOne")
                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 34, 63, (32, 32), Id="ForecastIconTwo")
                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 67, 63, (32, 32), Id="ForecastIconThree")
                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 100, 63, (32, 32), Id="ForecastIconFour")
                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 133, 63, (32, 32), Id="ForecastIconFive")
                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 166, 63, (32, 32), Id="ForecastIconSix")
            else:
                self.display.AddText("Today: ...", 25, 51,
                                     size=12, Id="ForecastOne")
                self.display.AddText("Tomorrow: ...", 25,
                                     74, size=12, Id="ForecastTwo")

                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 1, 49, (23, 23), Id="ForecastIconOne")
                self.display.AddImg(os.path.join(
                    DIRECTORY, 'images', 'weather', self.unknown_icon), 1, 72, (23, 23), Id="ForecastIconTwo")
        else:
            self.display.AddImg(os.path.join(
                DIRECTORY, 'images', 'weather', self.unknown_icon), 1, 15, (80, 80), Id="WeatherIcon")
            self.display.AddText("Loading...", 1, 1, size=13, Id="LineOne",
                                 fontPath='/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf')
            self.display.AddText("Loading...", 82, 15, size=12, Id="LineTwo")
            self.display.AddText("Loading...", 82, 30,
                                 size=12, Id="Line Three")
        self.display.WriteAll()

    def update(self):
        """Regurlarly update the screen with new information
        """

        self.gotWeather = False
        while not self.gotWeather:
            try:
                self.get_weather()
                self.gotWeather = True
            except:
                sleep(60)

        if not self.lookup:
            print("Invalid Location")
            exit()

        self.display.UpdateImg("WeatherIcon", os.path.join(
            DIRECTORY, 'images', 'weather', str(self.lookup["weather_code"])+'.png'))
        self.display.UpdateText("LineOne", self.lookup["weather_type"])

        if self.config["forecast"]["enabled"]:
            if self.config["forecast"]["sixday"]:
                self.display.UpdateText(
                    "ForecastOne", self.lookup["forecast"][0].day)
                self.display.UpdateText(
                    "ForecastTwo", self.lookup["forecast"][1].day)
                self.display.UpdateText(
                    "ForecastThree", self.lookup["forecast"][2].day)
                self.display.UpdateText(
                    "ForecastFour", self.lookup["forecast"][3].day)
                self.display.UpdateText(
                    "ForecastFive", self.lookup["forecast"][4].day)
                self.display.UpdateText(
                    "ForecastSix", self.lookup["forecast"][5].day)

                self.display.UpdateImg("ForecastIconOne", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][0].code)+'.png'))
                self.display.UpdateImg("ForecastIconTwo", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][1].code)+'.png'))
                self.display.UpdateImg("ForecastIconThree", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][2].code)+'.png'))
                self.display.UpdateImg("ForecastIconFour", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][3].code)+'.png'))
                self.display.UpdateImg("ForecastIconFive", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][4].code)+'.png'))
                self.display.UpdateImg("ForecastIconSix", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][5].code)+'.png'))
            else:
                self.display.UpdateText(
                    "ForecastOne", "Today: "+self.lookup["forecast"][0].day)
                self.display.UpdateText(
                    "ForecastTwo", "Tomorrow: "+self.lookup["forecast"][1].day)

                self.display.UpdateImg("ForecastIconOne", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][0].code)+'.png'))
                self.display.UpdateImg("ForecastIconTwo", os.path.join(
                    DIRECTORY, 'images', 'weather', str(self.lookup["forecast"][1].code)+'.png'))

        for stat in self.order:
            if stat == "temperature":
                self.display.UpdateText("LineTwo", "Temp: "+self.lookup[stat])
                self.display.UpdateText(
                    "LineThree", "Hi: "+self.lookup["forecast"][0].high+" Lo: "+self.lookup["forecast"][0].low)
            elif stat == "humidity":
                self.display.UpdateText(
                    "LineTwo", "Humidity: "+self.lookup[stat])
                humidity = int(self.lookup[stat][:-1])
                scale = ""
                if humidity < 25:
                    scale = "Very Dry"
                elif humidity < 60:
                    scale = "Dry"
                elif humidity < 80:
                    scale = "Wet"
                else:
                    scale = "Very Wet"
                self.display.UpdateText("LineThree", scale)
            elif stat == "wind":
                self.display.UpdateText(
                    "LineTwo", "Speed: "+self.lookup[stat]["speed"])
                self.display.UpdateText(
                    "LineThree", "Direction: "+self.lookup[stat]["direction"])
            elif stat == "pressure":
                self.display.UpdateText("LineTwo", "Pressure")
                self.display.UpdateText("LineThree", self.lookup[stat])
            elif stat == "visibility":
                self.display.UpdateText("LineTwo", "Visibility")
                self.display.UpdateText("LineThree", self.lookup[stat])
            elif stat == "sunrise":
                self.display.UpdateText("LineTwo", "Sunrise")
                self.display.UpdateText("LineThree", self.lookup[stat])
            elif stat == "sunset":
                self.display.UpdateText("LineTwo", "Sunset")
                self.display.UpdateText("LineThree", self.lookup[stat])

            self.display.WriteAll()
            if len(self.order) >= 3:
                sleep(20)
            else:
                sleep(int(60/len(self.order)))
            # Can only request weather data every 43 seconds (2000 calls a day)
            # 20 seconds per slide is safe

PI = PiDisplay()

if __name__ == "__main__":
    while True:
        PI.update()
