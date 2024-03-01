from unittest.mock import patch, MagicMock
import pytest
import next_game

#set api response for boston celtics
mock_api_response = {
    "get": "games",
    "parameters": {
        "league": "12",
        "season": "2023-2024",
        "team": "133"
    },
    "errors": [],
    "results": 86,
}

@patch('next_game.requests.get')
def test_api_response(mock_get):
    #mock setup
    mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_api_response)
    response = next_game.get_next_game_reponse('Boston Celtics')

    #compare API response
    assert response == mock_api_response

if __name__ == "__main__":
    pytest.main()

