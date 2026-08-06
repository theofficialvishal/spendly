---
name: test-feature
description: Generates pytest test cases from a feature specification and then runs them to validate the test suite using spendly-test-writer and spendly-test-runner.
---

# test-feature Skill

You are a test orchestrator. Your job is to take a feature specification, delegate the writing of test cases to the `spendly-test-writer` agent, and then delegate the execution of those tests to the `spendly-test-runner` agent.

User input:
$ARGUMENTS (This should contain the feature name or the path to the feature specification)

---

# Step 1 — Gather Feature Spec

Extract the feature spec or its path from `$ARGUMENTS`.
If none is provided, ask the user: 
"Which feature specification would you like to generate and run tests for?"

---

# Step 2 — Invoke Writer Subagent

Invoke the `spendly-test-writer` subagent.
Send it a message containing the feature spec and instruct it to write a comprehensive pytest test suite based strictly on the spec.
Wait for it to finish its task and confirm that the test files have been written and saved.

---

# Step 3 — Invoke Runner Subagent

Once the writer has finished, invoke the `spendly-test-runner` subagent.
Instruct it to run the pytest command to validate the newly written tests.
Wait for it to read the output and report the results back to you.

---

# Step 4 — Final Report

Present the test run summary from the runner to the user.
If tests passed, confirm that the feature's tests are fully ready.
If tests failed, provide the summary of failures and ask the user if they would like to investigate the application implementation or debug the test cases.
