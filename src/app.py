from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

fav_teams = {
    "Hawks": "Atlanta Hawks",
    "Celtics": "Boston Celtics",
    "Nets": "Brooklyn Nets",
    "Hornets": "Charlotte Hornets",
    "Bulls": "Chicago Bulls",
    "Cavaliers": "Cleveland Cavaliers",
    "Mavericks": "Dallas Mavericks",
    "Nuggets": "Denver Nuggets",
    "Pistons": "Detroit Pistons",
    "Warriors": "Golden State Warriors",
    "Rockets": "Houston Rockets",
    "Pacers": "Indiana Pacers",
    "Clippers": "Los Angeles Clippers",
    "Lakers": "Los Angeles Lakers",
    "Grizzlies": "Memphis Grizzlies",
    "Heat": "Miami Heat",
    "Bucks": "Milwaukee Bucks",
    "Timberwolves": "Minnesota Timberwolves",
    "Pelicans": "New Orleans Pelicans",
    "Knicks": "New York Knicks",
    "Thunder": "Oklahoma City Thunder",
    "Magic": "Orlando Magic",
    "76ers": "Philadelphia 76ers",
    "Suns": "Phoenix Suns",
    "Trail Blazers": "Portland Trail Blazers",
    "Kings": "Sacramento Kings",
    "Spurs": "San Antonio Spurs",
    "Raptors": "Toronto Raptors",
    "Jazz": "Utah Jazz",
    "Wizards": "Washington Wizards"
}

#postgreSQL database URL
database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
engine = create_engine(database_url)

#render home page
@app.route('/', methods=['GET', 'POST'])
def home():
    favorite_team = ""
    if request.method == 'POST':
        favorite_team = request.form['favoriteTeam']
    if favorite_team in fav_teams:
        favorite_team = fav_teams[favorite_team]
    return render_template("index.html", favorite_team=favorite_team)


#rankings page
@app.route("/rankings")
def rankings():
    query = 'SELECT * FROM teams ORDER BY "Pct" DESC;'
    df = pd.read_sql(query, con=engine)
    table_html = df.to_html(classes='table table-striped', index=False, justify='left')
    return render_template("rankings.html", table_html=table_html)

#prediction page
@app.route("/Simulate-the-Playoffs")
def make_a_prediction():
    return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)