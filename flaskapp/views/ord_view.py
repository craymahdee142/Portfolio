from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from app import app, db

#Route to ord_line page
@app.route("/ord_line", strict_slashes=False)
def ord_line():
    return render_template("ord_line.html")

#Route to ord page
@app.route("/ord_line/ord", strict_slashes=False)
def ord():
    return render_template("ord.html")


