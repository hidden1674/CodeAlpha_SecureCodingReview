# CodeAlpha Secure Coding Review

## Cyber Security Internship – Task 3

This project was completed as part of the CodeAlpha Cyber Security Internship.

The objective of this task is to review a Python application and identify potential security vulnerabilities. The review focuses on common secure coding problems and provides recommendations for improving the application's security.

## Application Reviewed

Language: Python

Application: Simple User Login Application

The application uses SQLite to store user credentials and authenticate users.

## Security Vulnerabilities Identified

### 1. SQL Injection

The application directly concatenates user input into an SQL query.

This can allow an attacker to manipulate the SQL statement through specially crafted input.

**Risk:**  
Potential authentication bypass or unauthorized database access.

**Recommendation:**  
Use parameterized SQL queries instead of directly concatenating user input.

---

### 2. Plain-Text Password Handling

The application stores and compares passwords as plain text.

**Risk:**  
If the database is compromised, stored passwords could be exposed directly.

**Recommendation:**  
Passwords should never be stored as plain text. Use secure password hashing algorithms such as Argon2, bcrypt, or scrypt.

---

### 3. Missing Input Validation

The application accepts username and password input without performing appropriate validation.

**Risk:**  
Unexpected or malicious input may cause security problems or unexpected application behavior.

**Recommendation:**  
Validate user input by applying suitable length, format, and character checks. Parameterized queries should also be used for database operations.

---

### 4. Lack of Secure Authentication Design

The application directly compares the entered password with the password stored in the database.

**Risk:**  
This approach can expose credentials if the database is compromised.

**Recommendation:**  
Store password hashes instead of plain-text passwords and verify passwords securely during authentication.

## Secure Coding Recommendations

- Use parameterized SQL queries.
- Never store passwords in plain text.
- Use secure password hashing.
- Validate and sanitize user input.
- Follow the principle of least privilege.
- Avoid exposing sensitive information in error messages.
- Keep dependencies and libraries updated.
- Perform regular security testing and code reviews.

## Project Files

- `vulnerable_app.py` – Python application reviewed during the security audit.
- `security_review.txt` – Detailed vulnerability findings and recommendations.
- `README.md` – Project documentation.

## Conclusion

The security review identified several common vulnerabilities in the application, including SQL injection, plain-text password handling, missing input validation, and insecure authentication design.

Implementing the recommended secure coding practices would significantly improve the security and reliability of the application.