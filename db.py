import sqlite3

# Connect to database
connection = sqlite3.connect("chatbot.db", check_same_thread=False)
cursor = connection.cursor()

# Check if 'interactions' table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS interactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_input TEXT,
    bot_response TEXT
)
""")
connection.commit()

# Try to add 'user_id' column if it doesn't exist
try:
    cursor.execute("ALTER TABLE interactions ADD COLUMN user_id TEXT")
except sqlite3.OperationalError:
    # Column already exists
    pass

# Function to log interactions
def log_interaction(user_id, user_input, bot_response):
    # Ensure bot_response is a string
    if isinstance(bot_response, tuple):
        bot_response = bot_response[0]

    cursor.execute(
        "INSERT INTO interactions (user_id, user_input, bot_response) VALUES (?, ?, ?)",
        (user_id, user_input, bot_response)
    )
    connection.commit()
