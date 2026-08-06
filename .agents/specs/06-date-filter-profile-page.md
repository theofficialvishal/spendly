---
title: Date Filter For Profile Page
---

# Spec: Date Filter For Profile Page

## Overview

The purpose of this feature is to allow users to filter their dashboard metrics, recent transactions, and category breakdown by a specific date range or quick preset filters. As users accumulate more expenses over time, viewing all-time data becomes less actionable. Adding start/end date inputs along with quick preset buttons ("All Time", "This Month", "Last 3 Months", "Last 6 Months") empowers users to track their spending for specific periods seamlessly.

---

## Feature Summary

- Add a date range filter form (start date and end date) to the profile dashboard.
- Add 4 quick preset buttons ("All Time", "This Month", "Last 3 Months", "Last 6 Months") to quickly select common date ranges.
- Update the `/profile` route to accept optional `start_date`, `end_date`, and `preset` query parameters.
- Filter all aggregated metrics (total spent, transactions, top category), recent transactions list, and category breakdown by the selected date range.
- Retain the selected date range in the form inputs after submission and highlight active preset button.
- If no dates or presets are provided, default to showing all-time data.

---

## Depends On

- 04 Profile Page Design (The dashboard layout must exist).

---

## Non Goals

- We will not implement date validation via JavaScript (HTML5 date input validation and backend validation are sufficient).
- We will not add pagination to the recent transactions list.

---

## Acceptance Criteria

- [x] A form with `start_date` and `end_date` inputs and a "Filter" button exists on the profile page.
- [x] 4 quick preset buttons ("All Time", "This Month", "Last 3 Months", "Last 6 Months") exist and automatically apply appropriate date filters when clicked.
- [x] Submitting the form or clicking a preset updates the URL query string (e.g., `?preset=this_month` or `?start_date=2026-08-01&end_date=2026-08-31`).
- [x] The Total Spent, Transactions count, and Top Category stats respect the date filters.
- [x] The Recent Transactions table only shows expenses within the selected dates.
- [x] The Category Breakdown progress bars only calculate totals based on the filtered expenses.
- [x] The selected dates remain visible in the form inputs after page reloads, and active preset button is highlighted.
- [x] If only one date is provided (e.g., start date), the filter should apply an open-ended range.
- [x] Clearing the inputs or clicking "All Time" resets the view to all-time data.

---

## Routes

| Method | Route | Access | Purpose |
|--------|-------|--------|---------|
| GET    | `/profile` | Private | Display the profile dashboard, applying optional date filters or presets via query string. |

---

## Database Changes

### Existing Tables Affected

No database schema changes. Query parameters will be dynamically injected into existing SELECT statements.

### New Tables

No new tables.

### Indexes

No new indexes.

### Constraints

No constraints.

### Migration Notes

No database changes.

---

## UI Changes

- **Forms:** Add a new `<form>` inside a `.filter-card` above `.stats-grid` containing quick filter presets and two `<input type="date">` fields with a submit button.
- **Buttons:** Add "All Time", "This Month", "Last 3 Months", and "Last 6 Months" preset links styled as toggle buttons, alongside "Filter" and "Clear Filter" buttons.
- **Responsive Behaviour:** Ensure the date filter form and preset buttons wrap cleanly on mobile devices.
- **Flash Messages:** Add an error message if `start_date` is strictly after `end_date`.

---

## Templates

### Create

No new templates.

### Modify

- `templates/profile.html`: 
  - Insert a filter card containing preset quick filter links and date filter form above `<div class="stats-grid">`.
  - The form should use `method="GET"`.
  - Populate the `value` attributes of date inputs and highlight active preset button based on context passed from backend.

---

## Files to Modify

- `app.py`
- `templates/profile.html`
- `static/css/style.css`
- `tests/test_profile.py`

---

## Files to Create

No new files.

---

## New Dependencies

No new dependencies.

---

## Risks

- **SQL Injection:** We are dynamically building SQL queries based on user input. We must strictly use parameterized queries.
- **Data Types:** SQLite stores dates as strings in ISO-8601 format (`YYYY-MM-DD`). We must ensure the input dates match this format before querying.

---

## Security Considerations

- **Authentication:** Only authenticated users can view the profile page and apply filters.
- **Authorization:** Ensure that all queries continue to filter strictly by `user_id = ?`.
- **Input Validation:** Validate that `start_date` and `end_date` are valid date strings before executing queries.
- **CSRF:** Not required for GET requests.
- **XSS Prevention:** Date strings passed to the template must be safely rendered.
- **Parameterized SQL:** All modified SQL queries must continue to use `?` placeholders for both `user_id` and date boundaries.
- **Password Hashing:** N/A.

---

## Manual Test Plan

- **Happy Path:** Select a start/end date or click a quick preset button ("This Month", "Last 3 Months", "Last 6 Months"). Verify stats and transactions update.
- **Validation Errors:** Enter a start date later than the end date. Verify an error is flashed and all-time data is shown.
- **Preset Checks:** Verify clicking "All Time" clears filters.
- **Authentication:** Log out and attempt to access `/profile?preset=this_month`. Verify redirection to login.
- **Regression Checks:** Ensure user identity info remains intact.

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

- [x] Date filter form and quick preset buttons are fully styled and responsive on the profile page.
- [x] Backend extracts `start_date`, `end_date`, and `preset` from `request.args`.
- [x] SQL queries for metrics, recent transactions, and category breakdowns apply date filters when provided.
- [x] Form retains user input after submission and active preset button is highlighted.
- [x] Invalid date ranges gracefully fail and show a flash message.
- [x] All test cases pass cleanly.
