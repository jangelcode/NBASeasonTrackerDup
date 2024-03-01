from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine
from data_scripts.add_count import add_count
from data_scripts.playoff_status import get_playoff_status

app = Flask(__name__)

fav_teams = {
    'HAWKS': 'Atlanta Hawks',
    'CELTICS': 'Boston Celtics',
    'NETS': 'Brooklyn Nets',
    'HORNETS': 'Charlotte Hornets',
    'BULLS': 'Chicago Bulls',
    'CAVALIERS': 'Cleveland Cavaliers',
    'MAVERICKS': 'Dallas Mavericks',
    'NUGGETS': 'Denver Nuggets',
    'PISTONS': 'Detroit Pistons',
    'WARRIORS': 'Golden State Warriors',
    'ROCKETS': 'Houston Rockets',
    'PACERS': 'Indiana Pacers',
    'CLIPPERS': 'Los Angeles Clippers',
    'LAKERS': 'Los Angeles Lakers',
    'GRIZZLIES': 'Memphis Grizzlies',
    'HEAT': 'Miami Heat',
    'BUCKS': 'Milwaukee Bucks',
    'TIMBERWOLVES': 'Minnesota Timberwolves',
    'PELICANS': 'New Orleans Pelicans',
    'KNICKS': 'New York Knicks',
    'THUNDER': 'Oklahoma City Thunder',
    'MAGIC': 'Orlando Magic',
    '76ERS': 'Philadelphia 76ers',
    'SUNS': 'Phoenix Suns',
    'TRAIL BLAZERS': 'Portland Trail Blazers',
    'KINGS': 'Sacramento Kings',
    'SPURS': 'San Antonio Spurs',
    'RAPTORS': 'Toronto Raptors',
    'JAZZ': 'Utah Jazz',
    'WIZARDS': 'Washington Wizards'
}

#postgreSQL database URL
database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
engine = create_engine(database_url)

#render home page
@app.route('/', methods=['GET', 'POST'])
def home():
    favorite_team = ""
    team_info = ""
    playoff_status = ""
    error_message = ""
    count_info = 0
    if request.method == 'POST':
        if request.form['favoriteTeam'].upper() in fav_teams:
            favorite_team = fav_teams[request.form['favoriteTeam'].upper()]
            count_info = add_count(favorite_team)
            playoff_status = get_playoff_status(favorite_team)
        else:
            error_message = "Invalid team name entered. Please try again."
    return render_template("index.html", favorite_team=favorite_team, team_info=team_info, error_message=error_message, count_info=count_info, 
                           playoff_status=playoff_status)


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