# CodeAlpha Cyber Security Internship

## Task 3: Secure Coding Review

### Project Title

**Secure Coding Review of a Python Authentication Application**

**Intern:** Vansh
**Organization:** CodeAlpha
**Domain:** Cyber Security
**Task:** Task 3 – Secure Coding Review
**Programming Language:** Python

---

## 1. Introduction

This project was completed as part of the CodeAlpha Cyber Security Internship.

The objective of this task was to review a Python-based authentication application, identify security vulnerabilities, apply secure coding practices, and document the security improvements.

The project contains an intentionally vulnerable version of an authentication application and a secure version containing the recommended security fixes.

---

## 2. Objectives

The main objectives of this project were:

* Identify security vulnerabilities in application code.
* Understand the security impact of each vulnerability.
* Apply secure coding practices.
* Protect user authentication information.
* Improve input validation.
* Implement secure password storage.
* Prevent SQL injection.
* Avoid exposing sensitive application errors.
* Document the complete security review.

---

## 3. Project Environment

### Software Used

* Python 3
* SQLite
* Visual Studio Code
* Windows
* Git and GitHub

### Python Modules Used

* `sqlite3`
* `os`
* `hashlib`
* `hmac`
* `logging`

---

## 4. Project Structure

```text
CodeAlpha_SecureCodingReview/
│
├── vulnerable_app.py
├── secure_app.py
├── security_review.md
└── .gitignore
```

The application also creates local database and log files during testing.

These files are excluded from GitHub using `.gitignore` because they are local testing files and are not required in the public source-code repository.

---

## 5. Application Overview

The application is a simple Python authentication system using SQLite.

The vulnerable version demonstrates common insecure coding practices.

The secure version applies security improvements including:

* Parameterized SQL queries
* Password hashing
* Random password salts
* Input validation
* Secure error handling
* Error logging
* Environment variables for configuration

---

# 6. Security Review Methodology

The following steps were used during the security review:

1. Reviewed the source code.
2. Identified insecure coding practices.
3. Classified vulnerabilities according to their potential security impact.
4. Implemented secure alternatives.
5. Tested the secure application.
6. Updated the security documentation.
7. Prepared the project for GitHub submission.

---

# 7. Security Findings Summary

| ID     | Vulnerability              | Severity | Status |
| ------ | -------------------------- | -------- | ------ |
| SEC-01 | SQL Injection              | High     | Fixed  |
| SEC-02 | Hardcoded Secret           | High     | Fixed  |
| SEC-03 | Plaintext Password Storage | High     | Fixed  |
| SEC-04 | Missing Input Validation   | Medium   | Fixed  |
| SEC-05 | Insecure Error Handling    | Medium   | Fixed  |

---

# 8. Detailed Security Findings

## SEC-01: SQL Injection

### Description

The vulnerable application constructed an SQL query using user-provided input.

Example:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

Directly inserting user input into an SQL query can allow malicious input to modify the intended database query.

### Risk

Potential consequences include:

* Unauthorized database access
* Authentication bypass
* Exposure or modification of database information

### Remediation

The secure application uses parameterized SQL queries.

Example:

```python
cursor.execute(
    """
    SELECT password_hash, salt
    FROM users
    WHERE username = ?
    """,
    (username,)
)
```

The user input is supplied separately from the SQL statement.

### Status

**Fixed and tested.**

---

# 9. SEC-02: Hardcoded Secret

### Description

The vulnerable application contained a secret directly in the source code.

Example:

```python
API_KEY = "DEMO_SECRET_12345"
```

Hardcoded secrets can accidentally become publicly accessible if source code is shared or uploaded to a repository.

### Risk

Potential consequences include:

* Credential exposure
* Unauthorized access to services
* Difficulty rotating compromised credentials

### Remediation

The secure version reads the value from an environment variable:

```python
API_KEY = os.getenv("CODEALPHA_DEMO_API_KEY")
```

Real credentials should never be placed directly inside source code.

### Status

**Fixed and tested.**

---

# 10. SEC-03: Plaintext Password Storage

### Description

The vulnerable application stored user passwords directly in the database.

Example:

```text
username | password
testuser | test123
```

Storing plaintext passwords creates a significant security risk if the database is exposed.

### Risk

An attacker who obtains the database could directly read user passwords.

### Remediation

The secure application uses:

* PBKDF2-HMAC
* SHA-256
* A randomly generated salt
* 600,000 hashing iterations

Passwords are not stored directly.

Instead, the application stores a password hash and a unique salt.

Example:

```python
password_hash = hashlib.pbkdf2_hmac(
    "sha256",
    password.encode("utf-8"),
    salt,
    600_000
)
```

Password verification uses:

```python
hmac.compare_digest(password_hash, stored_hash)
```

### Status

**Fixed and tested.**

---

# 11. SEC-04: Missing Input Validation

### Description

The original application accepted username and password input without checking whether the values were empty or excessively long.

### Risk

Insufficient input validation can lead to:

