import json
import sys

from typing import Dict, List
from urllib import error, parse, request
from weathercli.config import get_api_key


BASE_WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Weather Condition Codes
# https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)


def build_weather_query(city_input: List[str], imperial: bool = False) -> str:
    """Builds the URL for an API request to OpenWeather's weather API.

    Args:
        city_input (List[str]): Name of a city as collected by argparse
        imperial (bool): Whether or not to use imperial units for temperature

    Returns:
        str: URL formatted for a call to OpenWeather's city name endpoint
    """
    api_key = get_api_key()
    city_name = " ".join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = "imperial" if imperial else "metric"
    url = (
        f"{BASE_WEATHER_API_URL}?q={url_encoded_city_name}"
        f"&units={units}&appid={api_key}"
    )
    return url


def build_historical_query(
    city_input: List[str], imperial: bool = False, cnt: int = 3
) -> str:
    api_key = get_api_key()
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
        if http_error.code == 401:  # 401 - Unauthorized
            sys.exit("Access denied. Check your API key.")
        elif http_error.code == 404:  # 404 - Not Found
            sys.exit("Can't find weather data for this city.")
        else:
            sys.exit(f"Something went wrong...({http_error.code})")

    try:
        data = response.read()
    except json.JSONDecodeError:
        sys.exit("Couldn't read the server response.")

    return json.loads(data)
