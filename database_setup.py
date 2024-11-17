import sqlite3

# Connect to database (or create it)
conn = sqlite3.connect('stocks.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the 'users' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    stock TEXT NOT NULL
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
