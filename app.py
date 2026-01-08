
from google import genai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your API key (use environment variable in real projects)
os.environ['GOOGLE_API_KEY'] = 'PASTE_YOUR_API_KEY_HERE'

client = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_ingredients = data.get('ingredients', '')

    prompt = f"""
You are a helpful recipe assistant system with three roles:

1. First, as an INGREDIENT CHECKER, acknowledge the ingredients provided.

2. Then, as a RECIPE FINDER, suggest 2-3 simple recipes that can be made with: {user_ingredients}
   For each recipe provide:
   - Recipe name
   - Brief description
   - Main cooking steps

3. Finally, as a SHOPPING LIST CREATOR, list any common additional ingredients that might be needed.

Please organize your response with clear headings for each section.
"""

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )

    return jsonify({"result": response.text})

if __name__ == '__main__':
    app.run(debug=True)
