import unittest
import pandas as pd
import pytest
from sqlalchemy import create_engine
from playoff_status import get_playoff_status

class PlayoffStatusTest(unittest.TestCase):
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)

    def test_playoff_teams(self):
        query = f"SELECT \"Team\" FROM teams WHERE \"Conf. Standings\"={1} AND \"Conference\" = 'Eastern Conference';"
        df = pd.read_sql(query, con=self.engine)
        team = df["Team"].iloc[0]
        self.assertEqual(get_playoff_status(team), 'make the playoffs.')

    def test_playin_teams(self):
        query = f"SELECT \"Team\" FROM teams WHERE \"Conf. Standings\"={8} AND \"Conference\" = 'Eastern Conference';"
        df = pd.read_sql(query, con=self.engine)
        team = df["Team"].iloc[0]
        self.assertEqual(get_playoff_status(team), 'make the play-in tournament.')

    def test_non_playoff_teams(self):
        query = f"SELECT \"Team\" FROM teams WHERE \"Conf. Standings\"={12} AND \"Conference\" = 'Eastern Conference';"
        df = pd.read_sql(query, con=self.engine)
        team = df["Team"].iloc[0]
        self.assertEqual(get_playoff_status(team), 'miss the playoffs.')

if __name__ == "__main__":
    pytest.main()
