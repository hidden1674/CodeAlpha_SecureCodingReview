import sqlite3

API_KEY = "DEMO_SECRET_12345"


def setup_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO users (id, username, password)
        VALUES (1, 'testuser', 'test123')
    """)

    connection.commit()
    connection.close()


def login(username, password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Intentionally vulnerable code for security review
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    cursor.execute(query)

    user = cursor.fetchone()

    if user:
        print("Login successful")
    else:
        print("Invalid username or password")

    connection.close()


setup_database()

username = input("Username: ")
password = input("Password: ")

login(username, password)