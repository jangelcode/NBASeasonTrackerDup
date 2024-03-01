import pandas as pd
import pandas as pd
from sqlalchemy import create_engine

def get_playoff_status(team_name):
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)
    query = f"SELECT \"Team\", \"Conf. Standings\"  FROM teams WHERE \"Team\"='{team_name}';"

    df = pd.read_sql(query, con=engine)

    if not df.empty:
        seed = df.loc[df['Team'] == team_name, 'Conf. Standings'].iloc[0]
        if seed <= 6:
            playoff_status = 'make the playoffs.'
        elif seed <= 10:
            playoff_status = 'make the play-in.'
        else: 
            playoff_status = 'miss the playoffs.'
    return playoff_status