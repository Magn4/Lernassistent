from flask import jsonify
from ..database import AnkiDatabaseContext, Deck, Card

class DeckService:
    def __init__(self):
        self.db_context = AnkiDatabaseContext()

    def create_deck(self, request):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if not name:
            return jsonify({"error": "Missing required field (name)."}), 400

        try:
            new_deck = self.db_context.create_deck(name, description)
            return jsonify({
                "id": new_deck.id,
                "name": new_deck.name,
                "description": new_deck.description
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def update_deck(self, deck_id, request):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        try:
            updated_deck = self.db_context.update_deck(deck_id, name, description)
            if not updated_deck:
                return jsonify({"error": "Deck not found."}), 404

            return jsonify({
                "id": updated_deck.id,
                "name": updated_deck.name,
                "description": updated_deck.description
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def delete_deck(self, deck_id):
        session = self.db_context.Session()
        try:
            deck = session.query(Deck).get(deck_id)
            if not deck:
                return jsonify({"error": "Deck not found."}), 404

            session.delete(deck)
            session.commit()
            return jsonify({"message": "Deck deleted successfully."}), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500

    def list_decks(self):
        session = self.db_context.Session()
        try:
            decks = session.query(Deck).all()
            result = []
            for deck in decks:
                cards = session.query(Card).filter_by(deck_id=deck.id).all()
                result.append({
                    "id": deck.id,
                    "name": deck.name,
                    "description": deck.description,
                    "cards": [{"id": card.id, "front": card.front, "back": card.back} for card in cards]
                })
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    def get_deck(self, deck_id):
        session = self.db_context.Session()
        try:
            deck = session.query(Deck).get(deck_id)
            if not deck:
                return jsonify({"error": "Deck not found."}), 404

            cards = session.query(Card).filter_by(deck_id=deck.id).all()
            result = {
                "id": deck.id,
                "name": deck.name,
                "description": deck.description,
                "cards": [{"id": card.id, "front": card.front, "back": card.back} for card in cards]
            }
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
