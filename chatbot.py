import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import wikipedia

# ---------------------------
# Download missing NLTK resources
# ---------------------------
nltk_resources = ['punkt', 'stopwords', 'punkt_tab']
for resource in nltk_resources:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource)

# ---------------------------
# Load DialoGPT model
# ---------------------------
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# ---------------------------
# Rule-based casual responses
# ---------------------------
casual_responses = {
    "hello": "Hi! How can I help you today?",
    "hi": "Hello! Nice to meet you!",
    "hey": "Hey there! What can I do for you?",
    "how are you": "I'm a bot, but I'm doing great! How about you?",
    "bye": "Goodbye! Have a nice day!",
    "thanks": "You're welcome!",
    "thank you": "No problem!"
}

# ---------------------------
# Detect factual questions
# ---------------------------
def is_factual_question(user_input):
    keywords = ["who", "what", "when", "where", "first", "capital", "year", "moon", "president", "prime minister"]
    return any(word in user_input.lower() for word in keywords)

# ---------------------------
# Wikipedia factual answer
# ---------------------------
def get_factual_answer(user_input):
    try:
        summary = wikipedia.summary(user_input, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is ambiguous. Did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.exceptions.PageError:
        return "Sorry, I could not find an answer to that."

# ---------------------------
# Generate chatbot response
# ---------------------------
def generate_response(user_input, chat_history_ids=None):
    user_input_clean = user_input.lower().strip()

    # 1. Rule-based casual responses
    if user_input_clean in casual_responses:
        return casual_responses[user_input_clean], chat_history_ids

    # 2. Factual questions
    if is_factual_question(user_input):
        return get_factual_answer(user_input), chat_history_ids

    # 3. Fallback to DialoGPT
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    if chat_history_ids is not None:
        input_ids = torch.cat([chat_history_ids, input_ids], dim=-1)

    updated_history = model.generate(
        input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        num_return_sequences=1
    )

    response = tokenizer.decode(updated_history[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    if not response.strip():
        response = "I'm not sure how to answer that."

    # Clean response
    response = response.strip()

    # Reset history if too long
    if updated_history.shape[-1] > 1000:
        updated_history = None

    return response, updated_history
