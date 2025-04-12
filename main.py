from flask import Flask, request, jsonify
from flask_cors import CORS
import config
from google import genai
from google.genai import types

client = genai.Client(api_key=config.apikey)

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['POST'])
def create_item():
    data = request.get_json()

    # Basic validation
    if not data or 'job_title' not in data or 'company_name' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents= f"Create a <100 word cover letter for this: job title: {data['job_title']} company name: {data['company_name']}",
    )

    # Example response
    return jsonify({
        "message": "Item received successfully!",
        "gen_res": response.text
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
