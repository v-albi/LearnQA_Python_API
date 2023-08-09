import pytest
from libr.base_case import BaseCase
from libr.assertions import Assertions
from libr.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUerAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        resp1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(resp1, "auth_sid")
        self.token = self.get_header(resp1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(resp1, "user_id")

    @allure.description("This test successfully authorizes user by email and password")
    @allure.feature("Positive authorization case")
    def test_auth_user(self):
        resp2 = MyRequests.get("/user/auth",
                             headers={"x-csrf-token": self.token},
                             cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            resp2,
            "user_id",
            self.user_id_from_auth_method,
            "User id from auth method is not equal to user id from check method"
        )

    @allure.description("This test checks authorization status w/o auth cookie or token")
    @allure.feature("Negative authorization case")
    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            resp2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token})

        else:
            resp2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            resp2,
            "user_id",
            0,
            "User id from auth method is not equal to user id from check method"
        )



