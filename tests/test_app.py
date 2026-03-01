# tests/test_app.py
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
import create_db

@pytest.fixture
def client():
    with app.app_context():
        create_db.create_database() 
    
    with app.test_client() as client:
        yield client
    
    if os.path.exists('instance/todo.db'):
        os.remove('instance/todo.db')

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200