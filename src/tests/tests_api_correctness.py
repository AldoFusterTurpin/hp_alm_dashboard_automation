import unittest
import requests
import os


class TestApiCorrectness(unittest.TestCase):
    def test_authentication(self):
        with requests.Session() as session:
            file_path = os.path.join("credentials.txt")
            with open(file_path, "r", encoding="utf-8") as credentials_file:
                username = credentials_file.readline().strip()
                password = credentials_file.readline().strip()

            # activating authentication for the session
            session.auth = (username, password)

            # post authentication
            response = session.post(
                url="https://alm-1.azc.ext.hp.com/qcbin/authentication-point/authenticate?login-form-required=y",
                data="<alm-authentication><user>" + username + "</user><password>" + password + "</password></alm-authentication>")
            self.assertEqual(200, response.status_code)

            # log-in
            response = session.get(url="https://alm-1.azc.ext.hp.com/qcbin/rest/is-authenticated",
                                   headers={"Content-Type": "application/xml"})
            self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
