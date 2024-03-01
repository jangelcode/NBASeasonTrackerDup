import requests

teams = {
    'Atlanta Hawks': 132,
    'Boston Celtics': 133,
    'Brooklyn Nets': 134,
    'Charlotte Hornets': 135,
    'Chicago Bulls': 136,
    'Cleveland Cavaliers': 137,
    'Dallas Mavericks': 138,
    'Denver Nuggets': 139,
    'Detroit Pistons': 140,
    'Golden State Warriors': 141,
    'Houston Rockets': 142,
    'Indiana Pacers': 143,
    'Los Angeles Clippers': 144,
    'Los Angeles Lakers': 145,
    'Memphis Grizzlies': 146,
    'Miami Heat': 147,
    'Milwaukee Bucks': 148,
    'Minnesota Timberwolves': 149,
    'New Orleans Pelicans': 150,
    'New York Knicks': 151,
    'Oklahoma City Thunder': 152,
    'Orlando Magic': 153,
    'Philadelphia 76ers': 154,
    'Phoenix Suns': 155,
    'Portland Trail Blazers': 156,
    'Sacramento Kings': 157,
    'San Antonio Spurs': 158,
    'Toronto Raptors': 159,
    'Utah Jazz': 160,
    'Washington Wizards': 161
}

def get_next_game_reponse(team_name):
    url = "https://api-basketball.p.rapidapi.com/games"
    headers = {
        "X-RapidAPI-Key": "02d9b0d232msh33e360bbdbbf28cp14fc09jsn2aaba1786409",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }
    if team_name not in teams:
        return None
    
    querystring = {"season": "2023-2024", "league": "12", "team": str(teams[team_name])}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

def get_next_game(team_name):
    data = get_next_game_reponse(team_name)

    for i in range(0, data['results']):
        if data['response'][i]['status']['short'] == "FT":
            continue
        elif data['response'][i]['status']['short'] == "NS":
            game_data = {
            'Date': data['response'][i]['date'][0:10],
            'Time': data['response'][i]['time'][0:5],
            'Timezone': data['response'][i]['timezone'],
            }
            if data['response'][i]['teams']['home']['name'] != team_name:
                game_data['Opponent'] = data['response'][i]['teams']['home']['name']
            else:
                game_data['Opponent'] = data['response'][i]['teams']['away']['name']
            return game_data
