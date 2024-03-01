# test_next_game.py
import pytest
from unittest.mock import patch

from sqlalchemy import null
import next_game

# Sample mock API responses
mock_response_success = {
    "api": {
        "results": 1,
        "fixtures": [
            {
                "fixture_id": 593515,
                "league_id": 140,
                "league": {
                    "name": "Premier League",
                    "country": "England",
                    "logo": "https://example.com/premier-league-logo.png",
                    "flag": None,
                },
                "event_date": "2023-04-01T12:30:00+00:00",
                "event_timestamp": 1617275400,
                "firstHalfStart": 1617275400,
                "secondHalfStart": 1617279000,
                "round": "Regular Season - 31",
                "status": "NS",
                "statusShort": "NS",
                "elapsed": 0,
                "venue": "Emirates Stadium",
                "homeTeam": {
                    "team_id": 42,
                    "team_name": "Arsenal",
                    "logo": "https://example.com/arsenal-logo.png",
                },
                "awayTeam": {
                    "team_id": 33,
                    "team_name": "Liverpool",
                    "logo": "https://example.com/liverpool-logo.png",
                },
                "goalsHomeTeam": null,
                "goalsAwayTeam": null,
            }
        ],
    }
}

mock_response_error = {"message": "An error occurred"}

@pytest.mark.parametrize("team_name,expected", [
    ("Arsenal", "Arsenal vs Liverpool on 2023-04-01T12:30:00+00:00 at Emirates Stadium"),
    ("NonExistingTeam", None),  # Assuming function returns None for non-existing teams
])
@patch('next_game.requests.get')
def test_get_next_game(mock_get, team_name, expected):
    # Mock the .get() method's return value depending on the team_name
    if team_name == "NonExistingTeam":
        mock_get.return_value.json.return_value = mock_response_error
        mock_get.return_value.status_code = 404
    else:
        mock_get.return_value.json.return_value = mock_response_success
        mock_get.return_value.status_code = 200

    # Call the function with the mocked API response
    result = next_game.get_next_game(team_name)

    # Assert the expected outcome
    assert result == expected

if __name__ == "__main__":
    pytest.main()
