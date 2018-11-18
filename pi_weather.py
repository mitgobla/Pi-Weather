import os
from time import sleep
from papirus import PapirusComposite
from weather import Weather, Unit

directory_path = os.path.dirname(os.path.realpath(__file__))

weather = Weather(unit=Unit.CELSIUS)
ink_display = PapirusComposite(False)
first_iteration = True
while True:
    lookup = weather.lookup_by_location('llandysul')

    sunrise = lookup.astronomy.sunrise
    sunset = lookup.astronomy.sunset

    visibility = lookup.atmosphere.visibility+lookup.units.distance
    pressure = lookup.atmosphere.pressure+lookup.units.pressure
    wind_speed = lookup.wind.speed+lookup.units.speed
    wind_direction = lookup.wind.direction

    humidity = str(lookup.atmosphere.humidity)+"%"
    temperature = lookup.condition.temp+lookup.units.temperature
    weather_type = lookup.condition.text
    weather_code = lookup.condition.code
    if first_iteration:
        ink_display.AddImg(os.path.join(directory_path, 'images', 'weather', str(weather_code)+'.png'), 0, 0, (96, 96), Id = "WeatherIcon")
        ink_display.AddText(weather_type, 96, 0, size=10, Id="WeatherText")
    else:
        ink_display.UpdateImg("WeatherIcon", os.path.join(directory_path, 'images', 'weather', str(weather_code)+'.png'))
        ink_display.UpdateText("WeatherText", lookup.condition.text)
    ink_display.WriteAll()
    sleep(60)
