import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "current_weather": True
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

temperature = data["current_weather"]["temperature"]

print(f"Current temperature in Mumbai: {temperature}°C")

if temperature > 30:
    print("Carry water!")
else:
    print("Nice weather!")