import argparse
import sys

from datetime import datetime, timedelta
from typing import Dict, Tuple
from weathercli import __app_name__, __version__
from weathercli.config import (
    init_config_file,
    set_api_key,
    get_config,
    get_config_path
)
from weathercli.weather import (
    THUNDERSTORM,
    DRIZZLE,
    RAIN,
    SNOW,
    ATMOSPHERE,
    CLEAR,
    CLOUDY,
    get_weather_data,
    build_weather_query,
    build_historical_query
)

PADDING = 20
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[33m"
WHITE = "\033[37m"
REVERSE = "\033[;7m"
RESET = "\033[0m"


def change_color(color):
    print(color, end="")


def read_user_cli_args() -> argparse.Namespace:
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description='gets weather and temperature information for a city'
    )
    parser.add_argument(
        'city', nargs='*', type=str, help='enter the city name'
    )
    parser.add_argument(
        '-i',
        '--imperial',
        action='store_true',
        help='display the temperature in imperial units'
    )
    parser.add_argument(
        '-f',
        '--forecast',
        action='store_true',
        help='Whether to return current of forecasted weather'
    )
    parser.add_argument(
        '-n',
        '--number',
        default=3,
        help='The number of forecast periods (3h) to query. Should be between 1 and 40. Invalid inputs will be replaced by the default of 3.'
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
    """Process the CLI user provided arguments."""
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


def _select_weather_display_params(weather_id: int) -> Tuple:
    if weather_id in THUNDERSTORM:
        display_params = ("⚡", RED)
    elif weather_id in DRIZZLE:
        display_params = ("🌦️", CYAN)
    elif weather_id in RAIN:
        display_params = ("🌧️", BLUE)
    elif weather_id in SNOW:
        display_params = ("☃️", WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", BLUE)
    elif weather_id in CLEAR:
        display_params = ("☀️", YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("☁️", WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", RESET)
    
    return display_params


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

    change_color(REVERSE)
    print(f"{city:^{PADDING}}", end="")
    change_color(RESET)
    
    weather_symbol, color = _select_weather_display_params(weather_id)

    change_color(color)
    print(f" {weather_symbol}", end=" ")
    print(
        f"{weather_description.capitalize():^{PADDING}}", end="")
    print(f"{weather_symbol} ", end=" ")
    change_color(RESET)

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

        change_color(REVERSE)
        print(f"{city+' '+local:^{PADDING+17}}", end="")
        change_color(RESET)
        
        weather_symbol, color = _select_weather_display_params(weather_id)

        change_color(color)
        print(f" {weather_symbol}", end="")
        print(
            f"{weather_description.capitalize():^{PADDING}}", end="")
        print(f"{weather_symbol} ", end=" ")
        change_color(RESET)

        units = 'F' if imperial else 'C'
        print(f"{temperature:>4.1f}°{units} (feels like {temperature_feel:>4.1f}°{units})")


def cli() -> None:
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
    sys.exit(0)


if __name__ == '__main__':
    cli()
