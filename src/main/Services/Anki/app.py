from flask import Flask, jsonify, request
from database import AnkiDatabaseContext, Card, Deck  # Make sure Deck is imported from your models
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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

# Delete a deck
@app.route('/decks/<int:deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    session = db_context.Session()
    try:
        deck = session.query(Deck).get(deck_id)
        if not deck:
            return jsonify({"error": "Deck not found."}), 404

        # Delete all cards associated with the deck
        session.query(Card).filter_by(deck_id=deck_id).delete()

        session.delete(deck)
        session.commit()
        return jsonify({"message": "Deck and associated cards deleted successfully."}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

# List all decks
@app.route('/decks', methods=['GET'])
def list_decks():
    session = db_context.Session()
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

# Get a specific deck and its cards
@app.route('/decks/<int:deck_id>', methods=['GET'])
def get_deck(deck_id):
    session = db_context.Session()
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

@app.route('/auto-generate-cards', methods=['POST'])
def auto_generate_cards():
    try:
        # Check if a PDF file is provided in the request
        pdf_file = request.files.get('file')
        if not pdf_file:
            return jsonify({"error": "No PDF file provided"}), 400

        # Ensure the file is in PDF format
        if not pdf_file.filename.endswith('.pdf'):
            return jsonify({"error": "The file must be in PDF format"}), 400

        # Send the PDF file to the text extraction service
        extract_url = "http://127.0.0.1:5001/api/extract"
        files = {'file': pdf_file.read()}
        extract_response = requests.post(extract_url, files=files)

        # Check if the text extraction was successful
        if extract_response.status_code != 200:
            return jsonify({"error": "Failed to extract text from PDF"}), 500

        # Extract the text content from the response
        extracted_text = extract_response.json().get('text')
        if not extracted_text:
            return jsonify({"error": "No text extracted from PDF"}), 500

        # Prepare the data for generating cards
        data = {
            "content": extracted_text,
            "deck_id": request.form.get('deck_id'),
            "num_cards": request.form.get('num_cards', 20)
        }

        # Call the generate_cards endpoint with the extracted text
        generate_response = requests.post(
            'http://127.0.0.1:8000/generate-cards',
            json=data
        )

        # Check if the card generation was successful
        if generate_response.status_code != 201:
            return jsonify({"error": "Failed to generate cards"}), 500

        # Return the generated cards
        return generate_response.json(), 201

    except Exception as e:
        app.logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Generate Anki cards from content
@app.route('/generate-cards', methods=['POST'])
def generate_cards():
    try:
        # Parse incoming JSON
        data = request.get_json()
        content = data.get('content')
        deck_id = data.get('deck_id')
        num_cards = data.get('num_cards', 20)  # Default to 20 cards if not specified
        
        if not content or not deck_id:
            return jsonify({"error": "Missing required fields (content, deck_id)."}), 400
        
        # Ensure content is not excessively long
        if len(content) > 5000:
            return jsonify({"error": "Content too long. Please provide a shorter excerpt."}), 400

        # Set the URL and headers for the API request
        API_URL = "https://api.groq.com/openai/v1/chat/completions"
        HEADERS = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
        }

        # Construct the prompt dynamically based on the input
        prompt = f"""
        You are a flashcard generator. Based on the following content, generate {num_cards} high-quality Anki flashcards. 
        The flashcards should cover key concepts and definitions from the content. and only Exam related questions. 
        No need to generate questions that are not related to the exam. 

        For each flashcard:
        - The "front" should be a question that tests knowledge or recall of the key concept.
        - The "back" should provide a clear, concise answer, explanation, or definition.
        - The front and back should be short, precise, and easy to memorize.

        Content: {content}

        Format the output as a JSON array with 'front' and 'back' fields for each card, like this:

        [
          {{
            "front": "What is [concept]?",
            "back": "The definition of [concept] is [definition]."
          }},
          {{
            "front": "How does [concept] work?",
            "back": "The [concept] works by [explanation]."
          }},
          ...
        ]
        """

        # Define the payload for the API request
        PAYLOAD = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000  # Adjust token limit based on expected response size
        }

        # Send the request to the API
        app.logger.info("Sending request to API...")
        response = requests.post(API_URL, headers=HEADERS, json=PAYLOAD)
        app.logger.info(f"API Response Status: {response.status_code}")
        
        # Check if the request was successful
        if response.status_code == 200:
            response_data = response.json()
            # Extract the content from the response
            content = response_data['choices'][0]['message']['content']
            
            # Clean up the content to get just the JSON part
            try:
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                json_str = content[start_idx:end_idx]
                
                cards = json.loads(json_str)
                app.logger.info(f"Successfully parsed {len(cards)} cards")
            except json.JSONDecodeError as e:
                app.logger.error(f"JSON Parse Error: {e}")
                app.logger.error(f"Content: {content}")
                return jsonify({"error": "Failed to parse generated cards"}), 500
        else:
            app.logger.error(f"API Error: {response.text}")
            return jsonify({"error": f"API request failed: {response.text}"}), 500

        # Add the generated cards to the database
        created_cards = []
        for card in cards:
            front = card['front']
            back = card['back']
            try:
                new_card = db_context.create_card(front, back, deck_id)
                if new_card:
                    created_cards.append({
                        "id": new_card.id,
                        "front": new_card.front,
                        "back": new_card.back,
                        "deck_id": new_card.deck_id
                    })
                else:
                    app.logger.error(f"Failed to create card: {front}")
            except Exception as e:
                app.logger.error(f"Database Error: {e}")
                return jsonify({"error": f"Failed to create card: {str(e)}"}), 500

        return jsonify({"cards": created_cards}), 201

    except Exception as e:
        app.logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)