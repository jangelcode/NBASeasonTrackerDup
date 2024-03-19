import pandas as pd
from sqlalchemy import create_engine, text
from database import get_database_URI

#initialize the database that holds search counts for each team
def init_count():
    database_url = get_database_URI()
    engine = create_engine(database_url)
    query = f'SELECT "Team" FROM teams;'

    df = pd.read_sql(query, con=engine)
    df["Count"] = 0

    df.to_sql('searches', con=engine, index=False, if_exists='replace')
    engine.dispose()

    return df

#add to the count and save it to the database after each team search
def add_count(team_name: str):
    database_url = get_database_URI()
    engine = create_engine(database_url)

    query = f'SELECT * FROM searches;'
    df = pd.read_sql(query, con=engine)

    df.loc[df['Team'] == team_name, 'Count'] += 1
    count = df.loc[df['Team'] == team_name, 'Count'].iloc[0]
    df.to_sql('searches', con=engine, index=False, if_exists='replace')
    
    engine.dispose()

    return count
