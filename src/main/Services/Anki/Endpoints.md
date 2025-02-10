# API Endpoints

This document provides a list and description of all the endpoints available in the Anki service.

## Health Check

### GET /health
- **Description**: Check the health status of the service.
- **Response**: 
  - 200: `{"status": "ok"}`

## Cards

### POST /cards
- **Description**: Create a new card.
- **Request Body**:
  - `front` (string): The front text of the card.
  - `back` (string): The back text of the card.
  - `deck_id` (int): The ID of the deck to which the card belongs.
- **Response**:
  - 201: The created card.
  - 400: Missing required fields.
  - 500: Internal server error.

### GET /cards/<int:card_id>
- **Description**: Get a specific card by ID.
- **Response**:
  - 200: The card details.
  - 404: Card not found.
  - 500: Internal server error.

### PUT /cards/<int:card_id>
- **Description**: Update a card (e.g., after a review session).
- **Request Body**:
  - `button` (string): The response button (Again, Hard, Good, Easy).
- **Response**:
  - 200: Card updated successfully.
  - 400: Missing required field.
  - 404: Card not found.
  - 500: Internal server error.

### DELETE /cards/<int:card_id>
- **Description**: Delete a card.
- **Response**:
  - 200: Card deleted successfully.
  - 404: Card not found.
  - 500: Internal server error.

### GET /cards
- **Description**: List all cards.
- **Response**:
  - 200: List of all cards.
  - 500: Internal server error.

## Decks

### POST /decks
- **Description**: Create a new deck.
- **Request Body**:
  - `name` (string): The name of the deck.
  - `description` (string): The description of the deck.
- **Response**:
  - 201: The created deck.
  - 400: Missing required field.
  - 500: Internal server error.

### PUT /decks/<int:deck_id>
- **Description**: Update an existing deck.
- **Request Body**:
  - `name` (string): The new name of the deck.
  - `description` (string): The new description of the deck.
- **Response**:
  - 200: The updated deck.
  - 404: Deck not found.
  - 500: Internal server error.

### GET /decks
- **Description**: List all decks.
- **Response**:
  - 200: List of all decks with their cards.
  - 500: Internal server error.

### GET /decks/<int:deck_id>
- **Description**: Get a specific deck and its cards.
- **Response**:
  - 200: The deck details with its cards.
  - 404: Deck not found.
  - 500: Internal server error.

## Auto-Generate Cards

### POST /auto-generate-cards
- **Description**: Automatically generate cards from a provided PDF file.
- **Request**:
  - `file` (file): The PDF file to extract text from.
  - `deck_id` (int): The ID of the deck to which the cards will be added.
  - `num_cards` (int, optional): The number of cards to generate (default is 20).
- **Response**:
  - 201: The generated cards.
  - 400: Missing required fields or invalid file format.
  - 500: Internal server error.

### POST /generate-cards
- **Description**: Generate Anki cards from provided content.
- **Request Body**:
  - `content` (string): The content to generate cards from.
  - `deck_id` (int): The ID of the deck to which the cards will be added.
  - `num_cards` (int, optional): The number of cards to generate (default is 20).
- **Response**:
  - 201: The generated cards.
  - 400: Missing required fields or content too long.
  - 500: Internal server error.