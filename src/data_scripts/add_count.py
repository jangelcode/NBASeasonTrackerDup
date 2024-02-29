import pandas as pd
from sqlalchemy import create_engine, text

#initialize the database that holds search counts for each team
def init_count():
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)
    query = f'SELECT "Team" FROM teams;'

    df = pd.read_sql(query, con=engine)
    df["Count"] = 0

    df.to_sql('searches', con=engine, index=False, if_exists='replace')
    engine.dispose()

    return df

#add to the count and save it to the database after each team search
def add_count(team_name: str):
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)

    query = f'SELECT * FROM searches'
    df = pd.read_sql(query, con=engine)

    df.loc[df['Team'] == team_name, 'Count'] += 1
    count = df.loc[df['Team'] == team_name, 'Count'].iloc[0]
    df.to_sql('searches', con=engine, index=False, if_exists='replace')
    
    engine.dispose()

    return count
