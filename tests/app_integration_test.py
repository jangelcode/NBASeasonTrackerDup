import pytest
import sys
import os

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

#check home page status code and that it produces expected output
def test_team_selection_and_display(client):
    response = client.post('/', data={'favoriteTeam': 'HAWKS'})
    assert response.status_code == 200
    assert b'Atlanta Hawks' in response.data

#check rankings page status code and check for table
def test_rankings_page(client):
    response = client.get('/rankings')
    assert response.status_code == 200
    assert b'table table-striped' in response.data

#check simulate the playoffs page status code and produce a winner when submit is pushed
def test_playoff_prediction(client):
    form_data = {
        'pointDifferential': '8',
        'pointsPerGame': '8',
        'winPercentage': '6',
        'OPPG': '7',
        'confStandings': '6'
    }
    response = client.post("/Simulate-the-Playoffs", data=form_data)
    assert response.status_code == 200
    assert b"Winner:" in response.data


if __name__ == '__main__':
    pytest.main()

