import pytest
import requests
from libr.base_case import BaseCase
from libr.assertions import Assertions
from libr.my_requests import MyRequests
import allure


@allure.epic("Getting user info cases")
class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        resp = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(resp, "username")
        Assertions.assert_json_has_not_key(resp, "email")
        Assertions.assert_json_has_not_key(resp, "firstName")
        Assertions.assert_json_has_not_key(resp, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234",
        }

        resp1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(resp1, "auth_sid")
        token = self.get_header(resp1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(resp1, "user_id")

        resp2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                             headers={"x-csrf-token": token},
                             cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(resp2, expected_fields)

    @pytest.mark.flaky(reruns=3)
    def test_get_user_details_using_another_user_id(self):
        # register first user
        register_data1 = self.prepare_registration_data()
        register_user1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(register_user1, 200)
        Assertions.assert_json_has_key(register_user1, "id")

        email = register_data1["email"]
        firstName = register_data1["firstName"]
        password = register_data1["password"]
        user_id = self.get_json_value(register_user1, "id")

        # register second user
        register_data2 = self.prepare_registration_data()
        register_user2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(register_user2, 200)
        Assertions.assert_json_has_key(register_user2, "id")

        user_id_2 = self.get_json_value(register_user2, "id")

        # login first user
        login_data = {
            "email": email,
            "password": password
        }

        login_user = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(login_user, "auth_sid")
        token = self.get_header(login_user, "x-csrf-token")

        # get first user info using second user id

        resp = MyRequests.get(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_has_key(resp, "username")
        Assertions.assert_json_has_not_key(resp, "email")
        Assertions.assert_json_has_not_key(resp, "firstName")
        Assertions.assert_json_has_not_key(resp, "lastName")


