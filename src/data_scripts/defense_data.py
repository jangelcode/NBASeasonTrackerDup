import requests
import pandas as pd
from sqlalchemy import create_engine

def fill_database():
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"

    url = "https://api-basketball.p.rapidapi.com/statistics"

    headers = {
        "X-RapidAPI-Key": "02d9b0d232msh33e360bbdbbf28cp14fc09jsn2aaba1786409",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }

    #init data frame and apis team ids
    team_ids = range(132, 162)
    all_data = pd.DataFrame()

    for team_id in team_ids:
        querystring = {"season": "2023-2024", "league": "12", "team": str(team_id)}
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        #extract data from response categories
        team_info = data['response']['team']
        games_info = data['response']['games']
        points_info = data['response']['points']
        
        #create dictionary
        row_data = {
            'Team': team_info['name'],
            'Games Played (H)': games_info['played']['home'],
            'Games Played (A)': games_info['played']['away'],
            'Games Played': games_info['played']['all'],
            'Wins (H)': games_info['wins']['home']['total'],
            'Wins (A)': games_info['wins']['away']['total'],
            'Wins': games_info['wins']['all']['total'],
            'Loses (H)': games_info['loses']['home']['total'],
            'Loses (A)': games_info['loses']['away']['total'],
            'Loses': games_info['loses']['all']['total'],
            'Points (H)': points_info['for']['total']['home'],
            'Points (A)': points_info['for']['total']['away'],
            'Total Points': points_info['for']['total']['all'],
            'Points by opp (H)': points_info['against']['total']['home'],
            'Points by opp (A)': points_info['against']['total']['away'],
            'Total points (opp)': points_info['against']['total']['all'],
        }
        
        #add to dataframe
        if not all_data.empty:
            all_data.loc[team_id-132] = row_data
        else:
            all_data = pd.DataFrame([row_data])

    engine = create_engine(database_url)
    all_data.to_sql('teams', con=engine, index=False, if_exists='replace')
    engine.dispose()

fill_database()
