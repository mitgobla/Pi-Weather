# Pi-Weather

Weather Station built for Raspberry Pi Zero with a 2.0" PaPiRus E-Ink Display

## How to install

**1. First install requirements:**

```bash
#PaPiRus
curl -sSL https://pisupp.ly/papiruscode | sudo bash

#Weather API
sudo python3 -m pip install weather-api
```

More info on **PaPiRus** manual setup can be found on their [repository](https://www.github.com/PiSupply/PaPiRus).

**2. Run `pi_weather.py` with the first argument of a location of your choice.**

```bash
sudo python3 pi_weather.py "New York"
```

**Optionally**, replace `LOCATION = 'London'` on line 11 of `pi_weather.py` to a location of your choice.

**3. You should get a result similar to this:**

![Image of Pi-Weather](/docs/result.jpg)

## Planned Changes

1. Add use to buttons e.g change forecast range, show more detailed info, swap units.

2. Tidy up weather icons and make sure there are no duplicates for similar weather types.

3. Add lines to help separate forecast and current weather.

4. Add Inverted mode.
