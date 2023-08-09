from libr.my_requests import MyRequests
from libr.base_case import BaseCase
from libr.assertions import Assertions
import allure


@allure.epic("Edit cases")
class TestUserEdit(BaseCase):
    def test_edit_just_creating_user(self):
        # register new user
        register_data = self.prepare_registration_data()
        resp1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")

        email = register_data["email"]
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

        # edit authorized user
        new_name = "changed_name"

        resp3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(resp3, 200)

        # get user data
        resp4 = MyRequests.get(f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
        resp4,
        "firstName",
        new_name,
        "Wrong name of the edited user"
        )

    def test_edit_unauthorized_user(self):
        # register new user
        register_data = self.prepare_registration_data()
        resp1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")

        user_id = self.get_json_value(resp1, "id")

        # edit unauthorized user
        edited_name = "new_name"

        resp2 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": edited_name}
        )

        Assertions.assert_code_status(resp2, 400)
        assert resp2.content.decode("utf-8") == "Auth token not supplied", \
            f"Unexpected response content {resp2.content}"

    def test_edit_user_using_another_user_id(self):
        # register first user
        register_data1 = self.prepare_registration_data()
        register_user1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(register_user1, 200)
        Assertions.assert_json_has_key(register_user1, "id")

        email1 = register_data1["email"]
        password1 = register_data1["password"]
        user_id1 = self.get_json_value(register_user1, "id")

        # register second user
        register_data2 = self.prepare_registration_data()
        register_user2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(register_user2, 200)
        Assertions.assert_json_has_key(register_user2, "id")

        email2 = register_data2["email"]
        password2 = register_data2["password"]
        first_name = register_data2["firstName"]
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

        # edit first user using second user id
        new_name = "changed_name"

        resp = MyRequests.put(
            f"/user/{user_id_2}",
            headers={"x-csrf-token": token1},
            cookies={"auth_sid": auth_sid1},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(resp, 200)

        # get first user info
        resp2 = MyRequests.get(f"/user/{user_id1}",
                             headers={"x-csrf-token": token1},
                             cookies={"auth_sid": auth_sid1})

        Assertions.assert_json_value_by_name(
            resp2,
            "firstName",
            new_name,
            "Name of the user was changed but should not have been"
        )

        # get second user info
        resp3 = MyRequests.get(f"/user/{user_id_2}",
                               headers={"x-csrf-token": token2},
                               cookies={"auth_sid": auth_sid2})

        Assertions.assert_json_value_by_name(
        resp3,
        "firstName",
        first_name,
        "Name of the user was changed but should not have been"
        )

    def test_edit_email_of_authorized_user(self):
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

        # edit authorized user
        new_email = "learnqa05182023163827.example.com"

        resp3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(resp3, 400)
        assert resp3.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {resp3.content}"

        # get user data
        resp4 = MyRequests.get(f"/user/{user_id}",
                             headers={"x-csrf-token": token},
                             cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            resp4,
            "email",
            email,
            "Email was changed but should not have been"
        )

    def test_edit_first_name_to_short_one(self):
        # register new user
        register_data = self.prepare_registration_data()
        resp1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(resp1, 200)
        Assertions.assert_json_has_key(resp1, "id")

        email = register_data["email"]
        firstName = register_data["firstName"]
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

        # edit authorized user
        new_name = "l"

        resp3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        resp_error = resp3.json()
        Assertions.assert_code_status(resp3, 400)
        assert resp_error["error"] == "Too short value for field firstName", f"Unexpected response content {resp3.content}"

        # get user data
        resp4 = MyRequests.get(f"/user/{user_id}",
                             headers={"x-csrf-token": token},
                             cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            resp4,
            "firstName",
            firstName,
            "Wrong name of the edited user"
        )
