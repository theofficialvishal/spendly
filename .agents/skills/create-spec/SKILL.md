---
name: create-spec
description: Create a specification document and feature branch for the next Spendly roadmap feature.
argument-hint: "Step number and feature name (e.g. 2 registration)"
allowed-tools: Read, Write, Glob, Bash(git:*)
---

You are a senior software engineer responsible for preparing the next feature specification for the Spendly expense tracker.

Your goal is NOT to write implementation code.

Your only responsibility is to create a complete implementation specification that another AI or developer can safely implement.

Always follow every rule defined in GEMINI.md.

User input:

$ARGUMENTS

---

# Step 1 — Verify Working Directory

Run:

git status

If there are ANY:

- modified files
- staged files
- untracked files

STOP.

Tell the user:

"The working directory is not clean. Please commit or stash your changes before creating a new feature specification."

Do NOT continue.

---

# Step 2 — Parse User Arguments

Extract:

1. step_number
   - Zero-pad to two digits
   - Examples:
     2 → 02
     8 → 08
     11 → 11

2. feature_title
   Human readable Title Case

   Examples:

   Registration

   Login and Logout

3. feature_slug

Lowercase

kebab-case

Maximum 40 characters

Only:

a-z

0-9

-

Example:

login-logout

4. branch_name

feature/<feature_slug>

Example

feature/login

If anything cannot be confidently inferred,

STOP

Ask the user for clarification.

Do NOT guess.

---

# Step 3 — Verify Feature Understanding

Before doing anything else,

summarise your understanding of the requested feature in 3–5 concise bullet points.

If the request is ambiguous,

STOP.

Ask follow-up questions.

Do NOT continue until the request is clear.

---

# Step 4 — Ensure Branch Name is Unique

Run:

git branch

If the branch already exists,

append a numeric suffix.

Examples

feature/login

feature/login-01

feature/login-02

---

# Step 5 — Switch to Main

Run

git checkout main

git pull origin main

If pull fails,

STOP

Report the error.

---

# Step 6 — Create Feature Branch

Run

git checkout -b <branch_name>

---

# Step 7 — Research the Existing Project

Before writing anything,

read the following:

- GEMINI.md
- app.py
- database/db.py
- every spec inside .agents/specs/

Research the existing codebase carefully.

Every recommendation inside the spec MUST be supported by the existing project.

Never invent:

- routes

- tables

- schema

- filenames

- architecture

If information is missing,

explicitly write

"Not enough information."

Do NOT guess.

---

# Step 8 — Check for Duplicate Work

Compare the requested feature against:

- roadmap

- existing specs

If the feature already exists,

STOP.

Explain which specification already covers it.

Do NOT generate another spec.

Also verify inside GEMINI.md that the requested roadmap step has not already been completed.

If already completed,

STOP.

Warn the user.

---

# Step 9 — Generate the Specification

Generate the specification using EXACTLY the following structure.

---

# Spec: <Feature Title>

## Overview

One paragraph describing the purpose of the feature and why it exists at this stage of the roadmap.

---

## Feature Summary

3–5 bullet points describing the expected behaviour.

---

## Depends On

Previous roadmap steps required.

If none,

state:

None.

---

## Non Goals

Explicitly state what this feature will NOT implement.

---

## Acceptance Criteria

A measurable checklist describing what the finished feature must achieve.

---

## Routes

Use this table.

| Method | Route | Access | Purpose |

If no new routes:

Write:

No new routes.

---

## Database Changes

Split into:

### Existing Tables Affected

### New Tables

### Indexes

### Constraints

### Migration Notes

If nothing changes,

state:

No database changes.

---

## UI Changes

Include:

Navigation

Forms

Buttons

Validation

Flash Messages

Responsive Behaviour

If none,

state:

No UI changes.

---

## Templates

### Create

### Modify

Describe exactly what changes are needed.

---

## Files to Modify

List every existing file.

---

## Files to Create

List every new file.

---

## New Dependencies

List new pip packages.

Otherwise

No new dependencies.

---

## Risks

Potential implementation risks.

Examples

Database migration

Authentication

Performance

Compatibility

---

## Security Considerations

Always include:

Authentication

Authorization

Input Validation

CSRF

XSS Prevention

Parameterized SQL

Password Hashing

---

## Manual Test Plan

Describe manual testing scenarios including:

Happy Path

Validation Errors

Edge Cases

Authentication

Regression Checks

---

## Rules for Implementation

Always include:

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

A checklist where every item can be verified by running the application.

---

# Step 10 — Validate the Spec

Before saving,

verify:

✓ Every referenced file exists

✓ Route names are consistent

✓ No duplicated routes

✓ No duplicated templates

✓ Database changes match database/db.py

✓ Feature follows roadmap

✓ Spec does not contradict GEMINI.md

✓ No assumptions were made without evidence

If validation fails,

fix the specification before saving.

---

# Step 11 — Save the Spec

Save to:

.agents/specs/<step_number>-<feature_slug>.md

---

# Step 12 — Final Report

Print ONLY:

Branch: <branch_name>

Spec file: .agents/specs/<step_number>-<feature_slug>.md

Title: <feature_title>

Then tell the user:

Review the specification before proceeding.

Do not begin planning or implementation until the user explicitly approves the spec.
