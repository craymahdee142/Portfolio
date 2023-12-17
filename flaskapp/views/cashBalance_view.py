from flask import render_template, request, url_for, redirect
from flask import Flask
from app import app

# Cash at bank route
@app.route("/cashBalance", strict_slashes=False)
def cashBalance():
    return render_template("cashBalance.html")