import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Calculate the path to the src directory and add it to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

# Now you can import next_game as if it were directly accessible
from data_scripts.add_count import init_count
import warnings

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")


#unit test with mock objects for init_count
@patch('data_scripts.add_count.create_engine')
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
