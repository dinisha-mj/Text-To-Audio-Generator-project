from flask import Flask, render_template, request, redirect, session, send_file
import subprocess
import os

app = Flask(__name__)
app.secret_key = "speech_secret"

OUTPUT_FILE = "output.wav"

USERNAME = "admin"
PASSWORD = "1234"


# Home Page
@app.route("/")
def home():
    return render_template("home.html")


# Login Page
@app.route("/login")
def login_page():
    return render_template("login.html")


# Login Authentication
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    if username == USERNAME and password == PASSWORD:
        session["user"] = username
        return redirect("/generator")

    return "Invalid username or password"


# Speech Generator Page
@app.route("/generator")
def generator():

    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# Text to Speech
@app.route("/speak", methods=["POST"])
def speak():

    text = request.form.get("text")
    speed = request.form.get("speed")
    voice = request.form.get("voice")

    if not text:
        return "No text", 400

    speed_map = {
        "0.5": "90",
        "1": "175",
        "1.5": "250",
        "2": "350"
    }

    cmd = [
        "espeak-ng",
        "-v", voice,
        "-s", speed_map.get(speed, "175"),
        "-w", OUTPUT_FILE,
        text
    ]

    subprocess.run(cmd)

    if not os.path.exists(OUTPUT_FILE):
        return "Audio generation failed", 500

    return send_file(OUTPUT_FILE, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)