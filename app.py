from flask import Flask, request, jsonify
import openai
from openai import OpenAIError
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources="*")

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/ask', methods=['POST'])
def ask_gpt():
    data = request.get_json()

    # Retrieve conversation messages from the request
    messages = data.get('messages', [])

    if not messages:
        return jsonify({'error': 'No messages provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,  # Send the entire conversation history
            max_tokens=150,
            temperature=0.7
        )
        return jsonify({'value': response['choices'][0]['message']['content'].strip()})
    except OpenAIError as e:
        print(f"OpenAI Error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True)
