import pandas as pd
from sqlalchemy import create_engine

def get_playoff_teams(df):

    playoff_picture_east = []
    playoff_picture_west = []
    for index, row in df.iterrows():
        if row["Conf. Standings"] <= 10 and row["Conference"] == 'Eastern Conference':
            playoff_picture_east.append(row["Team"])
        elif row["Conf. Standings"] <= 10:
            playoff_picture_west.append(row["Team"])

    return playoff_picture_east, playoff_picture_west

