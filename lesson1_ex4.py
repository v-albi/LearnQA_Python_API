import requests

URL = 'https://playground.learnqa.ru/api/get_text'

resp = requests.get(URL)
print(resp.content.decode('utf-8'))





