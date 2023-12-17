
from flask import render_template, url_for, redirect, request
from flask import Flask, flash
from app import app, db

@app.route("/book", strict_slashes=False)
def book():
    return render_template("book.html")

 # Route to reservation page 
@app.route("/addline", strict_slashes=False)
def addline():
    return render_template("addline.html")


@app.route("/book/reserve", strict_slashes=False)
def reserve():
   
   return render_template("reserve.html")

