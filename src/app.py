from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# PostgreSQL connection parameters
db_params = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'defense',
}

# Create a connection to PostgreSQL
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')

@app.route("/")
def main():
    # Fetch data from the database
    query = "SELECT * FROM player_career_stats;"
    data_frame = pd.read_sql_query(query, engine)

    # Render the data in an HTML table
    table_html = data_frame.to_html(classes='table table-striped', index=False)

    return f'''
     <h1>NBA Player Career Stats</h1>
     {table_html}
     '''

if __name__ == "__main__":
    app.run(debug=True)


#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <label for="user_input">Enter text:</label>
         <input type="text" id="user_input" name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text