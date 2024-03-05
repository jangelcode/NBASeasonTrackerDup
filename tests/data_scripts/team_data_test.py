import pytest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
import os
import sys

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
src_path = os.path.join(parent_dir, 'src')
sys.path.append(src_path)

from data_scripts.team_data import fetch_team_data, store_team_data

#mock the requests.get function to test api response
def test_fetch_team_data(mocker):
    mocked_get = mocker.patch('requests.get')
    mocked_get.return_value.json.return_value = {"expected": "data"}
    data = fetch_team_data(132)
    assert data == {"expected": "data"}

#test that the function attempts to store data in a database once
def test_store_team_data(mocker):
    mock_to_sql = mocker.patch('pandas.DataFrame.to_sql')
    sample_df = DataFrame({
        "team_id": [132, 133],
        "team_name": ["Atlanta Hawks", "Boston Celtics"],
    })
    store_team_data(sample_df)
    mock_to_sql.assert_called_once()

if __name__ == "__main__":
    pytest.main()
