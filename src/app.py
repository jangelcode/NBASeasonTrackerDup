from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

#postgreSQL database URL
database_url = "postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e"
engine = create_engine(database_url)

#render home page
@app.route("/")
def home():
    return render_template("index.html")

#rankings page
@app.route("/rankings")
def rankings():
    query = 'SELECT * FROM teams ORDER BY "Pct" DESC;'
    df = pd.read_sql(query, con=engine)
    table_html = df.to_html(classes='table table-striped', index=False, justify='left')
    return render_template("rankings.html", table_html=table_html)

#prediction page
@app.route("/make-a-prediction")
def make_a_prediction():
    return render_template("prediction.html")


if __name__ == "__main__":
    app.run(debug=True)