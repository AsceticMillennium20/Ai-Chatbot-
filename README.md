AI-Powered Hybrid Chatbot

An intelligent hybrid chatbot built using Python, Flask, and NLP techniques.  
It combines rule-based responses, knowledge retrieval, and generative AI to handle a wide range of user queries.

---

Features

Hybrid Response System
- Rule-based responses for greetings and basic interactions
- Wikipedia API integration for factual question answering
- Generative AI fallback using DialoGPT-small for open-ended conversations

Multi-User Support
- Handles multiple users with separate chat sessions
- Maintains individual chat histories

Data Management
- Stores conversations in SQLite database
- Enables chat history tracking and analysis

---

Tech Stack

🔹 Core Technologies
- Python 3.12
- Flask (Backend API)

🔹 AI / NLP
- Hugging Face Transformers
- DialoGPT-small
- NLTK
- Wikipedia API

🔹 Database
- SQLite

---

System Workflow

1. User sends a message via frontend/API  
2. System checks:
   - If it's a greeting → rule-based response  
   - If it's factual → fetch from Wikipedia API  
   - Else → generate response using DialoGPT  
3. Response is returned and stored in database  

---

How to Run

1. Clone the repository  
2. Install dependencies:
3. pip install -r requirements.txt

3. Run Flask server:

python app.py

4. Open in browser / API tool  

---

Key Highlights

- Hybrid chatbot combining rule-based + retrieval + generative AI  
- Real-time response handling using NLP models  
- Persistent chat storage using database  
- Scalable architecture for future AI improvements  

---

Future Improvements

- Upgrade to larger LLM (GPT-Neo / LLaMA)  
- Add frontend UI (React / Streamlit)  
- Deploy on cloud (AWS / Render)  
- Add authentication & user dashboard  
