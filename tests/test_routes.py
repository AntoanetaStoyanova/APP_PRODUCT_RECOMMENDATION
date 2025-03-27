
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    return app

def test_home(app):
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
