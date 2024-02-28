import unittest
from app import app

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        #create client
        self.app = app.test_client()
        #set testing mode
        app.config['TESTING'] = True

    def test_main_route(self):
        response = self.app.get('/')

        #check status code is 200
        self.assertEqual(response.status_code, 200)

        self.assertIn(b'<h2>Home</h2>', response.data)

if __name__ == '__main__':
    unittest.main()

