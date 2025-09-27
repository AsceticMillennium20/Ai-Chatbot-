from flask import Flask, request, jsonify, render_template
from chatbot import generate_response
from db import log_interaction

app = Flask(__name__)

# Dictionary to store chat history per user
chat_histories = {}  # { user_id: chat_history_ids }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '').strip()
    user_id = data.get('userId', 'default_user')

    if not user_input:
        return jsonify({"response": "Please enter a message."})

    # Initialize chat history for new user
    if user_id not in chat_histories:
        chat_histories[user_id] = None

    # Generate response
    response, updated_history = generate_response(user_input, chat_histories[user_id])

    # Update chat history
    chat_histories[user_id] = updated_history

    # Log interaction
    log_interaction(user_id, user_input, response)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=33400)
