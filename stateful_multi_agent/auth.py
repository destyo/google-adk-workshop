import json
import os
import getpass
from typing import Dict

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_credentials() -> Dict[str, str]:
    """Load user credentials from a JSON file; create default demo users if not present."""
    if not os.path.exists(CREDENTIALS_FILE):
        creds = {
            'alice': 'alice123',
            'bob': 'bob123',
        }
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(creds, f)
    else:
        with open(CREDENTIALS_FILE, 'r') as f:
            creds = json.load(f)
    return creds

def authenticate_user(username: str, password: str) -> bool:
    """Validate username and password against stored credentials."""
    creds = load_credentials()
    return creds.get(username) == password

def authenticate_prompt() -> str:
    """Prompt user for credentials until valid login, then return the username."""
    while True:
        username = input('Username: ').strip()
        password = getpass.getpass('Password: ')
        if authenticate_user(username, password):
            print(f'✅ Authenticated as {username}')
            return username
        print('❌ Invalid credentials, please try again.')
