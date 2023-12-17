from flask import render_template, request, url_for, redirect
from flask import Flask
from app import app

# Receivables route
@app.route("/receivables", strict_slashes=False)
def receivables():
    return render_template("receivables.html")