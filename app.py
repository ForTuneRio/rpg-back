from flask import Flask, request, jsonify
import openai
import time
from openai import OpenAIError
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the environment variables from .env
load_dotenv()

# Get the OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/ask', methods=['GET'])
def ask_gpt():
    prompt = request.args.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    try:
        # Correct API call for chat-based model (gpt-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
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
