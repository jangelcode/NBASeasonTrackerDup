from unittest.mock import patch, MagicMock
import pytest
import next_game  # Replace with the name of your module

# The specific API response you want to test
mock_api_response = {
    "get": "games",
    "parameters": {
        "league": "12",
        "season": "2023-2024",
        "team": "133"
    },
    "errors": [],
    "results": 86,
    "response": '[] 86 items'
}

@patch('next_game.requests.get')
def test_api_response(mock_get):
    # Set up the mock to return your specific API response
    mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_api_response)

    # Call your function here. Replace 'your_function' with the actual function you're testing
    response = next_game.get_next_game_reponse('Boston Celtics')  # Adjust this call to match your actual function's signature

    # Check that the function returns the expected API response
    assert response == mock_api_response

if __name__ == "__main__":
    pytest.main()

