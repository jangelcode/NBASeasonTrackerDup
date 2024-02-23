import requests
import pandas as pd
from sqlalchemy import create_engine

# Your Heroku PostgreSQL database URL
def fill_database():
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"

    url = "https://api-basketball.p.rapidapi.com/statistics"

    headers = {
        "X-RapidAPI-Key": "02d9b0d232msh33e360bbdbbf28cp14fc09jsn2aaba1786409",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }

    # Define the range of team IDs
    team_ids = range(132, 162)

    # Create an empty DataFrame to store all the data
    all_data = pd.DataFrame()

    for team_id in team_ids:
        querystring = {"season": "2023-2024", "league": "12", "team": str(team_id)}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        print(data['response']['team']['name'])
        
        # Extracting relevant data
        team_info = data['response']['team']
        games_info = data['response']['games']
        points_info = data['response']['points']
        
        # Create a dictionary to represent a single row
        row_data = {
            'Team': team_info['name'],
            'Games_Played_Home': games_info['played']['home'],
            'Games_Played_Away': games_info['played']['away'],
            'Games_Played_All': games_info['played']['all'],
            'Wins_Home': games_info['wins']['home']['total'],
            'Wins_Away': games_info['wins']['away']['total'],
            'Wins_All': games_info['wins']['all']['total'],
            'Draws_Home': games_info['draws']['home']['total'],
            'Draws_Away': games_info['draws']['away']['total'],
            'Draws_All': games_info['draws']['all']['total'],
            'Loses_Home': games_info['loses']['home']['total'],
            'Loses_Away': games_info['loses']['away']['total'],
            'Loses_All': games_info['loses']['all']['total'],
            'Points_For_Home': points_info['for']['total']['home'],
            'Points_For_Away': points_info['for']['total']['away'],
            'Points_For_All': points_info['for']['total']['all'],
            'Points_Against_Home': points_info['against']['total']['home'],
            'Points_Against_Away': points_info['against']['total']['away'],
            'Points_Against_All': points_info['against']['total']['all'],
        }
        
        # Append the row to the DataFrame
        if not all_data.empty:
            all_data.loc[team_id-132] = row_data
        else:
            all_data = pd.DataFrame([row_data])

    # Connect to the PostgreSQL database
    engine = create_engine(database_url)

    # Insert the data into the database
    all_data.to_sql('your_table_name', con=engine, index=False, if_exists='replace')

    # Close the database connection
    engine.dispose()

fill_database()
