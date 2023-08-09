from libr.base_case import BaseCase
from libr.assertions import Assertions
from libr.my_requests import MyRequests
import allure


@allure.epic("Deletion cases")
class TestUserDelete(BaseCase):
    def test_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'}

        resp = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(resp, "auth_sid")
        token = self.get_header(resp, "x-csrf-token")
        user_id = self.get_json_value(resp, "user_id")

        resp2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(resp2, 400)
        assert resp2.content.decode('utf-8') == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"User with id '{user_id}' was deleted but should not have been"

    def test_delete_new_user(self):
        # register new user
        register_data = self.prepare_registration_data()
        resp1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")

        email = register_data["email"]
        # firstName = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(resp1, "id")

        # login created user
        login_data = {
            "email": email,
            "password": password
        }

        resp2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(resp2, "auth_sid")
        token = self.get_header(resp2, "x-csrf-token")

        # delete authorized user
        resp3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(resp3, 200)

        # get user data
        resp4 = MyRequests.get(f"/user/{user_id}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(resp4, 404)
        assert resp4.content.decode('utf-8') == "User not found", "User was not deleted"

    def test_delete_user_being_authorized_as_another_user(self):
        # register first user
        register_data1 = self.prepare_registration_data()
        register_user1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(register_user1, 200)
        Assertions.assert_json_has_key(register_user1, "id")

        email1 = register_data1["email"]
        password1 = register_data1["password"]
        user_id = self.get_json_value(register_user1, "id")

        # register second user
        register_data2 = self.prepare_registration_data()
        register_user2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(register_user2, 200)
        Assertions.assert_json_has_key(register_user2, "id")

        email2 = register_data2["email"]
        password2 = register_data2["password"]
        user_id_2 = self.get_json_value(register_user2, "id")

        # login first user
        login_data1 = {
            "email": email1,
            "password": password1
        }

        login_user1 = MyRequests.post("/user/login", data=login_data1)

        auth_sid1 = self.get_cookie(login_user1, "auth_sid")
        token1 = self.get_header(login_user1, "x-csrf-token")

        # login second user
        login_data2 = {
            "email": email2,
            "password": password2
        }

        login_user2 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookie(login_user2, "auth_sid")
        token2 = self.get_header(login_user2, "x-csrf-token")

        # delete first user using second user id
        resp = MyRequests.delete(f"/user/{user_id_2}",
                             headers={"x-csrf-token": token1},
                             cookies={"auth_sid": auth_sid1})

        Assertions.assert_code_status(resp, 200)

        # get first user data
        resp2 = MyRequests.get(f"/user/{user_id}",
                               headers={"x-csrf-token": token1},
                               cookies={"auth_sid": auth_sid1})

        Assertions.assert_code_status(resp2, 404)
        assert resp2.content.decode('utf-8') == "User not found", "User was not deleted"

        # get second user info
        resp3 = MyRequests.get(f"/user/{user_id_2}",
                               headers={"x-csrf-token": token2},
                               cookies={"auth_sid": auth_sid2})

        Assertions.assert_code_status(resp3, 200)
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(resp3, expected_fields)


