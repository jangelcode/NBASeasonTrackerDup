import pytest
from unittest.mock import MagicMock, patch
from add_count import init_count, add_count

#unit test with mock objects for init_count
@patch('add_count.create_engine')
def test_init_count(mock_create_engine):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    
    #mock database writing
    mock_engine.execute = MagicMock()
    mock_engine.dispose = MagicMock()

    df = init_count()
    
    #verify database URL
    mock_create_engine.assert_called_with("postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e")
    
    #verify counts are all set to 0
    assert (df["Count"] == 0).all()


if __name__ == "__main__":
    pytest.main()
