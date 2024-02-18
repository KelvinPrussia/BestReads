from functools import wraps

from flask import redirect, session

def login_required(f):
    # wrapper function for forcing login on certain pages
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # if no user logged in, redirect to login
        if session.get("user_id") is None:
                return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def map_searched_data(search_data):
    books = []

    # iterate through all books in search
    for item in search_data["items"]:

        # handle nested data seperately
        volume_info = item["volumeInfo"]
        authors = volume_info.get("authors", "Unknown")
        authors = ", ".join(authors) if isinstance(authors, list) else authors
        categories = volume_info.get("categories", "Unknown")
        categories = ", ".join(categories) if isinstance(categories, list) else categories
        isbns = volume_info.get("industryIdentifiers", [])
        isbn_13 = "Unknown"
        # only use isbn13 data (isbn10 deprecated)
        for isbn in isbns:
            if isbn["type"] == "ISBN_13":
                isbn_13 = isbn["identifier"]
        
        # map useful data from search to new book dict
        book = {
            "title":  volume_info.get("title", "Unknown"),
            "subtitle": volume_info.get("subtitle", "Unknown"),
            "author": authors,
            "publisher": volume_info.get("publisher", "Unknown"),
            "published_date": volume_info.get("publishedDate", "Unknown"),
            "description": volume_info.get("description", "Unknown"),
            "isbn": isbn_13,
            "page_count": volume_info.get("pageCount", "Unknown"),
            "categories": categories,
            "avg_rating": volume_info.get("averageRating", "Unknown"),
            "rating_count": volume_info.get("ratingsCount", "Unknown"),
            "image": volume_info.get("imageLinks", {}).get("thumbnail", "static/blankbook.jpg")
        }

        # add book to books list
        books.append(book)
    
    return books
     