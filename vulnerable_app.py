import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
""")

# Add a demo user
cursor.execute("""
INSERT OR IGNORE INTO users (username, password)
VALUES ('admin', 'admin123')
""")

conn.commit()

username = input("Enter username: ")
password = input("Enter password: ")

query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
cursor.execute(query)

user = cursor.fetchone()

if user:
    print("Login successful!")
else:
    print("Invalid username or password.")

conn.close()