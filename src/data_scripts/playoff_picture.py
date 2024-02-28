import pandas as pd
import psycopg2
from sqlalchemy import create_engine

#connect database
database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
engine = create_engine(database_url)

#create dataframe from SQL query
query = 'SELECT "Team", "Conf. Standings", "Conference" FROM teams ORDER BY "Conference", "Conf. Standings";'
df = pd.read_sql(query, engine)
engine.dispose()

playoff_picture_east = []
playoff_picture_west = []
for index, row in df.iterrows():
    if row["Conf. Standings"] <= 10 and row["Conference"] == 'Eastern Conference':
        playoff_picture_east.append([row["Conf. Standings"], row["Team"]])
    elif row["Conf. Standings"] <= 10:
        playoff_picture_west.append([row["Conf. Standings"], row["Team"]])

print(playoff_picture_east)
print(playoff_picture_west)

