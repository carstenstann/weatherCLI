# weather.py

import argparse
import json
import sys

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from urllib import error, parse, request

from weathercli import __app_name__, __version__, style
from weathercli.config import (
    init_config_file,
    set_api_key,
    get_config,
    get_config_path
)


BASE_WEATHER_API_URL  = 'http://api.openweathermap.org/data/2.5/weather'
BASE_FORECAST_API_URL = 'http://api.openweathermap.org/data/2.5/forecast'

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE      = range(300, 400)
RAIN         = range(500, 600)
SNOW         = range(600, 700)
ATMOSPHERE   = range(700, 800)
CLEAR        = range(800, 801)
CLOUDY       = range(801, 900)


def read_user_cli_args() -> argparse.Namespace:
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="gets weather and temperature information for a city"
    )
    parser.add_argument(
        "city", nargs="*", type=str, help="enter the city name"
    )
    parser.add_argument(
        "-i",
        "--imperial",
        action="store_true",
        help="display the temperature in imperial units"
    )
    parser.add_argument(
        "-f",
        "--forecast",
        action="store_true",
        help="Whether to return current of forecasted weather"
    )
    parser.add_argument(
        "-n",
        "--number",
        default=3,
        help="The number of forecast periods (3h) to query. Should be between 1 and 40. Invalid inputs will be replaced by the default of 3."
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Print weather CLI version.'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Creates config.ini and stores API key'
    )
    parser.add_argument(
        '--show-config',
        action='store_true'
    )
    return parser.parse_args()


def parse_args_exit(args: argparse.Namespace) -> None:
    """
    Process the CLI user provided arguments.
    """
    if args.version:
        print(f'{__app_name__} {__version__}')
        sys.exit(0)
    
    if args.api_key:
        config_file_path = init_config_file()
        set_api_key(args.api_key)
        print(f'API key successfully saved: {config_file_path}')
        sys.exit(0)

    if args.show_config:
        config_file_path = get_config_path()
        print(f'{config_file_path}\n')
        config = get_config()
        for section in config.sections():
            print(f'[{section}]')
            for k, v in config.items(section):
                print(f'{k} = {v}')
            print()
        sys.exit(0)


def _get_api_key() -> str:
    """Fetch the API key from configuration file."""
    try:
        config = get_config()
    except FileNotFoundError:
        print('No config file found.')
        print('Run weather --api-key {API KEY} to set an API key.')
        print('Generate an API key at https://openweathermap.org/')
        sys.exit(1)
    
    try:
        api_key = config['openweather']['api_key']
    except KeyError:
        print('API key not found.')
        print('Run weather --api-key {API KEY} to set an API key.')
        print('Generate an API key at https://openweathermap.org/')
        sys.exit(1)
    return api_key


def build_weather_query(city_input: List[str], imperial: bool = False) -> str:
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url


def build_historical_query(city_input: List[str], imperial: bool = False, cnt: int = 3) -> str:
    api_key = _get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_FORECAST_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&cnt={cnt}&appid={api_key}"
    )
    return url


def get_weather_data(query_url: str) -> Dict:
    """Makes an API request to a URL and returns the data as a Python object.

    Args:
        query_url (str): URL formatted for OpenWeather's city name endpoint

    Returns:
        dict: Weather information for a specific city
    """
    try:
        response = request.urlopen(query_url)
    except error.HTTPError as http_error:
        if http_error.code == 401: # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404: # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong...({http_error.code})")
    
    try:
        data = response.read()
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")
    
    return json.loads(data)


def display_weather_info(weather_data: Dict, imperial: bool = False) -> None:
    """Prints formatted weather information about a city.

    Args:
        weather_data (dict): API response from OpenWeather by city name
        imperial (bool): Whether or not to use imperial units for temperature

    More information at https://openweathermap.org/current#name
    """
    city = weather_data["name"]
    weather_id = weather_data["weather"][0]["id"]
    weather_description = weather_data["weather"][0]["description"]
    temperature = weather_data["main"]["temp"]
    temperature_feel = weather_data["main"]["feels_like"]

    style.change_color(style.REVERSE)
    print(f"{city:^{style.PADDING}}", end="")
    style.change_color(style.RESET)
    
    weather_symbol, color = _select_weather_display_params(weather_id)

    style.change_color(color)
    print(f" {weather_symbol}", end=" ")
    print(
        f"{weather_description.capitalize():^{style.PADDING}}",
        end=" "
    )
    print(f"{weather_symbol} ", end=" ")
    style.change_color(style.RESET)

    units = 'F' if imperial else 'C'
    print(f"{temperature:.1f}°{units} (feels like {temperature_feel:.1f}°{units})")


def display_forecast_info(weather_data: Dict, imperial: bool = False) -> None:
    city = weather_data['city']['name']
    timezone_shift = weather_data['city']['timezone']

    for forecast in weather_data['list']:
        weather_id = forecast['weather'][0]['id']
        weather_description = forecast['weather'][0]['description']
        temperature = forecast['main']['temp']
        temperature_feel = forecast['main']['feels_like']
        time = datetime.fromisoformat(forecast['dt_txt'])
        local = (time + timedelta(seconds=timezone_shift)).strftime('%Y-%m-%d %H:%M')

        style.change_color(style.REVERSE)
        print(f"{city+' '+local:^{style.PADDING+17}}", end="")
        style.change_color(style.RESET)
        
        weather_symbol, color = _select_weather_display_params(weather_id)

        style.change_color(color)
        print(f" {weather_symbol}", end="")
        print(
            f"{weather_description.capitalize():^{style.PADDING}}",
            end=""
        )
        print(f"{weather_symbol} ", end=" ")
        style.change_color(style.RESET)

        units = 'F' if imperial else 'C'
        print(f"{temperature:.1f}°{units} (feels like {temperature_feel:.1f}°{units})")


def _select_weather_display_params(weather_id: int) -> Tuple:
    if weather_id in THUNDERSTORM:
        display_params = ("⚡", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("🌧️", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("☀️", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("☁️", style.WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.RESET)
    
    return display_params


def main():
    user_args = read_user_cli_args()
    parse_args_exit(user_args)
    if user_args.forecast:
        query_url = build_historical_query(user_args.city, user_args.imperial, cnt=user_args.number)
        weather_data = get_weather_data(query_url)
        display_forecast_info(weather_data, user_args.imperial)
    else:
        query_url = build_weather_query(user_args.city, user_args.imperial)
        weather_data = get_weather_data(query_url)
        display_weather_info(weather_data, user_args.imperial)


if __name__ == "__main__":
    main()
