import requests
import time

# Set the URL of your FastAPI server
BASE_URL = "http://127.0.0.1:8000"

def test_update_card(card_id, button):
    url = f"{BASE_URL}/update-card"
    data = {
        "card_id": card_id,
        "button": button
    }
    
    # Send a POST request to the API
    response = requests.post(url, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Card {card_id} updated successfully:")
        print(f"Next interval: {response.json()['next_interval']} days")
        print(f"Ease factor: {response.json()['ef']}")
        print(f"Repetitions: {response.json()['repetitions']}")
        print(f"Lapses: {response.json()['lapses']}")
    else:
        print(f"Failed to update card {card_id}. Error: {response.text}")

if __name__ == "__main__":
    # Test the API with different button inputs (e.g., "Again", "Hard", "Good", "Easy")
    card_id = 1  # Assume card_id 1 exists in the database

    # Test "Again"
    print("Testing 'Again' button:")
    test_update_card(card_id, "Again")
    time.sleep(1)  # Sleep for 1 second between requests to simulate real usage

    # Test "Hard"
    print("\nTesting 'Hard' button:")
    test_update_card(card_id, "Hard")
    time.sleep(1)

    # Test "Good"
    print("\nTesting 'Good' button:")
    test_update_card(card_id, "Good")
    time.sleep(1)

    # Test "Easy"
    print("\nTesting 'Easy' button:")
    test_update_card(card_id, "Easy")
    time.sleep(1)
