# Spec: Login and Logout

## Overview

This feature implements user authentication (login) and session termination (logout) for the Spendly expense tracking application. Following database setup (Step 1) and user registration (Step 2), login and logout functionality is essential to authenticate users against stored credentials, establish secure user sessions using Flask's `session`, customize the user interface based on authentication state, and allow users to securely terminate their active sessions.

---

## Feature Summary

- Render the login form on `GET /login` and process authentication on `POST /login`.
- Query user records via parameterized SQL and verify password credentials securely using `werkzeug.security.check_password_hash`.
- Store authenticated user information (`user_id`, `user_name`, `user_email`) in Flask `session` upon successful authentication and redirect to the profile page (`/profile`) with a success flash message.
- Implement `/logout` route to clear all Flask session keys (`session.clear()`) and redirect to the landing page with an informational flash message.
- Dynamically update navigation UI in `templates/base.html` to reflect whether a user is logged in or logged out.

---

## Depends On

- 01-database-setup
- 02-registration

---

## Non Goals

- Password reset or "Forgot Password" functionality via email verification tokens.
- "Remember Me" persistent cookie / token management.
- Multi-factor authentication (MFA / 2FA).
- Third-party social logins (e.g., OAuth via Google or GitHub).
- Server-side session store integration (e.g., Redis or database-backed sessions).

---

## Acceptance Criteria

- [ ] Navigating to `GET /login` renders the login form page.
- [ ] Submitting `POST /login` with valid registered email and correct password verifies `check_password_hash`, sets `session['user_id']`, `session['user_name']`, and `session['user_email']`, and redirects to `url_for('profile')` with a success flash message.
- [ ] Submitting `POST /login` with non-existent email or wrong password displays a generic error flash message ("Invalid email or password.") on the login page.
- [ ] Accessing `/logout` clears `session`, displays flash message ("You have been logged out successfully."), and redirects to `url_for('landing')`.
- [ ] `templates/base.html` header navigation conditionally renders "Sign out" link and user greeting when logged in, or "Sign in" and "Get started" CTA links when logged out.
- [ ] Logged-in users navigating to `/`, `/login`, or `/register` are automatically redirected to `url_for('profile')`.

---

## Routes

| Method | Route | Access | Purpose |
| --- | --- | --- | --- |
| GET | `/login` | Public (Anonymous only) | Render user login form view |
| POST | `/login` | Public (Anonymous only) | Authenticate user credentials and establish session |
| GET / POST | `/logout` | Authenticated | Terminate active user session and redirect to landing page |

---

## Database Changes

### Existing Tables Affected

None.

### New Tables

None.

### Indexes

None.

### Constraints

None.

### Migration Notes

No database changes.

---

## UI Changes

- **Navigation**: Update header navbar in `templates/base.html` to conditionally display user state. When `session.get('user_id')` exists, show user name/greeting and "Sign out" link; when logged out, show "Sign in" link and "Get started" button.
- **Forms**: `templates/login.html` form uses `method="POST"` and `action="{{ url_for('login') }}"` with input names `email` and `password`.
- **Buttons**: Sign in submit button triggers authentication; Sign out link triggers logout.
- **Validation**: HTML5 required attributes for client-side check; server-side check for non-empty credentials and valid match.
- **Flash Messages**: Render error/success notifications inside `.auth-card` in `templates/login.html` and globally inside `<main class="main-content">` in `templates/base.html`.
- **Responsive Behaviour**: Navbar user links collapse cleanly on mobile device viewports using existing responsive layout rules.

---

## Templates

### Create

None.

### Modify

- `templates/login.html`: Verify form action (`{{ url_for('login') }}`), method (`POST`), input field `name` attributes, and flash message alert container formatting.
- `templates/base.html`: Add conditional Jinja rendering in the navbar for logged-in (`session.get('user_id')`) vs logged-out states. Add global flash message container inside main content wrapper.

---

## Files to Modify

- `app.py`
- `templates/login.html`
- `templates/base.html`

---

