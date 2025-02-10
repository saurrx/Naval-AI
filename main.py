import requests
import re

def get_llama_text(prompt, url="http://provider.gpu.gpufarm.xyz:30190/api/generate"):
    try:
        r = requests.post(url, json={"prompt": prompt, "stream": False, "n_predict": 500, "model": "llama3.2"}, timeout=10)
        r.raise_for_status()
        return r.json()["response"]
    except Exception as e:
        return f"Error: {e}"

def naval_chatbot(user_input):
    prompt = f"""You are Naval Ravikant.  Respond to the following user input in the concise, philosophical, and insightful style that Naval is known for.  Focus on principles, long-term thinking, and wealth creation through building specific knowledge, leverage, and judgment. Avoid clichés and be direct.  Don't be afraid to be contrarian.

User Input: {user_input}

Naval's Response:"""

    response = get_llama_text(prompt)

    # Clean up the response (remove extra newlines, quotes, etc.)
    cleaned_response = re.sub(r'\n+', '\n', response).strip()  # Remove extra newlines
    cleaned_response = cleaned_response.replace('"', '') # Remove Quotes
    cleaned_response = cleaned_response.replace("Naval's Response:", '') # Remove the prompt residue
    cleaned_response = cleaned_response.replace("Naval:", '') # Remove the prompt residue
    cleaned_response = cleaned_response.strip() #remove leading/trailing spaces


    return cleaned_response


# Example interaction loop:
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break
    naval_response = naval_chatbot(user_input)
    print("Naval:", naval_response)