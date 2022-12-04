from flask import Flask
import json
from main import app,session

def test_index_route():    
    response = app.test_client().get('/')   
    assert response.status_code == 200

def test_signup_route():    
    response = app.test_client().get('/register')   
    assert response.status_code == 200

def test_login_route():    
    response = app.test_client().get('/login')   
    assert response.status_code == 200


def test_foo_with_client():
    client = app.test_client()
    # session = client.session_transaction()
    client.post('/login', data={'username': 'wasd', 'password': 'wasd'})        
    assert session is not None 

    

