
from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

def get_llama_text(prompt, url="http://provider.gpu.gpufarm.xyz:30190/api/generate"):
    try:
        r = requests.post(url, json={"prompt": prompt, "stream": False, "n_predict": 500, "model": "llama3.2"}, timeout=10)
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        return f"Error: {e}"

def naval_chatbot(user_input):
    prompt = f"""You are Naval Ravikant. Respond to the following user input in the concise, philosophical, and insightful style that Naval is known for. Focus on principles, long-term thinking, and wealth creation through building specific knowledge, leverage, and judgment. Avoid clichés and be direct. Don't be afraid to be contrarian.

User Input: {user_input}

Naval's Response:"""

    response = get_llama_text(prompt)
    cleaned_response = re.sub(r'\n+', '\n', response).strip()
    cleaned_response = cleaned_response.replace('"', '')
    cleaned_response = cleaned_response.replace("Naval's Response:", '')
    cleaned_response = cleaned_response.replace("Naval:", '')
    cleaned_response = cleaned_response.strip()
    
    return cleaned_response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = naval_chatbot(user_message)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
