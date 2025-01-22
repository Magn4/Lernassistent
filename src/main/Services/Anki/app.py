from flask import Flask
from database.context import AnkiDatabaseContext

app = Flask(__name__)

# Initialize the database context
db_context = AnkiDatabaseContext()

# Import routes
from routes.health import health_bp
from routes.cards import cards_bp
from routes.decks import decks_bp

# Register blueprints
app.register_blueprint(health_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(decks_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
