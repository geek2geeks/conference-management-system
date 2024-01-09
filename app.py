from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/signUp.html")
def signUp():
    return render_template('signUp.html')