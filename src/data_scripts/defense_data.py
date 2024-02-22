from nba_api.stats.endpoints import playercareerstats
from sqlalchemy import create_engine

# Career stats for Nikola Jokic
career = playercareerstats.PlayerCareerStats(player_id='203999') 

data_frame = career.get_data_frames()[0]

engine = create_engine('postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e')

data_frame.to_sql('player_career_stats', engine, if_exists='replace', index=False)

engine.dispose()
