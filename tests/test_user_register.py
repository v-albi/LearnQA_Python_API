import requests
from libr.base_case import BaseCase
from libr.assertions import Assertions
from libr.my_requests import MyRequests
import pytest
import allure


@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    exclude_params = [
        ("no_password"),
        ("no_username"),
        ("no_firstName"),
        ("no_lastName"),
        ("no_email"),
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 200)
        Assertions.assert_json_has_key(resp, "id")

    def test_create_user_with_existing_email(self):
        email ="vinkotov@example.com"
        data = self.prepare_registration_data(email)

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {resp.content}"

    def test_create_user_with_wrong_email(self):
        email = "vinkotov.example.com"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {resp.content}"

    @pytest.mark.parametrize("params", exclude_params)
    def test_create_user_without_parameters(self, params):
        if params == "no_password":
            resp = MyRequests.post(
                "/user/", data={
                    "username": "learnqa",
                    "firstName": "learnqa",
                    "lastName": "learnqa",
                    "email": "vinkotov@example.com"})

            Assertions.assert_code_status(resp, 400)
            assert resp.content.decode("utf-8") == "The following required params are missed: password", f"Unexpected response content {resp.content}"

        if params == "no_username":
            resp = MyRequests.post(
                "/user/", data={
                    "password": "123",
                    "firstName": "learnqa",
                    "lastName": "learnqa",
                    "email": "vinkotov@example.com"})

            Assertions.assert_code_status(resp, 400)
            assert resp.content.decode("utf-8") == "The following required params are missed: username", f"Unexpected response content {resp.content}"

        if params == "no_firstName":
            resp = MyRequests.post(
                "/user/", data={
                    "password": "123",
                    "username": "learnqa",
                    "lastName": "learnqa",
                    "email": "vinkotov@example.com"})

            Assertions.assert_code_status(resp, 400)
            assert resp.content.decode("utf-8") == "The following required params are missed: firstName", f"Unexpected response content {resp.content}"

        if params == "no_lastName":
            resp = MyRequests.post(
                "/user/", data={
                    "password": "123",
                    "username": "learnqa",
                    "firstName": "learnqa",
                    "email": "vinkotov@example.com"})

            Assertions.assert_code_status(resp, 400)
            assert resp.content.decode("utf-8") == "The following required params are missed: lastName", f"Unexpected response content {resp.content}"

        if params == "no_email":
            resp = MyRequests.post(
                "/user/", data={
                    "password": "123",
                    "username": "learnqa",
                    "firstName": "learnqa",
                    "lastName": "learnqa"})

            Assertions.assert_code_status(resp, 400)
            assert resp.content.decode("utf-8") == "The following required params are missed: email", f"Unexpected response content {resp.content}"

    def test_create_user_with_short_name(self):
        firstName = "a"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": firstName,
            "lastName": "learnqa",
            "email": "vinkotov@example.com"
        }

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == "The value of 'firstName' field is too short", f"Unexpected response content {resp.content}"

    def test_create_user_with_long_name(self):
        firstName = "sdflsljgskgjskgsgfkjdgbkxzvhkxghxdogzpihgjoibkhbkdssdflsljgskgjskgsgfkjdgbkxzvhkxghxdogzpihgjoibkhbkddflsljgskgjskgsgfkjdgbkxzvhkxghxdogzpihgjoibkhbkdsdflsljgskgjskgsgfkjdgbkxzvhkxghxdogzpihgjoibkhbkdsdflsljgskgjskgsgfkjdgbkxzvhkxghxdogzpihgjoibkhbkdcgfde"
        data = {
            "password": "123",
            "username": "learnqa",
            "firstName": firstName,
            "lastName": "learnqa",
            "email": "vinkotov@example.com"
        }

        resp = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(resp, 400)
        assert resp.content.decode("utf-8") == "The value of 'firstName' field is too long", f"Unexpected response content {resp.content}"
