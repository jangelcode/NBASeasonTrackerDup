import requests

url = "https://api-basketball.p.rapidapi.com/statistics"

querystring = {"season":"2023-2024","league":"12","team":"133"}

headers = {
	"X-RapidAPI-Key": "02d9b0d232msh33e360bbdbbf28cp14fc09jsn2aaba1786409",
	"X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())