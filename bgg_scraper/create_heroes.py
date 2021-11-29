import requests

url = 'http://localhost:8000/heroes'

hero = {
    "id": 3,
    "name": "Super Man",
    "secret_name": "Clark",
    "age": 35
}

res = requests.post(url, json=hero)
print(res.status_code)
print(res.text)