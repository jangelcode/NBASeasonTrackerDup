import pytest
import sys
import os

# Calculate the path to the src directory and add it to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

from data_scripts.add_count import init_count
import warnings

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")

# Use the mocker fixture provided by pytest-mock
def test_init_count(mocker):
    mock_create_engine = mocker.patch('data_scripts.add_count.create_engine')
    mock_engine = mocker.MagicMock()
    mock_create_engine.return_value = mock_engine

    # Mock database writing
    mock_engine.execute = mocker.MagicMock()
    mock_engine.dispose = mocker.MagicMock()

    df = init_count()
    
    #verify database URL
    mock_create_engine.assert_called_with("postgresql://pcvqvgmijraryx:26c43ba15b78faf8bbf3b162d8f743b9ec3d741cabd07856f210bd7b0fc82dd8@ec2-34-230-120-83.compute-1.amazonaws.com:5432/d2m4f9jdj48v0e")
    
    #verify counts are all set to 0
    assert (df["Count"] == 0).all()


if __name__ == "__main__":
    pytest.main()
