import requests

response = requests.get("https://randomuser.me/api/?results=5")
response.raise_for_status()

data = response.json()

print(f"{'Name':<25}{'Age':<5}{'Country'}")
print("-" * 45)

for user in data["results"]:
    name = f"{user['name']['first']} {user['name']['last']}"
    age = user["dob"]["age"]
    country = user["location"]["country"]

    print(f"{name:<25}{age:<5}{country}")