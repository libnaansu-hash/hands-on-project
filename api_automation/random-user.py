import requests

response = requests.get("https://randomuser.me/api/")
response.raise_for_status()

data = response.json()

user = data["results"][0]

name = f"{user['name']['first']} {user['name']['last']}"
email = user["email"]
country = user["location"]["country"]

print(f"Name: {name}")
print(f"Email: {email}")
print(f"Country: {country}")
