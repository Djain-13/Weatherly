import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import datetime
load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: int
    humidity : int
    sunrise : str
    sunset : str
    date_time: str
    forecast: list

def get_lan_lon(city_name, country_code, API_Key):
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{country_code}&appid={API_Key}').json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

def get_current_weather(lat, lon, API_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        description=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temperature=int(resp.get('main').get('temp')),
        humidity=int(resp.get('main').get('humidity')),
        sunrise=convert_unix_to_time(resp.get('sys').get('sunrise')),
        sunset=convert_unix_to_time(resp.get('sys').get('sunset')),
        date_time=get_current_date_time(),
      forecast=[] 
    )
    return data

def convert_unix_to_time(unix_time):
    return datetime.datetime.fromtimestamp(unix_time).strftime('%I:%M %p')


def get_current_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d & %I:%M')

def get_5_day_forecast(lat, lon, API_key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric').json()
    forecast_dict={}

    for item in resp['list']:
        date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')

        if date not in forecast_dict:
            forecast_dict[date] = {
                'temperature' : int(item['main']['temp']),
                'description' : item['weather'][0]['description'],
                'icon' : item['weather'][0]['icon']
            }
    forecast_list = [{'date': date, **data} for date, data in forecast_dict.items()]
    return forecast_list


def main(city_name, country_name):
    lat, lon = get_lan_lon(city_name, country_name, api_key)
    weather_data=(get_current_weather(lat, lon, api_key))
    weather_data.forecast = get_5_day_forecast(lat, lon, api_key)
    return weather_data


if __name__ == "__main__":
    lat, lon = get_lan_lon('Mumbai', 'India', api_key)
    print(get_current_weather(lat, lon, api_key))