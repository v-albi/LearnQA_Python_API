import json
import requests
import pytest


class TestUserAgent:
    user_agents = ['Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                   'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
                   'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
                   'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
                   ]

    @pytest.mark.parametrize("user_agent", user_agents)
    def test_user_agent(self, user_agent):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        resp1 = requests.get(url, headers={"User-Agent": user_agent})

        # agents_and_values = {
            # {'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30':
                # {'platform': "Mobile", 'browser': 'No', 'device': 'Android'}},
            # {'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1':
                # {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}},
            # {'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)':
                # {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}},
            # {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0':
                # {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}},
            # {'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1':
                # {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}}
        # }

        resp_as_dict = resp1.json()

        # first user agent
        if user_agent == "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30":
            expected_platform = "Mobile"
            actual_platform = resp_as_dict["platform"]
            assert actual_platform == expected_platform, "Actual and expected platforms in first user agent are not the same"

            expected_browser = "No"
            actual_browser = resp_as_dict["browser"]
            assert actual_browser == expected_browser, "Actual and expected browsers in first user agent are not the same"

            expected_device = "Android"
            actual_device = resp_as_dict["device"]
            assert actual_device == expected_device, "Actual and expected devices in first user agent are not the same"

        # second user agent
        if user_agent == "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1":
            expected_platform = "Mobile"
            actual_platform = resp_as_dict["platform"]
            assert actual_platform == expected_platform, "Actual and expected platforms in second user agent are not the same"

            expected_browser = "Chrome"
            actual_browser = resp_as_dict["browser"]
            assert actual_browser == expected_browser, "Actual and expected browsers in second user agent are not the same"

            expected_device = "iOS"
            actual_device = resp_as_dict["device"]
            assert actual_device == expected_device, "Actual and expected devices in second user agent are not the same"

        # third user agent
        if user_agent == "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)":
            expected_platform = "Googlebot"
            actual_platform = resp_as_dict["platform"]
            assert actual_platform == expected_platform, "Actual and expected platforms in third user agent are not the same"

            expected_browser = "Unknown"
            actual_browser = resp_as_dict["browser"]
            assert actual_browser == expected_browser, "Actual and expected browsers in third user agent are not the same"

            expected_device = "Unknown"
            actual_device = resp_as_dict["device"]
            assert actual_device == expected_device, "Actual and expected devices in third user agent are not the same"

        # fourth user agent
        if user_agent == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0":
            expected_platform = "Web"
            actual_platform = resp_as_dict["platform"]
            assert actual_platform == expected_platform, "Actual and expected platforms in fourth user agent are not the same"

            expected_browser = "Chrome"
            actual_browser = resp_as_dict["browser"]
            assert actual_browser == expected_browser, "Actual and expected browsers in fourth user agent are not the same"

            expected_device = "No"
            actual_device = resp_as_dict["device"]
            assert actual_device == expected_device, "Actual and expected devices in fourth user agent are not the same"

        # fifth user agent
        if user_agent == "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1":
            expected_platform = "Mobile"
            actual_platform = resp_as_dict["platform"]
            assert actual_platform == expected_platform, "Actual and expected platforms in fifth user agent are not the same"

            expected_browser = "No"
            actual_browser = resp_as_dict["browser"]
            assert actual_browser == expected_browser, "Actual and expected browsers in fifth user agent are not the same"

            expected_device = "iPhone"
            actual_device = resp_as_dict["device"]
            assert actual_device == expected_device, "Actual and expected devices in fifth user agent are not the same"


    print(f"User agents with AssertionError:", user_agents[1], "- browser, ",
      user_agents[2], "- platform, ", user_agents[2], "- device")

