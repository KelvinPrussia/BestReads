import ast
from datetime import datetime
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
     updates = db.get_recent_updates(session["user_id"])
     return render_template("index.html", updates=updates)


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

    return render_template("search.html", books=books)


@app.route("/addtoshelf", methods=["POST"])
@login_required
def add_to_shelf():
    # convert string of book data to dict
    book = ast.literal_eval(request.form.get("book"))
    user_id = session["user_id"]
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    shelf = request.form.get("shelf")

    check_read = db.get_book_by_isbn(user_id, book["isbn"], "read")
    check_tbr  = db.get_book_by_isbn(user_id, book["isbn"], "tbr")

    if shelf == "read":
        # if book already exists in read, redirect to profile
        if check_read:
            return redirect("/profile")
        else:
            if check_tbr:
                db.delete_book(user_id, book["isbn"], "tbr")
    else:
        # if book already exists in tbr, redirect to profile
        if check_tbr:
            return redirect("/profile")
        # if book already exists in read, delete before adding to tbr
        if check_read:
            db.delete_book(user_id, book["isbn"], "read")
    
    # insert entry into tbr or read table and update table
    db.insert_book(user_id, book, shelf, timestamp)
    db.insert_update(user_id, book, shelf, timestamp)

    return redirect("/profile")


@app.route("/profile")
@login_required
def profile():
    # get current user information
    user_id = session["user_id"]
    user = db.get_user_by_id(user_id)
    username = user["username"]

    # get read + tbr books from bd
    read = db.get_books(user_id, "read")
    tbr = db.get_books(user_id, "tbr")

    return render_template("profile.html", username=username, read=read, tbr=tbr)


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    # Delete record of book from shelf (via profile)
    user_id = session["user_id"]
    book = ast.literal_eval(request.form.get("book"))
    shelf = request.form.get("shelf")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    db.delete_book(user_id, book["isbn"], shelf)
    db.insert_update(user_id, book, "delete", timestamp)

    return redirect("/profile")


@app.route("/book")
@login_required
def book():
    # Show all information for a book
    isbn = request.args.get("isbn")
    url = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn + "&maxResults=1&startIndex=0&langRestrict=en"
    
    resp = urlopen(url)

    book = map_searched_data(json.load(resp))[0]

    return render_template("book.html", book=book)


if __name__ == "__main__":
    app.run(debug=True, port=8001)