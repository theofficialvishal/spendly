---
name: finish-feature
description: Commit and push the completed feature branch.
argument-hint: "Commit message (e.g. add login and logout functionality)"
allowed-tools: Bash(git:*)
---

You are responsible for safely committing and pushing the completed feature.

User input:

$ARGUMENTS

---

# Step 1 — Verify Current Branch

Run:

git branch --show-current

If the current branch is:

main

master

STOP.

Tell the user:

Never commit feature work directly to the main branch.

---

# Step 2 — Check Working Tree

Run:

git status

If there are NO modified, staged or untracked files,

STOP.

Tell the user:

There are no changes to commit.

---

# Step 3 — Stage Files

Run:

git add .

---

# Step 4 — Commit Changes

Use the user supplied message.

Run:

git commit -m "$ARGUMENTS"

If no commit message was supplied,

STOP

Ask the user for one.

---

# Step 5 — Push Branch

Determine the current branch.

Run:

git push origin <current_branch>

---

# Step 6 — Report

Print:

Current branch: <current_branch>

Commit message: <commit_message>

Status: Successfully pushed to origin.

Do not perform any merge.

Do not create pull requests.

Do not switch branches.

The feature branch is now ready for review.
