from unittest.mock import patch, MagicMock
import pytest
import sys
import os

# Calculate the path to the src directory and add it to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

# Now you can import next_game as if it were directly accessible
from data_scripts.next_game import get_next_game_reponse

# Your test code goes here


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

@patch('data_scripts.next_game.requests.get')
def test_api_response(mock_get):
    #mock setup
    mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_api_response)
    response = get_next_game_reponse('Boston Celtics')

    #compare API response
    assert response == mock_api_response

if __name__ == "__main__":
    pytest.main()