* Unexpected application behavior
* Excessive input processing
* Poor error handling
* Increased attack surface

### Remediation

The secure application validates authentication input before processing it.

The application checks:

* Empty username
* Empty password
* Username length
* Password length

Example:

```python
def validate_input(username, password):
    if not username or not password:
        return False, "Username and password are required."

    if len(username) > 50:
        return False, "Username is too long."

    if len(password) > 128:
        return False, "Password is too long."

    return True, ""
```

### Status

**Fixed and tested.**

---

# 12. SEC-05: Insecure Error Handling

### Description

The original application did not provide structured handling for database errors.

Unexpected database errors could potentially expose technical information to users if exceptions were allowed to reach the interface.

### Risk

Detailed technical errors may reveal:

* Database information
* File paths
* Application implementation details
* Internal system information

### Remediation

The secure application catches SQLite errors and records technical information in a log file.

Users receive a generic message:

```text
An internal error occurred. Please try again later.
```

The application uses Python's `logging` module:

```python
logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

Database operations are handled using exception handling:

```python
except sqlite3.Error:
    logging.exception("Database error during login")
    print("An internal error occurred. Please try again later.")
```

### Status

**Fixed and tested.**

---

# 13. Secure Coding Improvements Implemented

The following security improvements were implemented:

### 1. Parameterized SQL Queries

Prevents user input from being directly combined with SQL statements.

### 2. Password Hashing

Passwords are processed using PBKDF2-HMAC with SHA-256.

### 3. Random Password Salts

Each password receives a randomly generated salt.

### 4. Environment Variables

Sensitive configuration values are loaded using environment variables instead of hardcoding them.

### 5. Input Validation

Authentication input is checked before database processing.

### 6. Secure Error Handling

Database errors are handled without exposing technical details to users.

### 7. Error Logging

Technical error information is recorded in a local log file for troubleshooting.

### 8. Git Security

Database and log files are excluded from the GitHub repository using `.gitignore`.

---

# 14. Testing Performed

The secure application was tested using several scenarios.

## Test 1: Valid Login

Input:

```text
Username: testuser
Password: test123
```

Result:

```text
Login successful
```

**Status: Passed**

---

## Test 2: Invalid Password

Input:

```text
Username: testuser
Password: incorrect_password
```

Result:

```text
Invalid username or password
```

**Status: Passed**

---

## Test 3: Empty Input

Empty username or password was supplied.

Result:

```text
Username and password are required.
```

**Status: Passed**

---

## Test 4: Excessive Input Length

Input exceeding the configured username or password length was tested.

Result:

```text
Username is too long.
```

or:

```text
Password is too long.
```

**Status: Passed**

---

## Test 5: Secure Password Storage

The secure database stores password hashes and salts instead of plaintext passwords.

**Status: Passed**

---

## Test 6: Parameterized SQL

The secure application uses parameterized SQL queries.

**Status: Passed**

---

## Test 7: Error Handling

Database errors are handled using exception handling and logged without exposing internal technical details to the user.

**Status: Passed**

---

# 15. Tools Used

* Visual Studio Code
* Python
* SQLite
* Python `hashlib`
* Python `hmac`
* Python `logging`
* Git
* GitHub

---

# 16. Security Best Practices Demonstrated

This project demonstrates the following secure coding principles:

* Never trust user input.
* Use parameterized database queries.
* Never store plaintext passwords.
* Use strong password hashing with salts.
* Avoid hardcoded secrets.
* Validate input before processing.
* Do not expose internal errors to users.
* Log security-relevant errors safely.
* Keep sensitive local files out of public repositories.

---

# 17. Project Status

The secure coding review has been completed.

### Completed Tasks

* [x] Project setup
* [x] Vulnerable authentication application
* [x] Security vulnerability identification
* [x] SQL Injection remediation
* [x] Hardcoded secret remediation
* [x] Plaintext password remediation
* [x] Password hashing implementation
* [x] Input validation
* [x] Secure error handling
* [x] Error logging
* [x] Secure authentication testing
* [x] Security documentation
* [x] `.gitignore` configuration

---

# 18. Conclusion

The security review identified several common vulnerabilities in the original authentication application.

The secure version applies appropriate secure coding practices to reduce the identified risks.

The final application uses parameterized SQL queries, secure password hashing, random salts, input validation, environment-based configuration, and controlled error handling.

This project demonstrates the importance of reviewing source code for security issues and applying secure development practices before deploying an application.

---

# 19. Disclaimer

This project was created for educational purposes as part of the CodeAlpha Cyber Security Internship.

The vulnerable code is intentionally insecure and is intended only for local security review and learning.

No unauthorized systems or third-party applications were targeted during this project.

---

# 20. Final Project Files

```text
CodeAlpha_SecureCodingReview/
│
├── vulnerable_app.py
├── secure_app.py
├── security_review.md
└── .gitignore
```

Local runtime files such as SQLite databases, log files, and Python cache files are excluded from the public repository.
