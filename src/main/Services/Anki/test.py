import requests

BASE_URL = "http://127.0.0.1:8000"  # Make sure this matches where your Flask app is running

# Create a new deck
deck_data = {
    "name": "Test Deck",
    "description": "Description for test deck"
}

response = requests.post(f"{BASE_URL}/health")

if response.status_code == 200:
    print(f"Deck created successfully: {response.json()}")
else:
    print(f"Failed to create deck. Error: {response.text}")

# Create a new card
card_data = {
    "front": "Test front",
    "back": "Test back",
    "deck_id": 1  # Ensure this matches an existing deck id
}

response = requests.post(f"{BASE_URL}/cards", json=card_data)

if response.status_code == 200:
    print(f"Card created successfully: {response.json()}")
else:
    print(f"Failed to create card. Error: {response.text}")
