from flask import Flask
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

        # Extract relevant information from the API response
        team_data = data.get('response', {}).get('team', {})
        player_stats = team_data

        # Create a DataFrame from the player_stats list
        df = pd.DataFrame(player_stats)
        print(df)

        # Create HTML table for data
        table_html = df.to_html(classes='table table-striped', index=False)

        # Render HTML directly within the Python code
        return f'''
        <html>
            <head>
                <title>NBA Player Career Stats for Nikola Jokic</title>
            </head>
            <body>
                <h1>NBA Player Career Stats for Nikola Jokic</h1>
                {table_html}
            </body>
        </html>
        '''
    else:
        # Handle the case where the API request was not successful
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    app.run(debug=True)


