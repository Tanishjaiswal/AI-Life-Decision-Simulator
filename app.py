from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔑 Your Groq API key
API_KEY = "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"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",   # ✅ THIS was missing before
            "Content-Type": "application/json"
        }

        prompt = """You are an AI Life Decision Advisor. Be concise and smart.

Rules:
- If the question is simple (yes/no, short query) → give a SHORT answer in 2-4 lines. No bullet points.
- If the question is complex or detailed → give a structured answer with choices, consequences, and recommendation.
- Never give unnecessary long responses.
- Always end with a confident 1-line recommendation.
- Talk like a smart friend, not a robot."""

        data = {
            "model": "llama-3.1-8b-instant",   # ✅ Free fast Groq model
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user",   "content": user_input}
            ],

            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        print(result)  # Debug

        if "choices" in result:
            reply = result["choices"][0]["message"]["content"]
        elif "error" in result:
            reply = f"⚠️ API Error: {result['error'].get('message', 'Unknown error')}"
        else:
            reply = "Unexpected response from API"

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
