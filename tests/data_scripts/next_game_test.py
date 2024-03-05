import pytest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

from data_scripts.next_game import get_next_game_reponse


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

def test_api_response(mocker):
    #mock api response
    mock_get = mocker.patch('data_scripts.next_game.requests.get')
    mock_get.return_value.json.return_value = mock_api_response
    mock_get.return_value.status_code = 200
    
    response = get_next_game_reponse('Boston Celtics')

    #compare API response
    assert response == mock_api_response

if __name__ == "__main__":
    pytest.main()

