---
name: create-subagent
description: Create a new custom subagent definition and save it to .agents/agents/<name>/agent.md.
argument-hint: "Agent name (e.g. code-reviewer)"
allowed-tools: Read, Write, Glob, Bash(git:*)
---

You are responsible for creating a new custom subagent definition for this project.

Your only responsibility is to gather the required information from the user, generate a correct `agent.md` file, and save it to the correct location.

Do NOT write any implementation code.

Do NOT create the agent unless all required information has been confirmed by the user.

User input:

$ARGUMENTS

---

# Step 1 — Parse Agent Name

Extract the agent name from $ARGUMENTS.

Convert it to a slug:

- Lowercase
- kebab-case
- Maximum 40 characters
- Only: a-z, 0-9, -

Example:

"Code Reviewer" → code-reviewer

If no name was provided in $ARGUMENTS,

STOP.

Ask the user for the agent name.

Do NOT guess.

---

# Step 2 — Check for Existing Agent

Run:

Glob .agents/agents/<agent_slug>/agent.md

If a file already exists at this path,

STOP.

Ask the user:

"An agent named '<agent_slug>' already exists. Overwrite it, or choose a different name?"

Do NOT overwrite without explicit confirmation.

---

# Step 3 — Gather Agent Purpose

Ask the user to describe:

1. What this agent should do (its responsibility).
2. When it should be used (the trigger conditions — what kind of request or situation should cause this agent to be invoked).

If the user already provided this in $ARGUMENTS or earlier in the conversation, use it.

If the description is vague, generic, or only covers one of the two parts (what it does, OR when to use it, but not both),

STOP.

Ask a follow-up question to fill the gap.

Do NOT invent responsibilities or trigger conditions the user did not describe.

A good description reads like this pattern:

"Use this agent when <trigger condition>. It <does what>."

Example:

"Use this agent when the user asks for a review of recently written code. It checks for bugs, security issues, and violations of project conventions, and reports findings without modifying files."

---

# Step 4 — Select Tool Access

Present these options to the user and ask them to choose ONE (or an explicit custom combination):

1. **All tools** — full access, no restrictions.
2. **Read-only tools** — Read, Glob, Grep. Use for agents that only inspect/analyze and must never modify anything.
3. **Edit tools** — Read, Write, Edit, Glob, Grep. Use for agents that read and modify files but should not run commands.
4. **Execution tools** — Read, Glob, Grep, Bash. Use for agents that need to run commands, tests, or scripts.
5. **MCP tools** — any connected MCP server tools relevant to this agent's job (ask the user which ones, if not obvious).
6. **Other tools** — a custom, explicit list the user specifies.

If the user has not specified a choice,

STOP.

Ask them to pick one.

Do NOT default to "All tools" without the user explicitly choosing it — an agent should get the minimum access it needs to do its job.

If the chosen tool category conflicts with the agent's stated purpose (e.g. a "read-only reviewer" that asks for Bash/Execution tools), point out the mismatch and confirm with the user before continuing.

---

# Step 5 — Select Model

Ask the user which model this subagent should run on.

If the user has not specified one,

STOP.

Ask them to choose, and briefly note the general tradeoff:

- Heavier/reasoning models → better for agents that judge, review, plan, or make architectural decisions.
- Lighter/faster models → better for agents that do repetitive, well-defined, mechanical work.

Do NOT pick a model on the user's behalf.

---

# Step 6 — Confirm Summary Before Generating

Before writing anything, summarise back to the user in 3–5 bullet points:

- Agent name
- What it does / when it's used
- Tools selected
- Model selected

Ask for explicit confirmation.

Do NOT generate the file until the user confirms.

---

# Step 7 — Generate the Agent File

Generate the file using EXACTLY the following structure:

```
---
name: <agent_slug>
description: <one to two sentence description combining "when to use" and "what it does">
tools: <resolved tool list from Step 4>
model: <model selected in Step 5>
---

# Role

<One paragraph defining the agent's role and area of responsibility, derived from the user's description in Step 3.>

# When To Use This Agent

<Restate the trigger conditions clearly, so the orchestrating agent/system can decide when to invoke this subagent.>

# Responsibilities

<3–6 bullet points of concrete responsibilities, derived only from what the user described. Do not invent responsibilities.>

# Out of Scope

<Explicitly state what this agent should NOT do, especially anything that could be confused with its responsibilities. If the tool access is restricted (e.g. read-only), state that it must never attempt actions outside that access.>

# Output Expectations

<Describe the expected shape of this agent's output — e.g. a report, a list of findings, modified files, a plan — based on its purpose.>
```

---

# Step 8 — Validate Before Saving

Verify:

✓ Agent name is a valid slug

✓ Description mentions both "when to use" and "what it does"

✓ Tools list matches exactly what the user selected in Step 4

✓ Model matches exactly what the user selected in Step 5

✓ Responsibilities do not include anything the user did not describe

✓ Out of Scope section is consistent with the selected tool access

If validation fails,

fix the file before saving.

---

# Step 9 — Save the Agent

Save to:

.agents/agents/<agent_slug>/agent.md

Rules:

- Create the `.agents/agents/<agent_slug>/` directory if it does not already exist.
- Never save the agent file anywhere else.
- Never choose another filename — it must be `agent.md`.
- If the file cannot be saved to the required location, STOP and report the error.

---

# Step 10 — Final Report

Print ONLY:

Agent name: <agent_slug>

Agent file: .agents/agents/<agent_slug>/agent.md

Tools: <resolved tool list>

Model: <selected model>

Then tell the user:

Review the agent definition before relying on it. You can now invoke this subagent from other Skills or workflows by referencing '<agent_slug>'.
