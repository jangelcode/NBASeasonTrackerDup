import requests
import pandas as pd
from sqlalchemy import create_engine
from database import get_database_URI

#connect to api and return response data
def fetch_team_data(team_id):
    url = "https://api-basketball.p.rapidapi.com/standings"
    headers = {
        "X-RapidAPI-Key": "02d9b0d232msh33e360bbdbbf28cp14fc09jsn2aaba1786409",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }
    querystring = {"season": "2023-2024", "league": "12", "team": str(team_id)}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data


def extract_team_info(data):
    team_info = data['response'][0][0]['team']
    conference_info = data['response'][0][0]['group']
    games_info = data['response'][0][0]['games']
    points_info = data['response'][0][0]['points']
    
    row_data = {
        #set row values equal to corresponding api data
        'Team': team_info['name'],
        'Conf. Standings': data['response'][0][0]['position'],
        'Conference': conference_info['name'],
        'Wins': games_info['win']['total'],
        'Loses': games_info['lose']['total'],
        'Played': games_info['played'],
        'Pct': games_info['win']['percentage'],
        'Points Scored': points_info['for'],
        'Points Allowed': points_info['against'],

        #calculate point diff, ppg, and oppg from data we've taken from the api
        'Point Differential': points_info['for'] - points_info['against'],
        'PPG': round(points_info['for'] / games_info['played'], 1),
        'OPPG': round(points_info['against'] / games_info['played'], 1),
    }
    
    return row_data

#combine data into a dataframe
def aggregate_team_data():
    team_ids = range(132, 162)
    all_data = pd.DataFrame()

    for team_id in team_ids:
        data = fetch_team_data(team_id)
        row_data = extract_team_info(data)
        
        if not all_data.empty:
            all_data = pd.concat([all_data, pd.DataFrame([row_data])], ignore_index=True)
        else:
            all_data = pd.DataFrame([row_data])
    
    return all_data

#push all the team data to postgres
def store_team_data(data_frame):
    database_url = get_database_URI()
    engine = create_engine(database_url)
    data_frame.to_sql('teams', con=engine, index=False, if_exists='replace')
    engine.dispose()


def get_team_data():
    all_data = aggregate_team_data()
    store_team_data(all_data)
    return all_data

#when this script is called with heroku scheduler it will run the get_team_data function
get_team_data()
