---
name: create-infographic
description: Convert any Markdown file (agent configs, specs, plans, README docs) into a single-file HTML infographic page for quick visual understanding.
argument-hint: "Path to the .md file (e.g. .agents/agents/spendly-test-writer/agent.md)"
allowed-tools: Read, Write, Glob
---

You are a technical information designer. Your job is to convert a given Markdown file into a single-file HTML infographic page that lets the user understand it at a glance, without reading the raw document.

You are NOT summarising in prose. You are designing a visual page.

User input:

$ARGUMENTS

---

# Step 1 — Locate the Source File

Extract the file path from $ARGUMENTS.

Run:

Glob <path>

If the file does not exist,

STOP.

Tell the user the path could not be found and ask them to confirm the correct path.

Do NOT guess a path.

---

# Step 2 — Read and Extract Structure

Read the full file.

Identify, only from what is actually present in the document:

1. **Identity** — a title/name and a one-sentence purpose statement (from frontmatter `name`/`description`, or the first heading + intro paragraph).
2. **Meta facts** — any config-like fields worth showing as small tags/badges (e.g. `tools`, `model`, `version`, `status`, `branch`).
3. **Sequence** — any real ordered process (numbered steps, a pipeline, a lifecycle). Only treat something as a sequence if order genuinely matters.
4. **Capability lists** — grouped bullet lists (responsibilities, features, checks, requirements, acceptance criteria).
5. **Duality** — any explicit contrast the doc draws (will do / won't do, in scope / out of scope, pros / cons, before / after).
6. **Leftover content** — anything that doesn't fit the above. Give it its own simple block rather than forcing it into one of the sections above.

If a section type (sequence, duality, etc.) is not present in the source document, do NOT invent one just to fill out a template — omit that section entirely.

If the file is too sparse to produce a meaningful infographic (e.g. only a title, no real content),

STOP.

Tell the user the file doesn't have enough structure for a useful infographic, and ask if they want to proceed anyway with a minimal version.

---

# Step 3 — Design Pass (do this before writing any code)

Pick a deliberate, small color system (4–6 named hex values) and a deliberate type pairing (a display face + a body face, used with restraint) — grounded in the actual subject of this specific document.

Do NOT default to:

- Cream background + terracotta accent
- Near-black background + single neon accent, with no other reasoning
- Generic dashboard-with-icons look

Pick ONE small signature visual detail that reflects what makes *this specific document* distinctive — not a generic icon. Keep everything else on the page restrained around it.

If there's a "will do / won't do" or similar contrast, give the two sides clearly distinct colors (one affirming, one restrictive) so the eye separates them instantly.

If there's a real sequence, number it. Otherwise, do not add numbered markers anywhere.

---

# Step 4 — Build the HTML

Output a single self-contained HTML file that:

- Uses inline `<style>` CSS, no external dependencies except web fonts.
- Is responsive down to mobile width.
- Uses real semantic structure (headings, lists) so it stays readable even if styling fails.
- Has visible keyboard focus states if there's any interactivity.
- Fits on one scrollable page — this is a glance-able summary, not a long-form document.
- Uses short labels and short phrases derived from the source — do not copy long paragraphs verbatim.

---

# Step 5 — Check for Existing Output

Determine the output slug from the source file's identity (Step 2.1), converted to kebab-case.

Run:

Glob .agents/infographics/<slug>.html

If a file already exists at this path,

STOP.

Ask the user:

"An infographic for '<slug>' already exists. Overwrite it?"

Do NOT overwrite without explicit confirmation.

---

# Step 6 — Save

Save to:

.agents/infographics/<slug>.html

Rules:

- Create the `.agents/infographics/` directory if it does not already exist.
- Never save anywhere else.
- If the file cannot be saved to the required location, STOP and report the error.

---

# Step 7 — Final Report

Print ONLY:

Source: <original file path>

Infographic: .agents/infographics/<slug>.html

Then tell the user:

Open the file in a browser to view it. If you need it as an image (for sharing in places that don't render HTML), take a screenshot of it in the browser.
