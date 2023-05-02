import json

import requests

URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"

resp1 = requests.post(URL).text
resp2 = requests.get(URL, params={"method": "HEAD"}).text
resp3 = requests.get(URL, params={"method": "GET"}).text

print(f"1. {resp1}",  f"2. {resp2}", f"3. {resp3}", sep="\n")

params = {"method": "GET"}

# methods for GET request with params
resp_get_params = requests.get(URL, params=params)
if resp_get_params.text != '{"success":"!"}':
    print(f"4. Response text: {resp_get_params.text}", f"request - {resp_get_params.request}", f"params = {resp_get_params.request.body}")

# methods for POST request with params
resp_post_params = requests.post(URL, params=params)
if resp_post_params.text == '{"success":"!"}':
    print(f"4. Response text: {resp_post_params.text},", f"request - {resp_post_params.request},", f"params = {resp_post_params.request.body}")

# methods for PUT request with params
resp_put_params = requests.put(URL, params=params)
if resp_put_params.text == '{"success":"!"}':
    print(f"4. Response text: {resp_put_params.text},", f"request - {resp_put_params.request},", f"params = {resp_get_params.request.body}")

# methods for DELETE request with params
resp_delete_params = requests.delete(URL, params=params)
if resp_delete_params.text == '{"success":"!"}':
    print(f"4. Response text: {resp_delete_params.text},", f"request - {resp_delete_params.request},", f"params = {resp_delete_params.request.body}")


payload = [{"method": "POST"}, {"method": "PUT"}, {"method": "DELETE"}]

for i in payload:
    # methods for GET request with data
    resp_get_data = requests.get(URL, data=i)
    if resp_get_data.text == '{"success":"!"}':
        print(f"4. Response text: {resp_get_data.text},", f"request - {resp_get_data.request}", f"payload = {i}")

    # methods for POST request with data
    resp_post_data = requests.post(URL, data=i)
    if resp_post_data.text == '{"success":"!"}' and i != {"method": "POST"}:
        print(f"4. Response text: {resp_post_data.text}", f"{resp_post_data.request},", f"payload = {i}")
    if resp_post_data.text == 'Wrong method provided' and payload == {"method": "POST"}:
        print(f"4. Response text: {resp_post_data.text},", f"request - {resp_post_data.request},", f"payload = {i}")

    # methods for PUT request with data
    resp_put_data = requests.put(URL, data=i)
    if resp_put_data.text == '{"success":"!"}' and i != {"method": "PUT"}:
        print(f"4. Response text: {resp_put_data.text}", f"{resp_put_data.request},", f"payload = {i}")
    if resp_put_data.text == 'Wrong method provided' and payload == {"method": "PUT"}:
        print(f"4. Response text: {resp_put_data.text},", f"request - {resp_put_data.request},", f"payload = {i}")

    # methods for DELETE request with data
    resp_delete_data = requests.delete(URL, data=i)
    if resp_delete_data.text == '{"success":"!"}' and i != {"method": "DELETE"}:
        print(f"4. Response text: {resp_delete_data.text}", f"{resp_put_data.request},", f"payload = {i}")
    if resp_delete_data.text == 'Wrong method provided' and payload == {"method": "DELETE"}:
        print(f"4. Response text: {resp_delete_data.text},", f"request - {resp_put_data.request},", f"payload = {i}")
