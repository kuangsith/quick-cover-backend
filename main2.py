from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("apikey")


client = genai.Client(api_key=api_key)

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['POST'])
def create_item():
    try:
        job_title = request.form.get('job_title')
        company_name = request.form.get('company_name')
        job_description = request.form.get('job_description')
        
        # Access uploaded file (resume)
        pdf_file = request.files.get('file')

        prompt = (
            f"Based on my resume, Create a basic cover letter for role {job_title} "
            f"at {company_name}. Jump right into the content. No 'Dear Hiring Manager'. "
            f"No 'Okay, here is the draft of the cover letter'"
            f"job description is as follows :{job_description}"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(
                    data=pdf_file.read(),
                    mime_type="application/pdf",
                ),
                prompt
            ]
        )

        return jsonify({
            "message": "Item received successfully!",
            "gen_res": response.text
        }), 201

    except Exception as e:
        print("Error occurred:", str(e))  # Logs to console
        return jsonify({
            "gen_res": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
