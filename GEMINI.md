# GEMINI.md - Spendly Project Guide

Welcome! This file provides essential guidelines, architecture overview, tech stack details, folder structure, and development commands for AI coding assistants and developers working on the **Spendly** repository.

---

## 1. Project Overview

**Spendly** is a lightweight, full-stack personal expense tracking web application built with Python and Flask. It provides user authentication, expense logging, categorization, and visual financial tracking.

---

## 2. Tech Stack

- **Backend Framework**: Python 3.x with Flask `3.1.3`
- **WSGI / Utilities**: Werkzeug `3.1.6`
- **Database**: SQLite3 (managed via helper routines in `database/db.py`)
- **Frontend**:
  - Templating: Jinja2 (HTML5 template inheritance)
  - Styling: Vanilla CSS (Custom properties, CSS Grid/Flexbox, responsive layout)
  - Interactivity: Vanilla JavaScript (ES6+, native DOM API, no external JS frameworks)
- **Testing**: Pytest `8.3.5` with `pytest-flask` `1.3.0`

---

## 3. Directory & Folder Structure

```
Expense Tracker/
├── app.py                  # Main Flask application entry point and route handlers
├── requirements.txt        # Python dependencies (Flask, Werkzeug, Pytest)
├── GEMINI.md               # AI assistant & project documentation guide
├── database/
│   ├── __init__.py
│   └── db.py               # SQLite database setup helper (get_db, init_db, seed_db)
├── static/
│   ├── css/
│   │   ├── style.css       # Global styles and layout rules
│   │   └── landing.css     # Landing page specific styles
│   └── js/
│       └── main.js         # Global JavaScript file for interactive features
├── templates/
│   ├── base.html           # Master layout template (Navbar, Footer, Blocks)
│   ├── landing.html        # Landing page template
│   ├── login.html          # User login view
│   ├── register.html       # User registration view
│   ├── privacy.html        # Privacy Policy template
│   └── terms.html          # Terms and Conditions template
└── venv/                   # Python virtual environment (ignored in git)
```

---

## 4. Common Commands & Workflows

### Setup & Environment Activation
```bash
# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run directly via Python entry point (default port 5001 with debug mode)
python app.py

# Alternatively, run using Flask CLI
flask run --port=5001
```

### Running Tests
```bash
# Run pytest test suite
pytest
```

---

## 5. Architecture & Design Patterns

1. **Routing & Server Logic (`app.py`)**:
   - Core routes are mapped directly using Flask route decorators (`@app.route`).
   - Page view handlers render Jinja templates via `render_template()`.
   - RESTful endpoints handle expense CRUD operations (e.g. `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`).

2. **Template Inheritance (`templates/`)**:
   - `base.html` serves as the master template containing shared HTML head tags, Google Fonts (*DM Serif Display*, *DM Sans*), navigation header, main content wrapper, and footer.
   - Child pages extend `base.html` using `{% extends "base.html" %}` and implement defined blocks:
     - `{% block title %}`
     - `{% block head %}`
     - `{% block content %}`
     - `{% block scripts %}`

3. **Database Layer (`database/db.py`)**:
   - Module providing database helpers:
     - `get_db()`: Returns a SQLite connection with `sqlite3.Row` row factory and foreign key enforcement enabled (`PRAGMA foreign_keys = ON;`).
     - `init_db()`: Initializes table schemas using `CREATE TABLE IF NOT EXISTS`.
     - `seed_db()`: Populates initial sample data for development.

4. **Styling & Assets (`static/`)**:
   - Vanilla CSS styling using CSS variables and modern flex/grid layouts.
   - External frontend frameworks (e.g., Bootstrap, TailwindCSS) are avoided to maintain lightweight, standard web compliance.
   - Assets are referenced dynamically in templates via Flask's `url_for('static', filename='...')`.

---

## 6. Coding Standards & Guidelines

- **Python**:
  - Adhere to PEP 8 standards for formatting and naming conventions.
  - Keep route handler logic cleanly organized and documented.
  - Ensure proper input validation and error handling across routes.

- **HTML & Jinja Templates**:
  - Use semantic HTML5 markup (`<nav>`, `<main>`, `<section>`, `<footer>`).
  - Use Flask's `url_for()` helper for all internal page navigation and asset references.

- **JavaScript**:
  - Write pure Vanilla JavaScript (ES6+). Avoid framework dependencies.
  - Attach event handlers programmatically (`addEventListener`) in JS files rather than inline HTML event attributes.
  - Clean up DOM interactions and media state (e.g. pause embedded iframe videos when closing modals).

- **Git Commit Conventions**:
  - Write clear, scoped commit messages (e.g., `landing: redesign hero section to match mockup`, `auth: implement user registration`).
