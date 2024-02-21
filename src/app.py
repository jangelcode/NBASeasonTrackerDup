import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql  # Import the PostgreSQL dialect
import pandas as pd

app = Flask(__name__)

# Use the DATABASE_URL environment variable provided by Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to suppress a warning

db = SQLAlchemy(app)

@app.route("/")
def main():
    # Fetch data from the database
    query = "SELECT * FROM player_career_stats;"
    data_frame = pd.read_sql_query(query, db.engine)

    # Render the data in an HTML table
    table_html = data_frame.to_html(classes='table table-striped', index=False)

    return f'''
     <h1>NBA Player Career Stats</h1>
     {table_html}
     '''

if __name__ == "__main__":
    app.run(debug=True)
