import pytest
import unittest
from unittest.mock import patch
import team_data
from sqlalchemy import create_engine, text

class TestTeamDataIntegration(unittest.TestCase):

    def setUp(self):
        self.database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
        self.engine = create_engine(self.database_url)

    def mock_api_response(self):
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
        mock_get.return_value.json = self.mock_api_response
        team_data.get_team_data()

        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM teams")).fetchone()
            #verify all teams were pulled
            self.assertEqual(result[0], 30)

    def tearDown(self):
        #delete test data
        with self.engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE teams"))

if __name__ == '__main__':
    pytest.main()
