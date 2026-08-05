---
# Spec: Registration

## Overview
This feature implements user registration, allowing new users to create an account in the Spendly application. It handles the form submission, validates the input, hashes the password, and creates a new user record in the database.

## Depends on
01-database-setup

## Routes
- `POST /register` — Handle registration form submission, validate input, create user, and redirect — public

## Database changes
No database changes.

## Templates
- **Create:** No new templates
- **Modify:** `templates/register.html` — Add form action, method (POST), and name attributes to inputs; display flash messages for errors.

## Files to change
- `app.py`
- `templates/register.html`

## Files to create
No files to create.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`

## Definition of done
- Navigating to `/register` displays the registration form.
- Submitting the form with a new email creates a user record in the database with a hashed password.
- Submitting the form with an existing email displays an error message (flash message).
- Successful registration redirects the user to the login page with a success message.
- The route uses parameterised queries to prevent SQL injection.
- Passwords are encrypted using `werkzeug.security.generate_password_hash`.
---
