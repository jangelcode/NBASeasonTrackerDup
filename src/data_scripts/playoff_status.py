import pandas as pd
from sqlalchemy import create_engine
# from database import get_database_URI

#get playoff status for each team (playoff, playin, or miss)
def get_playoff_status(team_name):
    database_url = "postgresql://fizcsntuttpigc:01594c15291a6eeaba874716fa449c578d303f263b94082efcce5c29ecbaf579@ec2-18-204-162-101.compute-1.amazonaws.com:5432/dbmcmt26draeuq"
    engine = create_engine(database_url)
    query = f'SELECT "Team", "Conf. Standings"  FROM teams WHERE "Team"=\'{team_name}\';'

    df = pd.read_sql(query, con=engine)

    if not df.empty:
        seed = df.loc[df['Team'] == team_name, 'Conf. Standings'].iloc[0]
        if seed <= 6:
            playoff_status = 'make the playoffs.'
        elif seed <= 10:
            playoff_status = 'make the play-in tournament.'
        else: 
            playoff_status = 'miss the playoffs.'
    return playoff_status