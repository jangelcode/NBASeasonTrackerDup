from flask import request
from sqlalchemy import create_engine
import pandas as pd


def scale_data(series, invert=False):
    # Scale data to a 0-10 range. Invert if lower values are considered better.
    if invert:
        scaled_series = (1 - (series - series.min()) / (series.max() - series.min())) * 10
    else:
        scaled_series = ((series - series.min()) / (series.max() - series.min())) * 10
    return scaled_series


def get_playoff_weights():
    # Extract slider values from the form
    point_diff_weight = float(request.form['pointDifferential']) / 10
    ppg_weight = float(request.form['pointsPerGame']) / 10
    win_pct_weight = float(request.form['winPercentage']) / 10
    oppg_pct_weight = float(request.form['OPPG']) / 10
    standings_pct_weight = float(request.form['confStandings']) / 10

    return point_diff_weight, ppg_weight, win_pct_weight, oppg_pct_weight, standings_pct_weight


def get_playoff_data():
    # Load team data
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)
    query = f'SELECT "Team", "Point Differential", "PPG", "Pct", "OPPG", "Conf. Standings" FROM teams;'
    team_data = pd.read_sql(query, con=engine)
    team_data = team_data.apply(lambda x: x.astype(float) if x.name != 'Team' else x)
    return team_data


def calculate_team_scores(team_data, weights):
    """Calculate weighted scores for each team based on scaled team data and weights."""
    # Scale team statistics
    team_data['Point Differential'] = scale_data(team_data['Point Differential'])
    team_data['PPG'] = scale_data(team_data['PPG'])
    team_data['Pct'] = scale_data(team_data['Pct'])
    team_data['OPPG'] = scale_data(team_data['OPPG'], invert=True)  # Invert since lower is better
    team_data['Conf. Standings'] = scale_data(team_data['Conf. Standings'], invert=True)  # Invert standings
    
    # Apply weights
    point_diff_weight, ppg_weight, win_pct_weight, oppg_pct_weight, standings_pct_weight = weights
    team_data['Score'] = round((team_data['Point Differential'] * point_diff_weight) +
                               (team_data['PPG'] * ppg_weight) +
                               (team_data['Pct'] * win_pct_weight) + 
                               (team_data['OPPG'] * oppg_pct_weight) +
                               (team_data['Conf. Standings'] * standings_pct_weight), 2)
    return team_data


def predict_winner():
    team_data = get_playoff_data()
    weights = get_playoff_weights()
    scored_teams = calculate_team_scores(team_data, weights)
    predicted_winner = scored_teams.loc[scored_teams['Score'].idxmax(), 'Team']
    prediction_results = scored_teams[['Team', 'Score']].sort_values(by='Score', ascending=False).head(10)
    msg = f"The predicted NBA Championship winner is: {predicted_winner}"
    return msg, prediction_results
