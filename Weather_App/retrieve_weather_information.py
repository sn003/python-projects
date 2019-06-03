import requests

api_key = None
with open("API_KEY.txt") as api:
   api_key = api.read().strip("\n")

base_url = "http://api.openweathermap.org/data/2.5/weather?"


def retrieve(city_name):
    complete_url = "{}appid={}&q={}".format(base_url, api_key, city_name)
    response = requests.get(complete_url)

    output = response.json()
    return output
