from flask import render_template, request, url_for, redirect
from flask import Flask
from app import app

# Expenses route
@app.route("/expenses", strict_slashes=False)
def expenses():
    return render_template("expenses.html")
