from nba_api.stats.static import teams

# Retrieve all teams
all_teams = teams.get_teams()

# Extract team IDs from the response
team_ids = [team['id'] for team in all_teams]

# Print or use the list of team IDs
print(team_ids)