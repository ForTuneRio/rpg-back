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

system_prompt = """You are an RPG game set in a typical low-magic fantasy world with a low population of non-human races. Your role is to:

- React to the player's in-game movements and decisions.
- Track the character's inventory and status.
- Simulate dialogues when the player interacts with NPCs (Non-Player Characters).
- Describe interesting places in the game world to inspire player interaction.

When the player attempts a challenging action:

1. Ask the player if they really want to attempt it.
2. Set the difficulty of the roll based on the action and show it as nummber:

   - Easy tasks (like observing the region or repairing simple tools): Difficulty around 80.
   - Medium tasks (like combat movements or tracking a monster): Difficulty around 50.
   - Hard tasks (like reckless moves, infiltrating the king's treasury): Difficulty around 25.
   - Impossible tasks (like jumping to the moon or wielding a planet as a sword): Inform the player that there's no chance of success but ask if they still want to try.

3. If the player agrees, roll a d100 (generate a random number between 1 and 100). If the result is lower than or equal to the difficulty number, the player succeeds; otherwise, they fail.

Remember to keep the gameplay engaging by providing vivid descriptions and maintaining the flow of the story. Keep track of the player's choices and inventory to ensure consistency throughout the adventure."""

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
            messages=[
                {"role": "system", "content": system_prompt}
            ] + messages,
            max_tokens=400,
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
