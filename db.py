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

def get_read(id):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    rows = conn.execute("SELECT * FROM read WHERE user_id = ?", (id,)).fetchall()
    conn.close()

    res = []
    for row in rows:
        if row:
            res.append(dict(row))

    return res

def get_read_by_isbn(id, isbn):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM read WHERE user_id = ? AND isbn = ?", (id, isbn,)).fetchone()
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None

    return res

def get_tbr(id):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    rows = conn.execute("SELECT * FROM tbr WHERE user_id = ?", (id,)).fetchall()
    conn.close()

    res = []
    for row in rows:
        if row:
            res.append(dict(row))

    return res

def get_tbr_by_isbn(id, isbn):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM tbr WHERE user_id = ? AND isbn = ?", (id, isbn,)).fetchone()
    conn.close()

    if row:
        res = dict(row)
    else:
        res = None

    return res

def insert_user(username, hash):
    conn = sql.connect(db)
    conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash,))
    conn.commit()
    conn.close()

def insert_read(user, book):
    conn = sql.connect(db)
    conn.execute("INSERT INTO read (user_id, isbn, title, subtitle, author, publisher, published_date, " +
                 "description, page_count, categories, avg_rating, rating_count, image_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user, book["isbn"], book["title"], book["subtitle"], book["author"], book["publisher"], book["published_date"], 
                    book["description"], book["page_count"], book["categories"], book["avg_rating"], book["rating_count"], book["image"]))
    conn.commit()
    conn.close()

def insert_tbr(user, book):
    conn = sql.connect(db)
    conn.execute("INSERT INTO tbr (user_id, isbn, title, subtitle, author, publisher, published_date, " +
                 "description, page_count, categories, avg_rating, rating_count, image_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user, book["isbn"], book["title"], book["subtitle"], book["author"], book["publisher"], book["published_date"], 
                    book["description"], book["page_count"], book["categories"], book["avg_rating"], book["rating_count"], book["image"]))
    conn.commit()
    conn.close()

def delete_read(user, isbn):
    conn = sql.connect(db)
    conn.execute("DELETE FROM read WHERE user_id = ? AND isbn = ?", (user, isbn,))

def delete_tbr(user, isbn):
    conn = sql.connect(db)
    conn.execute("DELETE FROM tbr WHERE user_id = ? AND isbn = ?", (user, isbn,))
