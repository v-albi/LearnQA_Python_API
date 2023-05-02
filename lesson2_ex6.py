import requests

URL = "https://playground.learnqa.ru/api/long_redirect"

resp = requests.get(URL, allow_redirects=True)

count = 0
for i in resp.history:
    count +=1

print(count)
print(resp.url)