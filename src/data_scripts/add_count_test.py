import pytest
from unittest.mock import MagicMock, patch
from add_count import init_count, add_count

@patch('add_count.create_engine')
def test_init_count(mock_create_engine):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    
    # Assuming init_count creates a DataFrame and writes it to SQL, we mock those interactions
    mock_engine.execute = MagicMock()
    mock_engine.dispose = MagicMock()

    df = init_count()
    
    # Verify that create_engine was called with the correct database URL
    mock_create_engine.assert_called_with("postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e")
    
    assert (df["Count"] == 0).all()



# def test_add_count():
#     db_mock = MagicMock()
#     db_mock.execute.return_value = None  # Adjust based on your function's implementation
#     team_name = "Team A"
#     add_count(db_mock, team_name)
#     db_mock.execute.assert_called_with(f'SELECT * FROM searches;', (team_name,))

# def test_add_count_db_error():
#     db_mock = MagicMock()
#     db_mock.execute.side_effect = Exception("Database connection error")
#     with patch('add_count.handle_db_error') as error_handler_mock:
#         add_count(db_mock, "Team A")
#         error_handler_mock.assert_called_once_with("Database connection error")

if __name__ == "__main__":
    pytest.main()
