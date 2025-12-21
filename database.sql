import sqlite3
conn = sqlite3.connect('database.db')
conn.execute('''CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at DATE NOT NULL
)''')
conn.execute('''CREATE TABLE IF NOT EXISTS url_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_id INTEGER,
    status_code INTEGER,
    h1 TEXT,
    title TEXT,
    description TEXT,
    created_at DATE NOT NULL,
    FOREIGN KEY(url_id) REFERENCES urls(id)
)''')
conn.commit()
conn.close()
exit()