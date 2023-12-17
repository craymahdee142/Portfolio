
from flask import render_template, url_for, redirect
from flask import Flask
from app import app

@app.route("/login", strict_slashes=False)
def log_in():
    return render_template("login.html")

@app.route("/signup", strict_slashes=False)
def sign_up():
    return render_template("signup.html")

