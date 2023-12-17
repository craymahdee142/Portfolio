from flask import render_template, request, url_for, redirect
from flask import Flask
from app import app

@app.route("/ledger", strict_slashes=False)
def ledger():
    return render_template("ledger.html")
"""
@app.route("/period", strict_slashes=False)
def period():
    return render_template("period.html")
"""
@app.route("/incomeStatement", strict_slashes=False)
def incomeStatement():
    return render_template("incomeStatement.html")
