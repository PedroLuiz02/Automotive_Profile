import sqlite3

def conectar():
    conn = sqlite3.connect("instance/database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn