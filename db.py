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

def get_books(id, shelf):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    rows = conn.execute("SELECT * FROM " + shelf + " WHERE user_id = ? ORDER BY date DESC", (id, )).fetchall()
    conn.close()

    res = []
    for row in rows:
        if row:
            res.append(dict(row))

    return res

def get_book_by_isbn(id, isbn, shelf):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM " + shelf + " WHERE user_id = ? AND isbn = ?", (id, isbn)).fetchone()
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None

    return res

def get_recent_updates(id):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    rows = conn.execute("SELECT * FROM updates WHERE user_id = ? ORDER BY date DESC LIMIT 10", (id,)).fetchall()
    conn.close()

    res = []
    for row in rows:
        if row:
            res.append(dict(row))

    return res

def insert_user(username, hash):
    conn = sql.connect(db)
    conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
    conn.commit()
    conn.close()

def insert_book(user, book, shelf, timestamp):
    conn = sql.connect(db)
    conn.execute("INSERT INTO " + shelf + " (user_id, isbn, title, subtitle, author, publisher, published_date, " +
                 "description, page_count, categories, image, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user, book["isbn"], book["title"], book["subtitle"], book["author"], book["publisher"], book["published_date"], 
                    book["description"], book["page_count"], book["categories"], book["image"], timestamp))
    conn.commit()
    conn.close()

def insert_update(user, book, type, timestamp):
    conn = sql.connect(db)
    conn.execute("INSERT INTO updates (user_id, type, title, subtitle, isbn, image, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (user, type, book["title"], book["subtitle"], book["isbn"], book["image"], timestamp))
    conn.commit()
    conn.close()

def delete_book(user, isbn, shelf):
    conn = sql.connect(db)
    conn.execute("DELETE FROM " + shelf + " WHERE user_id = ? AND isbn = ?", (user, isbn))
    conn.commit()
    conn.close()

