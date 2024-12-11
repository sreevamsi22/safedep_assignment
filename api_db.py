#!/usr/bin/env python
# coding: utf-8

# ## Api(flask) creation

# In[ ]:


from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DB_FILE = "commands.db"

def initialize_db():
    """
    Initializes the SQLite database and creates the 'commands' table if it doesn't exist.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    command TEXT NOT NULL
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

@app.route('/commands', methods=['POST'])
def add_commands():
    data = request.get_json()
    if not data or 'commands' not in data:
        return jsonify({"error": "Invalid request, 'commands' field is required"}), 400

    # Validate and insert commands into the database
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            for cmd in data['commands']:
                if not cmd.get("user_id") or not cmd.get("command"):
                    return jsonify({"error": "Each command must include 'user_id' and 'command'"}), 400
                cursor.execute("INSERT INTO commands (user_id, command) VALUES (?, ?)", 
                               (cmd["user_id"], cmd["command"]))
            conn.commit()
        return jsonify({"message": "Commands added successfully"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500


@app.route('/commands', methods=['GET'])
def get_commands():
    user_id = request.args.get('user_id')
    commands = []
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            if user_id:
                cursor.execute("SELECT command, user_id FROM commands WHERE user_id = ?", (user_id,))
            else:
                cursor.execute("SELECT command, user_id FROM commands")
            commands = [{"command": row[0], "user_id": row[1]} for row in cursor.fetchall()]
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    # Add pagination for large datasets (if needed in future)
    return jsonify(commands)


if __name__ == '__main__':
    initialize_db()  # Ensure the database is initialized before starting the server
    app.run(host="0.0.0.0", port=5000, debug=True)

