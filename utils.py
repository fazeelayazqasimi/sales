import json

SALES_FILE = "sales.json"
AGENTS_FILE = "agents.json"

def load_data(file):
    """Load data from a JSON file."""
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(file, data):
    """Save data to a JSON file."""
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def validate_login(username, password):
    """Validate login credentials."""
    agents = load_data(AGENTS_FILE)
    for agent in agents:
        if agent["username"] == username and agent["password"] == password:
            return agent
    return None

def calculate_commission(price):
    if price <= 40000:
        return price * 0.005
    elif 40001 <= price <= 80000:
        return price * 0.003
    elif 80001 <= price <= 150000:
        return price * 0.002
    else:
        return price * 0.001

