""" Test the main route of the backend. """
import unittest
from src.main import app

class TestMain(unittest.TestCase):
    """Test the main route of the backend."""
    def setUp(self):
        """Set up a test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        """Test if the home route returns the expected response."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello from the backend!"})

if __name__ == "__main__":
    unittest.main()
