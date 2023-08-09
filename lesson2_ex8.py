import requests
import time

URL = "https://playground.learnqa.ru/ajax/api/longtime_job"

start_task = requests.get(URL)

token_value = start_task.json().get('token')
seconds = start_task.json().get("seconds")

resp1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job",
                     params={"token": token_value})
status1 = resp1.json().get("status")
assert status1 == "Job is NOT ready", "Job is already ready"
time.sleep(seconds)

resp2 = requests.get(URL, params={"token": token_value})
status2 = resp2.json().get("status")
assert status2 == "Job is ready", "Job is not ready but should be"
result = resp2.json()["result"]
assert result in resp2.json()["result"], f"Response json does not have key '{result}'"
