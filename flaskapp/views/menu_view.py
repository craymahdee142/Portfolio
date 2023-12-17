from flask import render_template
from flask import Flask
from app import app

@app.route("/menu", strict_slashes=False)
def menu():
    return render_template("menu.html")