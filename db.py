import sqlite3 as sql

db = "bestreads.db"

def get_user(user):
    conn = sql.connect(db)
    conn.row_factory = sql.Row

    row = conn.execute("SELECT * FROM users").fetchone()
    res = dict(row)

    conn.close()
    return res