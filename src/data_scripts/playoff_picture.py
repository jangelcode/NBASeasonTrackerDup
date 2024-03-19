import pandas as pd
from sqlalchemy import create_engine
from database import get_database_URI

#pull teams, standings, and conference from database
def get_playoff_teams():
    database_url = get_database_URI()
    engine = create_engine(database_url)
    query = f'SELECT "Team", "Conf. Standings", "Conference" FROM teams;'

    df = pd.read_sql(query, con=engine)
    engine.dispose()

    return get_teams_by_conference(df)

# pull playoff teams from each conference
def get_teams_by_conference(df):
    playoff_picture_east = []
    playoff_picture_west = []

    for index, row in df.iterrows():
        if row["Conf. Standings"] <= 10 and row["Conference"] == 'Eastern Conference':
            playoff_picture_east.append(row["Team"])
        elif row["Conf. Standings"] <= 10:
            playoff_picture_west.append(row["Team"])

    return playoff_picture_east, playoff_picture_west

## FILE NOT CURRENTLY IN USE. TO BE IMPLEMENTED AT A LATER DATE.