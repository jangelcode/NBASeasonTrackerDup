from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Career stats for Nikola Jokic
career = playercareerstats.PlayerCareerStats(player_id='203999') 

data_frame = career.get_data_frames()[0]

db_params = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'defense',
}

engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')

data_frame.to_sql('player_career_stats', engine, if_exists='replace', index=False)

engine.dispose()
