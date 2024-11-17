import sqlite3


conn = sqlite3.connect('stocks.db')


cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    stock TEXT NOT NULL
)
''')


conn.commit()
conn.close()

print("Database and table created successfully.")
