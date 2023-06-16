import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{generate_prompt(title, description)}"},
            ],
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(title, description):
    return """Repeat the course title and suggest three skill tags for an online course. Limit your response to the list of possible tags.

Here are the possible tags (one on each line):
C (Programming Language)
C#
Communication
Programming
C++
Java
Kotlin
JavaScript
TypeScript
Leadership
Management
Culture

Title: Guiding a Team
Description: Learn how to help a team become stronger, more resilient, and more productive
Tags: Tags for "Guiding a Team": Culture, Management, Leadership

Title: Learning to Code
Description: Being your programming journey and explore some of the most common programming languages used today.
Tags: Tags for "Learning to Code": JavaScript, Programming, C#

Title: {}
Description: {}
Tags:""".format(title.capitalize(), description.capitalize())
