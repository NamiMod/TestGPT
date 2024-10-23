# app.py

from flask import Flask, render_template, request, jsonify
import os
import json
import logging
from openai import OpenAI

client = client = OpenAI(api_key="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")  # Consider using environment variables for API keys

# Initialize Flask app
app = Flask(__name__)

# ==========================
# Configure Logging
# ==========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================
# Helper Functions
# ==========================

def is_test_generation_prompt(prompt):
    """
    Determines if the provided prompt is related to test generation.
    Returns True if related, False otherwise.
    """
    system_message = "You are an assistant that determines whether a given prompt is related to test generation for software testing scenarios. Reply with 'Yes' or 'No' only."
    user_message = f"Is the following prompt related to test generation?\n\nPrompt: {prompt}"

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0
        )
        answer = response.choices[0].message.content.strip().lower()
        logger.info(f"Prompt relevance check response: {answer}")
        return answer == "yes"
    except Exception as e:
        logger.error(f"Error in is_test_generation_prompt: {str(e)}")
        # In case of error, default to False to prevent unintended processing
        return False

def generate_test(prompt):
    """
    Generates a test scenario based on the provided prompt.
    Returns a dictionary with 'answer'.
    """
    system_message = "You are ChatGPT, a large language model trained by OpenAI."
    user_message = (
        f"Please generate a test scenario based on the following description.\n\n"
        f"Description: {prompt}\n\n"
        f"Provide your response as plain text."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500
        )
        assistant_reply = response.choices[0].message.content.strip()
        logger.info(f"Test generation response: {assistant_reply}")

        return {'answer': assistant_reply}

    except Exception as e:
        logger.error(f"Error in generate_test: {str(e)}")
        raise e

# ==========================
# Routes
# ==========================

@app.route('/')
def home():
    """
    Renders the home page.
    """
    return render_template('index.html')  # Removed 'result' and 'title' as frontend handles it

@app.route('/submit', methods=['POST'])
def submit():
    """
    Handles the submission of prompts to generate tests.
    Expects JSON data with a 'prompt' field.
    Returns JSON with 'answer'.
    """
    try:
        # Parse JSON data from the request
        data = request.get_json()
        prompt = data.get('prompt', '').strip()

        logger.info(f"Received prompt: {prompt}")

        # Server-side Input Validation
        if not prompt:
            logger.warning("No prompt provided.")
            return jsonify({'error': 'No prompt provided.'}), 400
        if len(prompt) > 4000:
            logger.warning("Prompt is too long.")
            return jsonify({'error': 'Prompt is too long. Please limit to 4000 characters.'}), 400

        # Step 1: Check if the prompt is related to test generation
        if not is_test_generation_prompt(prompt):
            logger.info("Prompt is not related to test generation.")
            return jsonify({
                'error': 'This prompt is not related.'
            }), 400

        # Step 2: Generate the test
        test_result = generate_test(prompt)
        return jsonify(test_result)

    except Exception as e:
        logger.error(f"An error occurred in /submit route: {str(e)}")
        return jsonify({'error': 'An internal error occurred. Please try again later.'}), 500

# ==========================
# Run the Application
# ==========================

if __name__ == '__main__':
    # Run the Flask app in debug mode. Disable debug mode in production.
    app.run(debug=True)
