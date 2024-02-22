import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Set Flask to testing mode
        app.config['TESTING'] = True

    def tearDown(self):
        pass  # Clean up, if needed

    def test_main_route(self):
        # Send a GET request to the / endpoint
        response = self.app.get('/')

        # Check if the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # You can also check for specific content in the response, for example, checking if the HTML contains a specific string
        self.assertIn(b'<h1>NBA Player Career Stats for Nikola Jokic</h1>', response.data)
        # You might want to check for other specific content or patterns in the HTML response as needed.

if __name__ == '__main__':
    unittest.main()

