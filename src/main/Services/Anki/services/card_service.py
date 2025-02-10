from flask import jsonify
from ..database import AnkiDatabaseContext, Card

class CardService:
    def __init__(self):
        self.db_context = AnkiDatabaseContext()

    def create_card(self, request):
        data = request.get_json()
        front = data.get('front')
        back = data.get('back')
        deck_id = data.get('deck_id')

        if not front or not back or not deck_id:
            return jsonify({"error": "Missing required fields (front, back, deck_id)."}), 400

        try:
            new_card = self.db_context.create_card(front, back, deck_id)
            return jsonify({
                "id": new_card.id,
                "front": new_card.front,
                "back": new_card.back,
                "deck_id": new_card.deck_id
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_card(self, card_id):
        try:
            card = self.db_context.get_card(card_id)
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

    def update_card(self, card_id, request):
        data = request.get_json()
        button = data.get('button')

        if not button:
            return jsonify({"error": "Missing required field (button)."}), 400

        card = self.db_context.get_card(card_id)
        if not card:
            return jsonify({"error": "Card not found."}), 404

        interval = card.interval
        ef = card.ef
        repetitions = card.repetitions
        lapses = card.lapses

        result = self.update_card_logic(button, interval, ef, repetitions, lapses)

        try:
            self.db_context.update_card_db(
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

    def update_card_logic(self, button, interval, ef, repetitions, lapses):
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

    def delete_card(self, card_id):
        session = self.db_context.Session()
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

    def list_cards(self):
        session = self.db_context.Session()
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
