import requests
from sqlalchemy import create_engine
import pandas as pd

# Function to get NBA player career stats using the API
def get_nba_player_stats(player_id):
    url = f"https://stats.nba.com/stats/playercareerstats?PlayerID={player_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"}
    response = requests.get(url, headers=headers)
    data = response.json()
    # Extract relevant data from the response
    # (This will depend on the structure of the API response)
    stats_data = data["resultSets"][0]["rowSet"]
    columns = data["resultSets"][0]["headers"]
    stats_df = pd.DataFrame(stats_data, columns=columns)
    return stats_df

# Database setup
engine = create_engine('postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e')

# Get NBA player career stats for Nikola Jokic
player_id = '203999'
nba_stats_df = get_nba_player_stats(player_id)

# Store data in SQLite database
nba_stats_df.to_sql('player_career_stats', engine, if_exists='replace', index=False)

# Dispose of the database engine
engine.dispose()
