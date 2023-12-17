from flask import render_template, url_for, redirect
from flask import Flask
from app import app

@app.route("/payables", strict_slashes=False)
def payables():
    return render_template("payables.html")
