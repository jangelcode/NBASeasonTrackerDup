from nba_api.stats.endpoints import teams

# Retrieve all teams
all_teams = teams.Teams()

# Extract team IDs from the response
team_ids = [team['teamId'] for team in all_teams.data['teams']]

# Print or use the list of team IDs
print(team_ids)