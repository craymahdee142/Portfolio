from flask import render_template, request, url_for
from flask import Flask
from app import app

@app.route("/income", strict_slashes=False)
def income():
    return render_template("income.html")