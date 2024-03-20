import pandas as pd
from sqlalchemy import create_engine
import pytest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

from data_scripts.playoff_status import get_playoff_status

#connect to database
database_url = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
engine = create_engine(database_url)

#check that a #1 seed makes the playoffs
def test_playoff_teams():
    query = f"SELECT \"Team\" FROM teams WHERE \"Conf. Standings\"={1} AND \"Conference\" = 'Eastern Conference';"
    df = pd.read_sql(query, con=engine)
    team = df["Team"].iloc[0]
    assert get_playoff_status(team) == 'make the playoffs.'

#check #8 see would be a playin team
def test_playin_teams():
    query = f"SELECT \"Team\" FROM teams WHERE \"Conf. Standings\"={8} AND \"Conference\" = 'Eastern Conference';"
    df = pd.read_sql(query, con=engine)
    team = df["Team"].iloc[0]
    assert get_playoff_status(team) == 'make the play-in tournament.'

#check number 12 seed is not a playoff or playin team
def test_non_playoff_teams():
    query = f"SELECT \"Team\" FROM teams WHERE \"Conf. Standings\"={12} AND \"Conference\" = 'Eastern Conference';"
    df = pd.read_sql(query, con=engine)
    team = df["Team"].iloc[0]
    assert get_playoff_status(team) == 'miss the playoffs.'

if __name__ == "__main__":
    pytest.main()
