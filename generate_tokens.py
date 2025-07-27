import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def signup_user(username, email, password, role="user"):
    """Sign up a new user"""
    signup_data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    
    if response.status_code == 200:
        print(f"User {username} created successfully")
        return True
    elif response.status_code == 400 and "already exists" in response.text:
        print(f"User {username} already exists")
        return True
    else:
        print(f"Signup failed for {username}: {response.status_code} - {response.text}")
        return False

def login_and_get_token(username, password):
    """Login and get JWT token"""
    login_data = {
        "username": username,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Login failed for {username}: {response.status_code} - {response.text}")
        return None

def main():
    # Test users to create
    test_users = [
        {"username": "testuser", "email": "testuser@example.com", "password": "password123", "role": "user"},
        {"username": "admin", "email": "admin@example.com", "password": "admin123", "role": "admin"}
    ]
    
    print("Creating users and generating JWT tokens...")
    print("=" * 50)
    
    for user in test_users:
        # First, try to create the user
        if signup_user(user["username"], user["email"], user["password"], user["role"]):
            # Then get the token
            token = login_and_get_token(user["username"], user["password"])
            if token:
                print(f"Token for {user['username']}:")
                print(f'"{token}"')
                print()
            else:
                print(f"Could not get token for {user['username']}")
                print()
    
    print("=" * 50)
    print("Copy these tokens to your test_ws.py file")

if __name__ == "__main__":
    main() 