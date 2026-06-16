import requests

# Request to a non-existent post
response = requests.get("https://jsonplaceholder.typicode.com/posts/9999")

print("Status code:", response.status_code)

if response.status_code == 200:
    print("Found it!")
else:
    print("Not found")

# Request to a valid post
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

print("\nValid post status code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("Title:", data["title"])
    print("Found it!")
else:
    print("Not found")