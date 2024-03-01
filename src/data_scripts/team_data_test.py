import unittest
from unittest.mock import patch
import team_data
from sqlalchemy import create_engine, text
import pandas as pd

class TestTeamDataIntegration(unittest.TestCase):

    def setUp(self):
        # Configure your test database connection
        self.database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
        self.engine = create_engine(self.database_url)

    def mock_api_response(self):
        # This is a simplified version of the expected API response
        return {
            'response': [
                [{
                    'team': {'name': 'Test Team'},
                    'group': {'name': 'Test Conference'},
                    'games': {'win': {'total': 10, 'percentage': 0.6}, 'lose': {'total': 6}, 'played': 16},
                    'points': {'for': 1000, 'against': 800},
                    'position': 1
                }]
            ]
        }

    @patch('requests.get')
    def test_get_team_data(self, mock_get):
        # Mock the API response
        mock_get.return_value.json = self.mock_api_response

        # Execute the script (you might need to adjust this if your script or function requires arguments)
        team_data.get_team_data()

        # Verify database changes
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM teams")).fetchone()
            self.assertEqual(result[0], 30)  # Assuming 30 teams were fetched

            # Further verification can be added here to check data integrity

    def tearDown(self):
        #delete test data
        with self.engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE teams"))

if __name__ == '__main__':
    unittest.main()
