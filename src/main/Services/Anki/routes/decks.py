from flask import Blueprint, jsonify, request
from database.context import AnkiDatabaseContext

decks_bp = Blueprint('decks', __name__)
db_context = AnkiDatabaseContext()

@decks_bp.route('/decks', methods=['POST'])
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

@decks_bp.route('/decks/<int:deck_id>', methods=['PUT'])
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

@decks_bp.route('/decks', methods=['GET'])
def list_decks():
    session = db_context.Session()
    try:
        decks = session.query(Deck).all()
        result = []
        for deck in decks:
            result.append({
                "id": deck.id,
                "name": deck.name,
                "description": deck.description
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@decks_bp.route('/decks/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    try:
        deck = db_context.get_deck(deck_id)
        if not deck:
            return jsonify({"error": "Deck not found."}), 404

        return jsonify({
            "id": deck.id,
            "name": deck.name,
            "description": deck.description
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@decks_bp.route('/decks/<int:deck_id>/cards', methods=['GET'])
def get_cards_in_deck(deck_id):
    try:
        cards = db_context.get_cards_in_deck(deck_id)
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

@decks_bp.route('/decks/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    try:
        deck = db_context.delete_deck(deck_id)
        if not deck:
            return jsonify({"error": "Deck not found."}), 404

        return jsonify({"message": "Deck deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@decks_bp.route('/decks', methods=['DELETE'])
def delete_all_decks():
    try:
        db_context.delete_all_decks()
        return jsonify({"message": "All decks deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
