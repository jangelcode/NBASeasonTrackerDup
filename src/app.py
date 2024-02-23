from flask import Flask, render_template
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/")
def main():
    # API request to get data
    url = "https://api-basketball.p.rapidapi.com/statistics"
    querystring = {"season": "2023-2024", "league": "12", "team": "133"}
    headers = {
        "X-RapidAPI-Key": "02d9b0d232msh33e360bbdbbf28cp14fc09jsn2aaba1786409",
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract relevant information from the API response and create a Pandas DataFrame
        # Adjust the code based on the actual structure of the API response
        # For example, if the data is nested under a specific key, use data['key']
        df = pd.DataFrame(data['response'])

        # Create HTML table for data
        table_html = df.to_html(classes='table table-striped', index=False)

        return render_template('index.html', table_html=table_html)

    else:
        # Handle the case where the API request was not successful
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    app.run(debug=True)

