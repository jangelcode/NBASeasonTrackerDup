import requests
import pandas as pd
from sqlalchemy import create_engine

def get_team_data():
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    url = "https://api-basketball.p.rapidapi.com/standings"
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
        team_info = data['response'][0][0]['team']
        conference_info = data['response'][0][0]['group']
        games_info = data['response'][0][0]['games']
        points_info = data['response'][0][0]['points']
        
        #create dictionary
        row_data = {
            'Team': team_info['name'],
            'Conf. Standings': data['response'][0][0]['position'],
            'Conference': conference_info['name'],
            'Wins': games_info['win']['total'],
            'Loses': games_info['lose']['total'],
            'Played': games_info['played'],
            'Pct': games_info['win']['percentage'],
            'Points Scored': points_info['for'],
            'Points Allowed': points_info['against'],
            'Point Differential': points_info['for'] - points_info['against'],
            'PPG': round(points_info['for'] / games_info['played'], 1),
            'OPPG': round(points_info['against'] / games_info['played'], 1),
        }
        
        #add to dataframe
        if not all_data.empty:
            all_data.loc[team_id-132] = row_data
        else:
            all_data = pd.DataFrame([row_data])
        
        print(team_info['name'])

    engine = create_engine(database_url)
    all_data.to_sql('teams', con=engine, index=False, if_exists='replace')
    engine.dispose()

get_team_data()
