from src.Main.main import read_credentials, open_session, sign_in, create_requests_session
import unittest


class TestApiCorrectness(unittest.TestCase):
    def test_authentication(self):
        session = create_requests_session()
        username, password = read_credentials()

        # activating authentication for the session
        session.auth = (username, password)

        sign_in(session=session, username=username, password=password)

        open_session(session=session)

        session.close()

        # here is this trivial assert. But if open_session fails, it will throw an Exception and the test will fail
        self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()
