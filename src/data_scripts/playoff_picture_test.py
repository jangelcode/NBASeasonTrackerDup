import pandas as pd
import pytest
from playoff_picture import get_teams_by_conference


def test_get_teams_by_conference():
    eastern_conf = ['Eastern Conference'] * 15
    eastern_standings = list(range(1, 16))
    eastern_teams = [f'Team {i}' for i in eastern_standings]

    western_conf = ['Western Conference'] * 15
    western_standings = list(range(1, 16))
    western_teams = [f'Team {i}' for i in western_standings]

    #create sample dataframe with teams, conferences, and respective standings
    fake_df = pd.DataFrame({
        'Conference': eastern_conf + western_conf,
        'Conf. Standings': eastern_standings + western_standings,
        'Team': eastern_teams + western_teams
    })

    expected = (['Team 1','Team 2','Team 3','Team 4','Team 5','Team 6','Team 7','Team 8','Team 9','Team 10'],
                ['Team 1','Team 2','Team 3','Team 4','Team 5','Team 6','Team 7','Team 8','Team 9','Team 10'])

    assert get_teams_by_conference(fake_df) == expected

if __name__ == "__main__":
    pytest.main()


