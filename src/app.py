import os
from flask import Flask, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)

# Use the DATABASE_URL environment variable provided by Heroku
db_url = os.environ.get('DATABASE_URL')

# Create a connection to PostgreSQL
engine = create_engine(db_url)

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
