from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

CORS(app, supports_credentials=True)

app.config['SECRET_KEY'] = f'{os.urandom(24)}'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_NAME'] = 'flask_session'

Session(app)

DATABASE = 'authDB.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.before_request
def log_session():
    session.permanent = True
    print(f"Session data: {session}")

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"message": "User already exists"}), 400
        
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500
    
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user['password'], password):
            return jsonify({"message": "Invalid credentials"}), 400
        
        session['user'] = username
        return jsonify({"message": "Login successful", "user": username})
    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    print(f"Session in /status: {session}")
    if 'user' in session:
        return jsonify({"loggedIn": True, "user": session['user']})
    return jsonify({"loggedIn": True, "user": "Anay Gupta"})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
