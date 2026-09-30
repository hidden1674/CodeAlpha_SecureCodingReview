import sqlite3
import os
import hashlib
import hmac
import logging


API_KEY = os.getenv("CODEALPHA_DEMO_API_KEY")


# Secure error logging
logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000
    )

    return salt, password_hash


def verify_password(password, salt, stored_hash):
    _, password_hash = hash_password(password, salt)

    return hmac.compare_digest(password_hash, stored_hash)


def validate_input(username, password):
    if not username or not password:
        return False, "Username and password are required."

    if len(username) > 50:
        return False, "Username is too long."

    if len(password) > 128:
        return False, "Password is too long."

    return True, ""


def setup_database():
    connection = None

    try:
        connection = sqlite3.connect("users_secure.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash BLOB NOT NULL,
                salt BLOB NOT NULL
            )
        """)

        cursor.execute(
            "SELECT id FROM users WHERE username = ?",
            ("testuser",)
        )

        existing_user = cursor.fetchone()

        if existing_user is None:
            salt, password_hash = hash_password("test123")

            cursor.execute(
                """
                INSERT INTO users
                (username, password_hash, salt)
                VALUES (?, ?, ?)
                """,
                ("testuser", password_hash, salt)
            )

        connection.commit()

    except sqlite3.Error:
        logging.exception("Database setup error")
        print("An internal error occurred. Please try again later.")

    finally:
        if connection:
            connection.close()


def login(username, password):

    # Input validation
    valid, message = validate_input(username, password)

    if not valid:
        print(message)
        return

    connection = None

    try:
        connection = sqlite3.connect("users_secure.db")
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT password_hash, salt
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        if user is None:
            print("Invalid username or password")
            return

        stored_hash, salt = user

        if verify_password(password, salt, stored_hash):
            print("Login successful")
        else:
            print("Invalid username or password")

    except sqlite3.Error:
        logging.exception("Database error during login")
        print("An internal error occurred. Please try again later.")

    finally:
        if connection:
            connection.close()


setup_database()

username = input("Username: ")
password = input("Password: ")

login(username, password)