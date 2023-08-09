import requests

class TestCookie:
    def test_check_cookie(self):
        URL = "https://playground.learnqa.ru/api/homework_cookie"
        check_cookie = requests.get(URL)
        cookie_value = check_cookie.cookies.get('HomeWork')

        assert cookie_value == "hw_value", f"Got {cookie_value} instead of 'HomeWork=hw_value'"