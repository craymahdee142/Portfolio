from flask import render_template, request, url_for, redirect
from flask import Flask
from app import app

# perform booking operations for accounts
@app.route("/bookings", strict_slashes=False)
def bookings():
    
    return render_template("bookings.html")