import os
import unittest
from main import create_app

# Set environment variables due to the fact that the unittests aren't performed in docker
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "50444"
os.environ["POSTGRES_USER"] = "AbgWatch_admin"
os.environ["POSTGRES_PASSWORD"] = "adafg-trastr-8090"
os.environ["POSTGRES_DB"] = "DIP"

# Initialize app with function from main
app = create_app()


class BackendTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """One-time setup for the tests"""
        cls.client = app.test_client()
        cls.client.testing = True

    def test_get_v_candidacy_mandates_all(self):
        """Test for the endpoint /v_candidacy_mandates/"""
        response = self.client.get('/v_candidacy_mandates/')
        self.assertEqual(response.status_code, 200)

    def test_get_v_candidacy_mandates_grouped_1(self):
        """Test for the endpoint /v_candidacy_mandates/?grouped=1"""
        response = self.client.get('/v_candidacy_mandates/?grouped=1')
        self.assertEqual(response.status_code, 200)

    def test_get_v_candidacy_mandates_grouped_2(self):
        """Test for the endpoint /v_candidacy_mandates/?grouped=2"""
        response = self.client.get('/v_candidacy_mandates/?grouped=2')
        self.assertEqual(response.status_code, 200)

    def test_get_vote_poll_details_all(self):
        """Test for the endpoint /vote_poll_details/"""
        response = self.client.get('/vote_poll_details/')
        self.assertEqual(response.status_code, 200)

    def test_get_vote_poll_details_grouped_1(self):
        """Test for the endpoint /vote_poll_details/?grouped=1"""
        response = self.client.get('/vote_poll_details/?grouped=1')
        self.assertEqual(response.status_code, 200)

    def test_get_vote_poll_details_grouped_2(self):
        """Test for the endpoint /vote_poll_details/?grouped=2"""
        response = self.client.get('/vote_poll_details/?grouped=2')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

# RUN WITH: python3 -m unittest tests/test_apis.py
