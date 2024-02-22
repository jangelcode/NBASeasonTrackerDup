from nba_api.stats.static import teams

# Retrieve list of all teams information
all_teams = teams.get_teams()

# Extract team IDs from each team
team_ids = [team['id'] for team in all_teams]

print(team_ids)