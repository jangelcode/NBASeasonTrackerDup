from flask import Flask, request
from sqlalchemy import create_engine
import pandas as pd
from data_scripts.team_data import get_team_data



def predict_winner():
    # Extract slider values from the form
    point_diff_weight = float(request.form['pointDifferential'])
    ppg_weight = float(request.form['pointsPerGame'])
    win_pct_weight = float(request.form['winPercentage'])
    
    # Load team data
    database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
    engine = create_engine(database_url)

    query = f'SELECT * FROM teams;'
    team_data = pd.read_sql(query, con=engine) # Assuming this function returns a DataFrame
    
    # Calculate weighted score for each team
    team_data['Score'] = round((team_data['Point Differential'].astype(float) / team_data['Played'].astype(float) * 10 * point_diff_weight/10) +
                          (team_data['PPG'].astype(float) * ppg_weight/10) +
                          (team_data['Pct'].astype(float)* 100 * win_pct_weight/10), 2)
    
    # Predict winner as the team with the highest score
    predicted_winner = team_data.loc[team_data['Score'].idxmax(), 'Team']

    prediction_results = team_data[['Team', 'Score']].sort_values(by='Score', ascending=False).head(10)
    
    msg = ( f"The predicted NBA Championship winner is: {predicted_winner} {max(team_data['Score'])}")

    return msg, prediction_results