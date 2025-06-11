import pytest
from app import create_app, db
from app.config import TestingConfig
from app.models.user import User

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful! Please login.' in response.data

def test_login(client):
    # First register a user
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    # Then try to login
    response = client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Check for dashboard or index page content
    assert b'Task Manager' in response.data or b'dashboard' in response.data

def test_logout(client):
    # First register and login
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123'
    })
    # Then try to logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    # Check for index page content
    assert b'Task Manager' in response.data or b'dashboard' in response.data 