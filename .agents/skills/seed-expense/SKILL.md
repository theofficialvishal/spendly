---
name: seed-expenses
description: >-
  Use this skill when the user wants to seed the database
  with realistic dummy expenses for an existing user,
  generate sample expense records, or populate the
  expenses table for testing.
argument-hint: "<user_id> <count> <months>"
allowed-tools: Read, Bash(python3:*)
---

Read database/db.py to understand the expenses table
schema, the db connection pattern, and the database
file name.

User input: $ARGUMENTS

## Step 1 — Parse arguments

Extract from $ARGUMENTS:

- user_id — integer
- count — integer, number of expenses to create
- months — integer, how many past months to spread them across

If any argument is missing or not a valid integer, stop and say:

```
Usage: /seed-expenses <user_id> <count> <months>

Example:
/seed-expenses 1 50 6
```

## Step 2 — Verify user exists

Before generating anything, confirm the user_id exists
in the users table.

If not, stop and say:

```
No user found with id <user_id>.
```

## Step 3 — Generate and insert expenses

Write and run a Python script that:

1. Spreads expenses randomly across the past `<months>` months.
2. Uses these categories with realistic Indian descriptions and amounts (₹):

- Food: 50–800
- Transport: 20–500
- Bills: 200–3000
- Health: 100–2000
- Entertainment: 100–1500
- Shopping: 200–5000
- Other: 50–1000

3. Distributes categories roughly proportionally:

- Food → Most common
- Transport → Common
- Bills → Common
- Shopping → Moderate
- Other → Moderate
- Health → Less common
- Entertainment → Least common

4. Uses the database connection pattern from `db.py`.

Do **not** hardcode the database filename.

5. Uses parameterized SQL queries only.

Never use string formatting inside SQL statements.

6. Inserts all expenses inside a single transaction.

If any insert fails, roll back the entire transaction.

## Step 4 — Confirm

Print:

- Total expenses inserted
- Date range covered
- Sample of 5 inserted expense records
