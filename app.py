from flask import Flask, render_template, request, session, redirect, url_for
import openai
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import keys

app = Flask(__name__)
app.secret_key = keys.SESSION_DB_KEY

openai.api_base = keys.OPENAPI_BASE
openai.api_key = keys.OPENAPI_KEY
openai.api_type = keys.OPENAPI_TYPE
openai.api_version = keys.OPENAPI_VERS
deployment_name = keys.OPENAPI_DEPLOYMENT


# Routes
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/submit-login", methods=["POST"])
def submit_login():
    form_data = request.form
    session['user'] = form_data['user']
    print(session['user'])
    assistance = generate_assistance(session)

    return render_template("assistance.html", assistance=assistance)




def generate_assistance(user_info):
    prompt = f"I am asking a question and I want you to answer it in a mean and disrespectful way. {user_info['user']}"
    print(prompt)
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are a stupid assistant and very very mean and disrespectful."},

            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run()
