from flask import Flask
import pandas as pd
from sqlalchemy import create_engine
from data_scripts.defense_data import fill_database

app = Flask(__name__)

# Your PostgreSQL database URL
database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"

# Connect to the PostgreSQL database
engine = create_engine(database_url)

@app.route("/")
def main():
    query = "SELECT * FROM your_table_name;"
    df = pd.read_sql(query, con=engine)

    table_html = df.to_html(classes='table table-striped', index=False)

    return f'''
        <html>
            <head>
                <header>Team Stats</header>
            </head>
            <body>
                {table_html}
            </body>
        </html>
        '''

if __name__ == "__main__":
    app.run(debug=True)
