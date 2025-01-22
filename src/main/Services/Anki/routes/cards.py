from flask import Blueprint, jsonify, request
from database.context import AnkiDatabaseContext
from datetime import datetime, timedelta

cards_bp = Blueprint('cards', __name__)
db_context = AnkiDatabaseContext()

@cards_bp.route('/cards', methods=['POST'])
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

@cards_bp.route('/cards/<int:card_id>', methods=['GET'])
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

@cards_bp.route('/cards/<int:card_id>', methods=['PUT'])
def update_card(card_id):
    data = request.get_json()
    button = data.get('button')

    if not button:
        return jsonify({"error": "Missing required field (button)."}), 400

    card = db_context.get_card(card_id)
    if not card:
        return jsonify({"error": "Card not found."}), 404

    interval = card.interval
    ef = card.ef
    repetitions = card.repetitions
    lapses = card.lapses

    result = update_card_logic(button, interval, ef, repetitions, lapses)

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
    if button == "Again":
        interval = 10 / 60
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

@cards_bp.route('/cards/<int:card_id>', methods=['DELETE'])
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

@cards_bp.route('/cards', methods=['GET'])
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

@cards_bp.route('/next-review-card', methods=['GET'])
def next_review_card():
    try:
        card = db_context.get_next_review_card()
        if not card:
            return jsonify({"message": "No cards ready for review."}), 200

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
