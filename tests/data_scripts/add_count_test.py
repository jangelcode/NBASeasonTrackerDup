import pytest
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

from data_scripts.add_count import init_count
import warnings

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")

#mock database connection
def test_init_count(mocker):
    mock_create_engine = mocker.patch('data_scripts.add_count.create_engine')
    mock_engine = mocker.MagicMock()
    mock_create_engine.return_value = mock_engine

    #mock database writing
    mock_engine.execute = mocker.MagicMock()
    mock_engine.dispose = mocker.MagicMock()

    df = init_count()
    
    #verify database URL
    mock_create_engine.assert_called_with("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    
    #verify counts are all set to 0
    assert (df["Count"] == 0).all()


if __name__ == "__main__":
    pytest.main()