## Files to Create

None.

---

## New Dependencies

No new dependencies.

---

## Risks

- **Session Security**: Session cookies could be tampered with if Flask `secret_key` is exposed or insecure.
- **User Enumeration**: Returning specific error messages (e.g. "Email does not exist") would allow attackers to enumerate valid email addresses. Using a uniform "Invalid email or password." error prevents enumeration.
- **Flash Message Visibility**: Global flash messages on landing page after logout or redirect must render cleanly without layout breakage.

---

## Security Considerations

- **Authentication**: Use `werkzeug.security.check_password_hash(user['password_hash'], password)` for secure constant-time password verification.
- **Authorization**: Session teardown (`session.clear()`) must purge all user-identifying session keys on logout.
- **Input Validation**: Normalize email inputs (`email.strip().lower()`); reject empty email or password fields.
- **CSRF**: Follow standard Flask form processing conventions.
- **XSS Prevention**: Rely on Jinja2 auto-escaping for dynamic output such as `{{ session.get('user_name') }}`.
- **Parameterized SQL**: Always query user records using parameterized SQL statements (`SELECT id, name, email, password_hash FROM users WHERE email = ?;`).
- **Password Hashing**: Plaintext passwords must never be stored, logged, or queried directly.

---

## Manual Test Plan

- **Happy Path**:
  1. Open app at `http://127.0.0.1:5001/login`.
  2. Enter credentials for demo user (`demo@spendly.com` / `demo123`).
  3. Click "Sign in" and verify redirect to `/profile` with success message "Welcome back, Demo User!".
  4. Verify top navbar displays "Demo User" and "Sign out".
  5. Click "Sign out" and verify redirect to `/` with message "You have been logged out successfully.".
  6. Verify top navbar displays "Sign in" and "Get started".

- **Validation Errors**:
  1. Try submitting empty login form — browser validation prevents submission.
  2. Enter `demo@spendly.com` with incorrect password `wrongpassword` — verify error banner "Invalid email or password.".
  3. Enter non-existent email `nobody@spendly.com` with password `password123` — verify generic error banner "Invalid email or password.".

- **Edge Cases**:
  1. Enter email with surrounding whitespace or uppercase letters (` DEMO@SPENDLY.COM `) — login succeeds.
  2. Directly visit `/`, `/login`, or `/register` while logged in — automatically redirected to `/profile`.
  3. Directly visit `/logout` when logged out — safely redirects to `/` or `/login` without application errors.

- **Authentication**:
  1. Inspect session handling to ensure `user_id`, `user_name`, and `user_email` are properly managed and cleared upon logout.

- **Regression Checks**:
  1. Test `/register`, `/terms`, `/privacy`, and landing page `/` to ensure no existing functionality is broken.

---

## Rules for Implementation

- No SQLAlchemy or ORMs
- Parameterized SQL queries only
- Passwords hashed using werkzeug.security
- Reuse existing helper functions whenever possible
- Never duplicate existing logic
- Keep routes thin
- Move business logic into reusable functions
- Use CSS variables
- Never hardcode colours
- Every template extends base.html
- Follow existing project structure
- Avoid unnecessary dependencies
- Preserve backward compatibility
- Do not break existing functionality

---

## Definition of Done

- [ ] Navigating to `GET /login` displays the login form template.
- [ ] Submitting `POST /login` with valid credentials authenticates user, sets `session` keys, and redirects to profile page (`/profile`) with success flash message.
- [ ] Submitting `POST /login` with invalid credentials displays generic error message without logging user in.
- [ ] Accessing `/logout` purges all `session` data and redirects to landing page with flash message.
- [ ] `templates/base.html` navbar updates dynamically based on session status.
- [ ] Logged-in users attempting to visit `/`, `/login`, or `/register` are redirected to profile page (`/profile`).
- [ ] Database query for user authentication uses parameterized SQL (`?`).
- [ ] Password verification uses `werkzeug.security.check_password_hash`.
- [ ] All manual test plan scenarios pass without errors.
