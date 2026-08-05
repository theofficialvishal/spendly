# Spec: Profile Page Design

## Overview
This feature introduces a comprehensive personal financial profile dashboard for authenticated users at the `/profile` endpoint. It serves as a central hub where users can view their account identity (avatar initials, name, email, member join date), high-level spending summaries (total spent, transaction count, top spending category), recent transaction history, and a spending breakdown by category with dynamic progress indicators matching the Spendly design system mockup.

## Feature Summary
- Create/update route and view function for the `/profile` endpoint.
- Protect the route to ensure only logged-in users can access it (redirecting unauthenticated users to `/login`).
- Fetch the authenticated user's account details (name, email, created_at) from the database and compute avatar initials (e.g. "DU" for Demo User).
- Fetch and compute key user spending metrics: Total Spent (₹), Total Transactions count, and Top Category.
- Query recent transactions for the user (date, description, category, amount) formatted with category badges.
- Query category spending breakdown for the user with calculated percentage representation for visual progress bars.
- Render a responsive, modern dashboard interface matching the Spendly mockup layout.

## Depends On
03-login-and-logout

## Non Goals
- Implementing profile picture file uploads (initials-based SVG/CSS avatar used instead).
- Editing profile details or changing password (handled in separate settings steps).
- Exporting transaction history to CSV/PDF (handled in reporting step).

## Acceptance Criteria
- [ ] Navigating to `/profile` as an authenticated user displays the profile dashboard.
- [ ] Navigating to `/profile` as an unauthenticated user redirects to `/login` with an informational flash message.
- [ ] The Profile Hero card displays the user's avatar initials, full name, email, and formatted member join date (e.g. "Member since 15 Jan 2025").
- [ ] Displays 3 summary metric cards:
  - **TOTAL SPENT**: Formatted currency (e.g. ₹12,450.75).
  - **TRANSACTIONS**: Total count of expenses recorded.
  - **TOP CATEGORY**: Name of the highest spending category.
- [ ] Displays a **Recent Transactions** section with columns for Date, Description, Category (with colored pill badges), and Amount.
- [ ] Displays a **By Category** spending breakdown section showing category names, formatted amounts, and visual colored progress bars scaled to proportion.
- [ ] Layout is fully responsive: stacked 1-column layout on mobile (<768px) and multi-column grid layout on desktop.

## Routes
| Method | Route | Access | Purpose |
|--------|-------|--------|---------|
| GET | `/profile` | Authenticated | Display user profile identity, financial metrics summary, recent transactions, and category spending breakdown. |

## Database Changes
### Existing Tables Affected
- `users`: Queried for user identity (`id`, `name`, `email`, `created_at`).
- `expenses`: Queried for user spending stats (`amount`, `category`, `date`, `description`).

### New Tables
No database changes required.

### Indexes
No new indexes required.

## UI Changes
- **Header Greeting**: Display "Welcome back!" sub-header.
- **Profile Hero Card**: Avatar circle with user initials, large user name, muted email, and join date.
- **Stats Row**: 3-column metric cards for Total Spent, Transactions count, and Top Category.
- **Main Dashboard Section (2-Column Grid)**:
  - Left column (~65%): Recent Transactions table with category tags (Food, Transport, Bills, Health, Shopping, Entertainment, Other).
  - Right column (~35%): "By Category" spending breakdown list with custom-colored progress bars.

## Templates
### Modify
- `templates/profile.html`: Redesign into full profile financial dashboard.
- `templates/base.html`: Ensure navigation link to Profile is present and properly styled.

## Files to Modify
- `app.py`
- `static/css/style.css`
- `templates/profile.html`

## New Dependencies
No new dependencies.

## Risks
- **Empty State**: Ensure gracefully handled UI presentation if a user has 0 transactions (showing zero total spent, 0 transactions, "N/A" top category, and friendly empty states).

## Rules for Implementation
- Parameterized SQL queries only (no raw string interpolation).
- Use CSS variables from the Spendly theme palette.
- Responsive CSS Grid and Flexbox layout.
- Clean typography hierarchy (DM Serif Display for main headings/values, DM Sans for body/labels).

## Definition of Done
- [ ] `/profile` route updated to fetch user identity + expense aggregates + recent expenses + category breakdown.
- [ ] `profile.html` updated with hero card, 3 summary cards, recent transactions table, and category progress bars.
- [ ] `style.css` updated with profile layout grid, stat card, category tag, and progress bar styles.
- [ ] Manual test verifies layout matches mockup screenshot and handles edge cases (e.g. empty expense list).
