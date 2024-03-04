import pytest
from app import app  # Ensure this correctly imports your Flask app instance

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

