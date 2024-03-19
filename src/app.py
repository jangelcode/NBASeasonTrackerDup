from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine
from data_scripts.add_count import add_count
from data_scripts.playoff_status import get_playoff_status
from data_scripts.next_game import get_next_game
from data_scripts.simulate_playoffs import predict_winner
from data_scripts.database import get_database_URI

app = Flask(__name__)

teams = {
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
database_url = get_database_URI()
engine = create_engine(database_url)

#render home page
@app.route('/', methods=['GET', 'POST'])
def home():
    favorite_team, team_info, playoff_status, error_message = "", "", "", ""
    date, time, timezone, opponent = "", "", "", ""
    count_info, plusMinus, avg_plusminus = 0, 0, 0

    if request.method == 'POST':
        #if valid name entry
        if request.form['favoriteTeam'].upper() in teams:
            favorite_team = teams[request.form['favoriteTeam'].upper()]
            count_info = add_count(favorite_team)
            playoff_status = get_playoff_status(favorite_team)
            next_game = get_next_game(favorite_team)
            date = next_game['Date']
            time = next_game['Time']
            timezone = next_game['Timezone']
            opponent = next_game['Opponent']
            #query point differential
            query = f"SELECT \"Point Differential\" FROM teams WHERE \"Team\"='{favorite_team}';"
            ptdiff = pd.read_sql(query, con=engine)
            plusMinus = ptdiff.loc[0, 'Point Differential']
            #query games played
            query = f"SELECT \"Played\" FROM teams WHERE \"Team\"='{favorite_team}';"
            played = pd.read_sql(query, con=engine)
            total_played = played.loc[0, 'Played']
            avg_plusminus = round(plusMinus / total_played, 1)
        else:
            error_message = "Invalid team name entered. Please try again."
    return render_template("index.html", favorite_team=favorite_team, team_info=team_info, error_message=error_message, count_info=count_info, 
                           playoff_status=playoff_status, date=date, time=time, timezone=timezone, opponent=opponent, plusMinus=plusMinus, avg_plusminus=avg_plusminus)


#rankings page
@app.route("/rankings")
def rankings():
    query = 'SELECT * FROM teams ORDER BY "Pct" DESC;'
    df = pd.read_sql(query, con=engine)
    #convert table
    table_html = df.to_html(classes='table table-striped', index=False, justify='left')
    return render_template("rankings.html", table_html=table_html)


@app.route("/Simulate-the-Playoffs", methods=['GET', 'POST'])
def make_a_prediction():
    if request.method == 'POST':
        #call predict_winner to get the prediction
        winner_prediction = predict_winner()[0]
        winner_table = predict_winner()[1].to_html(classes='table table-striped', index=False, justify='left')
        #pass the prediction to the template to display it
        return render_template("prediction.html", winner_prediction=winner_prediction, winner_table=winner_table)
    return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)
