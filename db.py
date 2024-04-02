import sqlite3 as sql

db = "bestreads.db"

def get_user_by_name(user):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM users WHERE username = ?", (user,)).fetchone() 
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None

    return res

def get_user_by_id(id):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None

    return res

def get_books_by_user(id, shelf):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    rows = conn.execute(("SELECT * FROM books WHERE id IN (SELECT book_id FROM " + shelf + " WHERE user_id = ?)"), (id, )).fetchall()
    conn.close()

    res = []
    for row in rows:
        if row:
            res.append(dict(row))

    return res

def get_book_by_isbn(isbn):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute(("SELECT * FROM books WHERE isbn = ?"), (isbn, )).fetchone()
    conn.close()

    if row:
        res= dict(row)
    else:
        res = None

    return res

def get_shelf_by_isbn(id, isbn, shelf):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM " + shelf + " WHERE user_id = ? AND book_id = (SELECT book_id FROM books WHERE isbn = ?)", (id, isbn)).fetchone()
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None

    return res

def get_recent_updates(id):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    rows = conn.execute("SELECT u.type, u.date, b.* FROM updates as u INNER JOIN books as b ON u.book_id = b.id WHERE user_id = ? ORDER BY date DESC LIMIT 10", (id,)).fetchall()
    conn.close()

    res = []
    for row in rows:
        if row:
            res.append(dict(row))

    return res

def get_review(id, isbn):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM reviews WHERE user_id = ? AND book_id = (SELECT id FROM books WHERE isbn = ?)", (id, isbn)).fetchone()
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None
    
    return res

def insert_user(username, hash):
    conn = sql.connect(db)
    conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
    conn.commit()
    conn.close()

def insert_book(book):
    conn = sql.connect(db)
    conn.execute("INSERT INTO books (isbn, title, subtitle, author, publisher, published_date, " +
                 "description, page_count, categories, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (book["isbn"], book["title"], book["subtitle"], book["author"], book["publisher"], book["published_date"], 
                    book["description"], book["page_count"], book["categories"], book["image"]))
    conn.commit()
    conn.close()

def insert_to_shelf(user, shelf, isbn, timestamp):
    conn = sql.connect(db)
    book_id = conn.execute("SELECT id FROM books WHERE isbn = ?", (isbn,)).fetchone()[0]
    conn.execute("INSERT INTO " + shelf + " (user_id, book_id, date) VALUES (?, ?, ?)",(user, book_id, timestamp,))
    conn.commit()
    conn.close()

def insert_update(user, isbn, type, timestamp):
    conn = sql.connect(db)
    book_id = conn.execute("SELECT id FROM books WHERE isbn = ?", (isbn,)).fetchone()[0]
    conn.execute("INSERT INTO updates (user_id, book_id, type, date) VALUES (?, ?, ?, ?)", (user, book_id, type, timestamp))
    conn.commit()
    conn.close()

def insert_review(user, rating, isbn, text=None):
    conn = sql.connect(db)
    book_id = conn.execute("SELECT id FROM books WHERE isbn = ?", (isbn,)).fetchone()[0]
    conn.execute("INSERT INTO reviews (user_id, book_id, rating, text) VALUES (?, ?, ?, ?)", (user, book_id, rating, text))
    conn.commit()
    conn.close()

def update_review(user, rating, isbn, text=None):
    conn = sql.connect(db)
    book_id = conn.execute("SELECT id FROM books WHERE isbn = ?", (isbn,)).fetchone()[0]
    conn.execute("UPDATE reviews SET rating = ?, text = ? WHERE book_id = ? AND user_id = ?", (rating, text, book_id, user))
    conn.commit()
    conn.close()

def delete_from_shelf(user, isbn, shelf):
    conn = sql.connect(db)
    conn.execute("DELETE FROM " + shelf + " WHERE user_id = ? AND book_id = (SELECT id FROM books WHERE isbn = ?)", (user, isbn))
    conn.commit()
    conn.close()

def delete_review(user, isbn):
    conn = sql.connect(db)
    conn.execute("DELETE FROM reviews WHERE user_id = ? AND book_id = (SELECT id FROM books WHERE isbn = ?)", (user, isbn))
    conn.commit()
    conn.close()
