from flask import Blueprint, request, jsonify, stream_with_context, Response
import openai
import os
from dotenv import load_dotenv

#Gets the OpenAI API key from the environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

#print(f"loaded key: {api_key}")

openai.api_key = api_key

#print(f"loaded key: {openai.api_key}")

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/ask', methods=['POST'])
def ask_question():
    #✔️ Reads JSON { "prompt": "your question here" } from the frontend and strips it for safety.
    data = request.get_json()
    prompt = data.get('prompt', '').strip()

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    def generate():
        #Tells openai to use the gpt-3.5-turbo model and stream the response.
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            #Streams the response back to the frontend.
            for chunk in response:
                if "choices" in chunk:
                    delta = chunk["choices"][0]["delta"]
                    content = delta.get("content", "")
                    yield content
        except openai.error.RateLimitError as e:
            yield b'Error. Rate limit exceeded. Please try again later.'

    return Response(stream_with_context(generate()), mimetype='text/plain')
