# weatherCLI

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
       Warsaw        ☁️    Broken clouds     ☁️  1.9°C (feels like -2.9°C)
```

Alternatively, Imperial units can be displayed by using the `-i` flag:

```bash
$ weather San Francisco -i
   San Francisco     ☁️      Few clouds      ☁️  66.2°F (feels like 64.8°F)
```

### Weather Forecasts

Forecasted weather conditions can be displayed by appending the `--forecast` flag. Forecasts are available on 3 hour intervals.

```bash
$ weather Warsaw -f
       Warsaw 2022-02-08 01:00        ☁️   Broken clouds    ☁️  1.9°C (feels like -2.8°C)
       Warsaw 2022-02-08 04:00        ☁️   Broken clouds    ☁️  1.9°C (feels like -2.5°C)
       Warsaw 2022-02-08 07:00        ☁️   Broken clouds    ☁️  1.2°C (feels like -3.3°C)
```

By default, 3 forecast periods are displayed, but up to 40 (or 5 days) can be displayed by passing a number to the `-n NUMBER` argument.

```bash
$ weather New York -i -f -n 8
      New York 2022-02-07 19:00       🌧️     Light rain     🌧️  36.8°F (feels like 32.3°F)
      New York 2022-02-07 22:00       🌧️     Light rain     🌧️  35.9°F (feels like 30.5°F)
      New York 2022-02-08 01:00       🌧️     Light rain     🌧️  35.1°F (feels like 29.3°F)
      New York 2022-02-08 04:00       🌧️     Light rain     🌧️  34.8°F (feels like 28.8°F)
      New York 2022-02-08 07:00       ☁️   Broken clouds    ☁️  31.9°F (feels like 24.8°F)
      New York 2022-02-08 10:00       ☀️     Clear sky      ☀️  36.8°F (feels like 30.1°F)
      New York 2022-02-08 13:00       ☀️     Clear sky      ☀️  41.2°F (feels like 34.6°F)
      New York 2022-02-08 16:00       ☁️  Scattered clouds  ☁️  39.5°F (feels like 31.9°F)
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
