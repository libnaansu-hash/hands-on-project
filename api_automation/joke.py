import requests

response = requests.get("https://official-joke-api.appspot.com/random_joke")
response.raise_for_status()

joke = response.json()

print(joke["setup"])
print(joke["punchline"])