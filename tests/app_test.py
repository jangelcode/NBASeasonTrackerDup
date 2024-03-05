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

def test_main_route(client):
    """Test the main route to ensure it returns a status code of 200 and contains the expected content."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<h2>Home</h2>' in response.data

if __name__ == '__main__':
    pytest.main()

