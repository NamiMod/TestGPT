from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(api_key="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")
username = ""

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', result="")

@app.route('/submit', methods=['POST'])
def submit():
    # Get the prompt from the user
    prompt = request.form.get('prompt')

    # Make a request to the OpenAI API
    response = client.chat.completions.create(model="gpt-3.5-turbo",  # or gpt-4 if you have access
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ])

    # Extract the assistant's response
    result = response.choices[0].message.content

    # Render the template and pass the result to the textarea
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)