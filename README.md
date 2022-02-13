# weatherCLI

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple CLI to view current and forecast weather data in the terminal.

## Inspiration

This project was inspired by Martin Breuss's brilliant [Raining Outside? Build a Weather CLI App With Python](https://realpython.com/build-a-python-weather-app-cli/) tutorial on Real Python.

This repository extends the tutorial CLI with CLI interfaces for retrieving weather forecasts and inputting and storing API keys. Finally, the project was restructured as a python package for shorter CLI calls.

## Installation

The weather CLI can be installed by cloning this repository and building locally with the following commands:

```bash
$ git clone https://github.com/carstenstann/weatherCLI.git
Cloning into 'weatherCLI'...
$ cd weatherCLI
$ python setup.py install
$ python setup.py clean
```

## Setup

Before the CLI can query weather data, an [API key for OpenWeather's API](https://openweathermap.org/appid) must first be configured (the free tier should provide more than enough call for private usage).

After signing up, the generated API key can be provided to the CLI, which stores it locally for future use.

```bash
$ weather --api-key <API_KEY>
API key successfully saved: {OS dependent filepath}/config.ini
```

Config files are saved at the following locations:

- linux: ~/.local/share/weathercli/
- macOS: ~/Library/Application Support/weathercli
- windows: C:/Users/<USER>/AppData/Roaming/weathercli

The location and contents of the config can be retrieved with the following command:

```bash
weather --show-config
```

## Usage

### Current Weather

Current weather conditions can be queried by city name. Additionally, the `-i` flag display temperature in terms of Fahrenheit instead of Celcius (the defualt).

```bash
$ weather <CITY_NAME> [-i]
```

For example, current weather in Warsaw, Poland can be displayed with the following call:

```bash
$ weather Warsaw
       Warsaw        ☁️    Broken clouds    ☁️  2.8°C (feels like -0.9°C)
```

Alternatively, Imperial units can be displayed by using the `-i` flag:

```bash
$ weather San Francisco -i
   San Francisco     ☁️      Few clouds     ☁️  48.0°F (feels like 47.0°F)
```

### Weather Forecasts

Forecasted weather conditions can be displayed by appending the `--forecast` flag. Forecasts are available on 3 hour intervals.

```bash
$ weather Warsaw -f
       Warsaw 2022-02-08 16:00        ☃️     Light snow     ☃️   2.9°C (feels like -2.0°C)
       Warsaw 2022-02-08 19:00        🌧️     Light rain     🌧️   3.4°C (feels like -1.6°C)
       Warsaw 2022-02-08 22:00        🌧️     Light rain     🌧️   4.5°C (feels like  0.1°C)
```

By default, 3 forecast periods are displayed, but up to 40 (or 5 days) can be displayed by passing a number to the `-n NUMBER` argument.

```bash
$ weather New York -i -f -n 8
      New York 2022-02-08 10:00       ☀️     Clear sky      ☀️  38.5°F (feels like 31.8°F)
      New York 2022-02-08 13:00       ☀️     Clear sky      ☀️  39.9°F (feels like 32.5°F)
      New York 2022-02-08 16:00       ☁️  Scattered clouds  ☁️  40.0°F (feels like 32.3°F)
      New York 2022-02-08 19:00       ☁️  Scattered clouds  ☁️  35.3°F (feels like 26.3°F)
      New York 2022-02-08 22:00       ☀️     Clear sky      ☀️  32.9°F (feels like 24.6°F)
      New York 2022-02-09 01:00       ☀️     Clear sky      ☀️  32.0°F (feels like 24.4°F)
      New York 2022-02-09 04:00       ☀️     Clear sky      ☀️  31.7°F (feels like 25.3°F)
      New York 2022-02-09 07:00       ☀️     Clear sky      ☀️  31.9°F (feels like 26.0°F)
```

## Uninstall

The package can be uninstalled with `pip`:

```bash
$ pip uninstall weathercli
```

Don't forget to remove the config.ini file from the respective directory. On macOS this can be done as follows:

```bash
$ rm -r ~/Library/Application\ Support/weathercli
```
