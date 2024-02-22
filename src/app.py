from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Use the database URL provided by Heroku
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e'

db = SQLAlchemy(app)

@app.route("/")
def main():
    # Fetch data from the database
    query = "SELECT * FROM player_career_stats;"
    data_frame = pd.read_sql_query(query, db.engine)

    # Show the data in an HTML table
    table_html = data_frame.to_html(classes='table table-striped', index=False)

    return f'''
     <h1>NBA Player Career Stats for Nikola Jokic</h1>
     {table_html}
     '''

if __name__ == "__main__":
    app.run(debug=True)
