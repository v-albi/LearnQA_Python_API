import requests

class TestCookie:
    def test_check_cookie(self):
        URL = "https://playground.learnqa.ru/api/homework_header"
        resp = requests.get(URL)
        resp_header = resp.headers.get("x-secret-homework-header")
        # print(resp.headers)

        assert resp_header == "Some secret value", "Header should be equal to 'Some secret value'"

