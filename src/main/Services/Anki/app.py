from flask import Flask, jsonify, request
from database import AnkiDatabaseContext, Card, Deck  # Make sure Deck is imported from your models

app = Flask(__name__)

# Initialize the database context
db_context = AnkiDatabaseContext()


# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200


# Create a new card
@app.route('/cards', methods=['POST'])
def create_card():
    data = request.get_json()
    front = data.get('front')
    back = data.get('back')
    deck_id = data.get('deck_id')

    if not front or not back or not deck_id:
        return jsonify({"error": "Missing required fields (front, back, deck_id)."}), 400

    try:
        new_card = db_context.create_card(front, back, deck_id)
        return jsonify({
            "id": new_card.id,
            "front": new_card.front,
            "back": new_card.back,
            "deck_id": new_card.deck_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get a specific card by ID
@app.route('/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    try:
        card = db_context.get_card(card_id)
        if not card:
            return jsonify({"error": "Card not found."}), 404

        return jsonify({
            "id": card.id,
            "front": card.front,
            "back": card.back,
            "next_review": card.next_review,
            "deck_id": card.deck_id,
            "interval": card.interval,
            "ef": card.ef,
            "repetitions": card.repetitions,
            "lapses": card.lapses
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update a card (e.g., after a review session)
@app.route('/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.get_json()

    # Get the response button (Again, Hard, Good, Easy)
    button = data.get('button')

    # Check if required fields are present
    if not button:
        return jsonify({"error": "Missing required field (button)."}), 400

    # Get current card data
    card = db_context.get_card(card_id)
    if not card:
        return jsonify({"error": "Card not found."}), 404

    interval = card.interval
    ef = card.ef
    repetitions = card.repetitions
    lapses = card.lapses

    # Apply the spaced repetition algorithm
    result = update_card_logic(button, interval, ef, repetitions, lapses)

    # Update the card with the new values
    try:
        db_context.update_card_db(
            card_id,
            {
                "next_interval": result["next_interval"],
                "new_ef": result["new_ef"],
                "repetitions": result["repetitions"],
                "lapses": result["lapses"]
            }
        )
        return jsonify({"message": "Card updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_card_logic(button, interval, ef, repetitions, lapses):
    # The core spaced repetition algorithm resides here.
    if button == "Again":
        interval = 10 / 60  # 10 minutes in fractional days
        repetitions = 0
        lapses += 1
    elif button == "Hard":
        interval = max(1, interval * 1.2)
        ef = max(1.3, ef - 0.15)
    elif button == "Good":
        interval = interval * ef
        repetitions += 1
    elif button == "Easy":
        interval = interval * ef * 1.3
        ef = min(3.0, ef + 0.15)
        repetitions += 1

    return {
        "next_interval": interval,
        "new_ef": ef,
        "repetitions": repetitions,
        "lapses": lapses,
    }

# Delete a card
@app.route('/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    session = db_context.Session()
    try:
        card = session.query(Card).get(card_id)
        if not card:
            return jsonify({"error": "Card not found."}), 404

        session.delete(card)
        session.commit()
        return jsonify({"message": "Card deleted successfully."}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500


# Create a new deck
@app.route('/decks', methods=['POST'])
def create_deck():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Missing required field (name)."}), 400

    try:
        new_deck = db_context.create_deck(name, description)
        return jsonify({
            "id": new_deck.id,
            "name": new_deck.name,
            "description": new_deck.description
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update an existing deck
@app.route('/decks/<int:deck_id>', methods=['PUT'])
def update_deck(deck_id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    try:
        updated_deck = db_context.update_deck(deck_id, name, description)
        if not updated_deck:
            return jsonify({"error": "Deck not found."}), 404

        return jsonify({
            "id": updated_deck.id,
            "name": updated_deck.name,
            "description": updated_deck.description
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# List all cards
@app.route('/cards', methods=['GET'])
def list_cards():
    session = db_context.Session()
    try:
        cards = session.query(Card).all()
        result = []
        for card in cards:
            result.append({
                "id": card.id,
                "front": card.front,
                "back": card.back,
                "next_review": card.next_review,
                "deck_id": card.deck_id,
                "interval": card.interval,
                "ef": card.ef,
                "repetitions": card.repetitions,
                "lapses": card.lapses
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)