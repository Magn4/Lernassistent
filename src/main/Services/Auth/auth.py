import os
from flask import Flask, request, jsonify
import secrets
import string
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Database connection details (you can change these to your own)
DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'db_user')}:{os.getenv('DB_PASSWORD', 'password123')}@{os.getenv('DB_HOST', 'database')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'app_db')}"

def generate_token(length=32):
    """Generate a secure random token."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Function to get DB connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Function to ensure the tokens table exists
def ensure_tokens_table_exists():
    """Check if the tokens table exists and create it if not."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tokens (
        id SERIAL PRIMARY KEY,
        token TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()

# Ensure the tokens table exists at startup
ensure_tokens_table_exists()

# Endpoint to generate a new token
@app.route('/generate-token', methods=['GET'])
def generate_new_token():
    token = generate_token(32)

    # Store the token in the database
    conn = get_db_connection()
    cur = conn.cursor()
    insert_query = sql.SQL("INSERT INTO tokens (token) VALUES (%s)")
    cur.execute(insert_query, (token,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"token": token}), 201

# Endpoint to validate the token
@app.route('/validate-token', methods=['GET', 'POST'])
def validate_token():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Token missing"}), 401

    token = token.replace("Bearer ", "")  # If the token is passed as a Bearer token

    # Check if the token exists in the database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tokens WHERE token = %s;", (token,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        return jsonify({"message": "Token is valid!"}), 200
    else:
        return jsonify({"message": "Invalid token!"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
