from flask import Flask, request, jsonify
import openai
import time

app = Flask(__name__)

# Set the OpenAI API key from a file
openai.api_key_path = 'api_key.txt'


@app.route('/')
def index():
    return "Welcome to the Flask OpenAI Chat Integration!"

@app.route('/ask', methods=['POST'])
def ask_gpt():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return jsonify({'response': response.choices[0].message['content'].strip()})
        except openai.error.RateLimitError:
            if attempt < retry_attempts - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
        except openai.error.InvalidRequestError as e:
            return jsonify({'error': str(e)}), 400
        except openai.error.AuthenticationError:
            return jsonify({'error': 'Authentication failed. Check your API key.'}), 401
        except openai.error.APIError:
            return jsonify({'error': 'API error. Please try again later.'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)