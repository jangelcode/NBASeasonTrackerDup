from flask import Flask, request
from sqlalchemy import create_engine
import pandas as pd
from data_scripts.team_data import get_team_data



def predict_winner():
    # Extract slider values from the form
    point_diff_weight = float(request.form['pointDifferential']) / 10
    ppg_weight = float(request.form['pointsPerGame']) / 10
    win_pct_weight = float(request.form['winPercentage']) / 10
    oppg_pct_weight = float(request.form['OPPG']) / 10
    standings_pct_weight = float(request.form['confStandings']) / 10

    
    # Load team data
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)

    query = f'SELECT * FROM teams;'
    team_data = pd.read_sql(query, con=engine)
    team_data_point_diff = (team_data['Point Differential'].astype(float) / max(team_data['Point Differential'].astype(float))) * 10
    team_data_ppg = (team_data['PPG'].astype(float) / max(team_data['PPG'].astype(float))) * 10
    team_data_pct = (team_data['Pct'].astype(float) / max(team_data['Pct'].astype(float))) * 10
    team_data_current_standings = (team_data['Conf. Standings'].astype(float) / max(team_data['Conf. Standings'].astype(float))) * 10
    max_oppg = max(team_data['OPPG'].astype(float))
    team_data_oppg = (1 - (team_data['OPPG'].astype(float) / max_oppg)) * 10
    
    # Calculate weighted score for each team
    team_data['Score'] = round((team_data_point_diff * point_diff_weight) +
                          (team_data_ppg * ppg_weight) +
                          (team_data_pct * win_pct_weight) + 
                          (team_data_oppg * oppg_pct_weight) +
                          (team_data_current_standings * standings_pct_weight), 2)
    # team_data['Score'] = round(team_data['Score'] / max(team_data['Score']) * 10, 2)
    
    # Predict winner as the team with the highest score
    predicted_winner = team_data.loc[team_data['Score'].idxmax(), 'Team']

    prediction_results = team_data[['Team', 'Score']].sort_values(by='Score', ascending=False).head(10)
    
    msg = (f"The predicted NBA Championship winner is: {predicted_winner}")

    return msg, prediction_results