import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 13.08,
    "longitude": 80.27,
    "current_weather": True
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    temperature = data["current_weather"]["temperature"]
    wind_speed = data["current_weather"]["windspeed"]

    print(f"It is {temperature}°C in Chennai with wind speed {wind_speed} km/h.")
else:
    print("Something went wrong:", response.status_code)