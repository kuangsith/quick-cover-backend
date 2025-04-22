from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import json
import config
from dotenv import load_dotenv
from pymongo import MongoClient
import gridfs
import os

load_dotenv()
api_key = os.getenv("apikey")

loginString = os.getenv("loginString")
dbclient = MongoClient(loginString)
db = dbclient["quick-cover"]
collection = db["users"]
fs = gridfs.GridFS(db)
fields_map = config.fields_map


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

@app.route('/create_resume_user', methods=['POST'])
def create_item_user():
    try:
        job_title = request.form.get('job_title')
        company_name = request.form.get('company_name')
        job_description = request.form.get('job_description')

        # Access user ID
        user_id = request.form.get('id')

        ## access all user info from id
        doc = collection.find_one({"_id": user_id})

        if doc:
            user_info = {}
            for front_end_field,db_field in fields_map.items():
                user_info[front_end_field] = doc.get(db_field,'')
        
        ## access pdf file

        resume = fs.find_one({'metadata._id': user_id})
        if resume:
            prompt = (
                f"My name is {user_info.get('given_name','')} {user_info.get('family_name','')}"
                f"Based on my resume, Create a basic cover letter for role {job_title} "
                f"at {company_name}. Jump right into the content. No 'Dear Hiring Manager'. "
                f"No 'Okay, here is the draft of the cover letter'"
                f"No placeholder,"
                f"job description is as follows :{job_description}"
            )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    types.Part.from_bytes(
                        data=resume.read(),
                        mime_type="application/pdf",
                    ),
                    prompt
                ]
            )
        else:
            prompt = (
                f"My name is {user_info.get('given_name','')} {user_info.get('family_name','')}"
                f"Create a basic cover letter for role {job_title} "
                f"at {company_name}. Jump right into the content. No 'Dear Hiring Manager'. "
                f"No 'Okay, here is the draft of the cover letter'"
                f"No placeholder,"
                f"job description is as follows :{job_description}"
            )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt]
            )

        out_dict = {}
        out_dict['message'] = "Item received successfully!"
        out_dict['gen_res'] = response.text
        out_dict['id'] = user_id
        out_dict.update(user_info)

        return jsonify(out_dict), 201

    except Exception as e:
        print("Error occurred:", str(e))  # Logs to console
        return jsonify({
            "message":f'Error {e}',
            "gen_res": None
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
