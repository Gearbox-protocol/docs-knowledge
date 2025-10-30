# Gearbox User Docs — Model Writing Rules (v2)

> Goal: the model generates full, readable, user-level Markdown pages based on the existing dumped materials, **without** browsing the UI and **without** inventing missing data. All unknown or UI-dependent parts must be explicitly marked for the agent.

---

## 1. Sources

- Use **only** the materials we already dumped:
  - `dev-docs/`
  - `doc-gitbook/`
  - `gearbox-docs/`
  - `gearbox-news/`
- Do **not** invent buttons, screens, limits, or features that are not present in these sources.
- If two sources say different things, keep **both** and mark it as a conflict.

---

## 2. Structure Compliance

- The model writes **one `.md` file per page** from `structure.md`.
- The **file name must match** the page name from `structure.md` (same wording, English, kebab-case if needed).
- The model **must not** impose its own inner page structure — pages can be different (some with tables, some with formulas, some just text), because this is decided in `structure.md` or in the original docs.

---

## 3. What the Model Must Do

1. Rewrite the content from the existing docs into **clear, user-friendly English**, in a style similar to product guides.
2. Add short connective explanations (“why this step”, “what the user will see”) **only if** they follow from the docs.
3. Where UI / exact label / network / explorer check is needed — leave a marker.
4. Where sources disagree — leave both statements and mark the conflict.
5. Where a screenshot is required — leave a placeholder line.
6. Leave small, inline, practical notes where it helps the user, **not** giant warning blocks.

---

## 4. Markers (must use)

Use **exactly** these markers — no other ad-hoc formats:

- `TODO: …` — something is missing in the current materials, needs to be filled later.  
  Example:  
  `TODO: add exact button label from current UI`

- `VERIFY: …` — a fact that must be confirmed in the live app or in the block explorer.  
  Example:  
  `VERIFY: transaction appears in History with status "Success"`

- `SOURCE-CONFLICT: …` — two versions in the sources, the agent/human must decide which to keep.  
  Example:  
  `SOURCE-CONFLICT: doc-gitbook says this screen is in "Account"; gearbox-docs says it is in "Dashboard".`

- `SCREENSHOT: …` — a screenshot must be taken here; describe what must be visible.  
  Example:  
  `SCREENSHOT: Deposit form showing amount, APR, and Confirm button`

Markers must be on their **own line** so the agent can regex-scan them.

---

## 5. Style

- **Audience**: end users (lenders / borrowers / traders), **not** curators, **not** smart-contract devs.
- **Tone**: calm, confident, helpful, similar to Aave user docs — short sentences, active voice (“Open…”, “Click…”, “You can…”).
- **Perspective**: talk to the user, not about the protocol. Prefer “you will see”, “you can deposit”, “you can close”.
- **Explaining but not low-level**: it is OK to say “price changes can reduce your health factor”, but **not** “the adapter pulls from X and pushes to Y”.
- **Warnings stay inline**:  
  “If the market moves against you, your Health Factor can fall, so keep a buffer.”  
  (No giant page-wide warning panels.)
- **No placeholders like `...`, `TBD`, `XXX`** — always use explicit `TODO:` / `VERIFY:` / `SCREENSHOT:`.

---

## 6. What the Model Must NOT Do

- Must **not** insert made-up contract addresses, APYs, caps, or network names.
- Must **not** change the logical order or layout that is already implied by `structure.md`.
- Must **not** link to random external sites — only to our dumped docs/blog/dev materials.
- Must **not** replace `SCREENSHOT:` with any image markup — leave the placeholder.

---

## 7. What the Model Should Do Instead

- If the original text has a table / formula / example — **preserve** it in Markdown.
- If the text mentions a deployment / contract but the URL is not present — write:  
  `TODO: add link to official deployments list`
- If steps are clearly UI-driven but the exact labels are not in the dump — write a normal human step and add `TODO:` right next to the uncertain part.
- If the page is obviously related to another (`deposit` ↔ `withdraw`, `open account` ↔ `close account`) — you may add a tiny “See also …” line; if the exact target file is unknown, mark it:  
  `TODO: add link to withdraw page`

---

## 8. Conflict Handling

When two dumped sources contradict each other, the model must **show it**, not resolve it:

```markdown
SOURCE-CONFLICT: gearbox-docs says "Health Factor is visible on the main account screen".
SOURCE-CONFLICT: doc-gitbook says "Health Factor is inside account details".
TODO: agent to confirm actual location in current UI.