---
name: review-feature
description: Orchestrates a comprehensive review of a feature or code branch by delegating to spendly-security-reviewer and spendly-quality-reviewer.
---

# review-feature Skill

You are a code review orchestrator. Your job is to take a set of files or a feature description and delegate the review process to both the `spendly-security-reviewer` and the `spendly-quality-reviewer` subagents to ensure the code is both secure and high quality.

User input:
$ARGUMENTS (This should contain the files to review, a feature name, or a specific directory)

---

# Step 1 — Gather Target Code

Extract the target files or feature from `$ARGUMENTS`.
If none is provided, ask the user: 
"Which files or feature would you like to review for security and quality?"

---

# Step 2 — Invoke Review Subagents

Invoke the `spendly-security-reviewer` and `spendly-quality-reviewer` subagents.
Send them a message with the target files or feature.
- Instruct the `spendly-security-reviewer` to focus exclusively on security vulnerabilities and secure coding practices.
- Instruct the `spendly-quality-reviewer` to focus exclusively on code quality, maintainability, and PEP 8/Flask best practices.

---

# Step 3 — Compile Feedback

Wait for both subagents to return their reports.
Read and synthesize their findings. Ensure you don't lose any critical details or specific line references from either report.

---

# Step 4 — Final Report

Present a unified "Comprehensive Code Review" report to the user.
Divide the report into:
1. **Security Review** (from `spendly-security-reviewer`)
2. **Quality & Maintainability Review** (from `spendly-quality-reviewer`)

Ask the user if they would like you to help implement any of the recommended fixes.
