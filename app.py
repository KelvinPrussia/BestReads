import ast
import datetime
import json
import db

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from urllib.request import urlopen

from helpers import login_required, map_searched_data


# Configure app
app = Flask(__name__)

# Configure session to use filesystem instead of client-side cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure responses to include headers that prevent caching
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    # Clear current session
    session.clear()

    if request.method == "POST":
        # Get username/password input from form
        username = request.form.get("username")
        password = request.form.get("password")

        # Query db for username
        user = db.get_user_by_name(username)

        # Check user exists and password is correct
        if user == None or not check_password_hash(user["hash"], password):
            return render_template("login.html", wrong_credentials=True)
        
        # Set current user in session
        session["user_id"] = user["id"]

        # Redirect to homepage
        return redirect('/')
         
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Set input values from request
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check that password/confirmation are the same, show error on page reload
        if password != confirmation:
            return render_template("register.html", incorrect_confirm=True)
        # check if username already used, show error on page reload
        elif db.get_user_by_name(username):
            return render_template("register.html", user_exists=True)
        
        # insert user into database with hash
        db.insert_user(username, generate_password_hash(password))

        return redirect("/")

    return render_template("register.html")


@app.route("/logout")
def logout():
    # Clear user id for current session
    session.clear()

    # Redirect to home/login
    return redirect("/")


@app.route("/")
@login_required
def index():
     return render_template("index.html")


@app.route("/search", methods=["POST"])
@login_required
def search():
    # get search from form and ensure correct format
    search_term = request.form.get("search").replace(" ", "+")

    url = "https://www.googleapis.com/books/v1/volumes?q=" + search_term + "&maxResults=40&startIndex=0&langRestrict=en"

    # get response from googlebooks api url with search term
    resp = urlopen(url)

    # extract and map useful data from the api response
    books = map_searched_data(json.load(resp))

    return render_template("index.html", books=books)

@app.route("/addtoshelf", methods=["POST"])
@login_required
def add_to_shelf():
    # convert string of book data to dict
    book = ast.literal_eval(request.form.get("book"))
    user_id = session["user_id"]

    if request.form.get("shelf") == "read":
        # check if already in read/tbr database for user
        check_read = db.get_read_by_isbn(user_id, book["isbn"])
        check_tbr  = db.get_tbr_by_isbn(user_id, book["isbn"])

        # if record exists in read, redirect to profile, else add to db and remove from tbr if there
        if check_read:
            return redirect("/profile")
        else:
            if check_read:
                db.delete_tbr(user_id, book["isbn"])
            db.insert_read(user_id, book)
    else:
        # check if already in read/tbr database for user
        check_read = db.get_read_by_isbn(user_id, book["isbn"])
        check_tbr = db.get_tbr_by_isbn(user_id, book["isbn"])

        # if record exists, redirect to profile, else add to db and remove from read if there
        if check_tbr:
            return redirect("/profile")
        else:
            if check_read:
                db.delete_read(user_id, book["isbn"])
            db.insert_tbr(user_id, book)

    return redirect("/profile")

@app.route("/profile")
@login_required
def profile():
    # get current user information
    user_id = session["user_id"]
    user = db.get_user_by_id(user_id)
    username = user["username"]

    # get read + tbr books from bd
    read = db.get_read(user_id)
    tbr = db.get_tbr(user_id)

    return render_template("profile.html", username=username, read=read, tbr=tbr)

if __name__ == "__main__":
    app.run(debug=True, port=8001)