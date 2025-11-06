# Gearbox User Docs — Model Writing Rules (v2)

> IMPORTANT — Style Anchor: Use the first three chapters of `user_docs_model` as the template for tone, structure, and formatting. Mirror their smooth prose, “Step X — …” guide style, and strict marker usage.
> Reference files: `1_what-is-gearbox.md`, `2_getting-started.md`, `3_earn-lend.md`.

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
- You may use items from `gearbox-news/` for user-level explanations; time-sensitive numbers from news must be accompanied by a `VERIFY:` marker.

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
7. Use standardized terminology consistently: **Health Factor**, **Credit Account**, **Diesel Tokens**, **Permissionless**.

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
Only the markers defined above are allowed. Do not invent alternatives (e.g., do not use `SUPPORT:`).

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
- **Terms**: Use Health Factor, Credit Account, Diesel Tokens, Permissionless exactly as written.
- **Flow & readability**: write smoothly and human-like. Avoid choppy, staccato, list-heavy output. Prefer short paragraphs with natural transitions (e.g., “Then…”, “Next…”, “Now…”) and vary sentence length. Use bullet lists when they genuinely improve scannability (steps, options, checklists), not as the default for all content.

### Flow & readability — Practical guide

- Purpose-first intros: start each section with 1–2 sentences that explain the purpose (“What the user will achieve and why it matters”).
- Paragraph rhythm: aim for 2–5 sentences per paragraph; mix short and medium sentences (approx. 7–25 words) to avoid robotic cadence.
- Natural transitions: connect actions and outcomes with signposts:
  - Then, Next, Now, After this, As a result, Because, However, Instead, In most cases, For example.
- Lists with intent: use lists for true steps, options, or checklists only. Keep lists short (≤5 bullets). Avoid nested lists; convert long lists into short paragraphs.
- Action → Why → Outcome pattern for steps:
  1. Action: what to click/open/select.
  2. Why: what this accomplishes or why it’s needed.
  3. Outcome: what appears or changes in the UI.
  4. Marker: add `TODO:`/`VERIFY:` if any label/number needs confirmation.

Example (before → after):

Choppy:

```
1) Go to Pools. 2) Pick pool. 3) Click Supply. 4) Confirm.
```

Smooth:

```
Open the Pools section and choose the pool that fits your goal. Next, enter the amount you want to supply and review the preview with your balance and current APY. When you’re ready, click Supply and confirm in your wallet — you’ll receive Diesel Tokens that track your share of the pool.
VERIFY: confirm exact button labels in the current UI
```

- Active voice and second person: prefer “Open…”, “You will see…”, “Click…” over passive or impersonal forms.
- Avoid filler and hedging: remove “basically”, “just”, “obviously”, and meta-comments about the docs.
- Minimize parentheses: if extra detail is important, integrate it into the sentence or split into a clear follow-up sentence.

### Guides — Step formatting

- In how-to guides, enumerated steps are encouraged — but not as one-line staccato commands. Use sentence-based steps with context.
- Format: `Step 1 — <action & context>` on its own line, followed by 1–2 sentences that cover Why and Outcome (as needed). Keep each step compact but complete.
- Never use the choppy pattern (e.g., `1) Go to X. 2) Click Y. 3) Confirm.`). It is forbidden.
- Outside of guides, enumerate only when necessary (true alternatives, checklists). Prefer prose when lists do not add clarity.

Example (good):

```
Step 1 — Open the Pools section and choose a pool that fits your goal.
This helps you see current APY and utilization for that asset.

Step 2 — Enter the amount you want to supply and review the preview.
You’ll see your available balance and expected APY before confirming.

Step 3 — Click Supply and confirm in your wallet.
You receive Diesel Tokens that represent your share of the pool.
VERIFY: confirm exact button labels in the current UI
```

### Editorial checklist (run before finalizing)

- Each section starts with a one-sentence purpose.
- No more than two list blocks in a row; paragraphs connect steps with transitions.
- Screenshots described with `SCREENSHOT:` (what must be visible).
- All uncertain labels/values have `TODO:`/`VERIFY:` markers on their own lines.
- No “official” lists of networks/addresses/limits/rates; instead use the markers policy.
- Terminology is consistent: Health Factor, Credit Account, Diesel Tokens, Permissionless.

---

## 6. What the Model Must NOT Do

- Must **not** insert made-up contract addresses, APYs, caps, or network names.
- Must **not** change the logical order or layout that is already implied by `structure.md`.
- Must **not** link to random external sites — only to our dumped docs/blog/dev materials.
- Must **not** replace `SCREENSHOT:` with any image markup — leave the placeholder.
- Must **not** enumerate authoritative lists (networks, contract addresses, quantitative limits, rates) inside user pages. Instead, add markers as described below.

---

## 7. What the Model Should Do Instead

- If the original text has a table / formula / example — **preserve** it in Markdown.
- If the text mentions a deployment / contract but the URL is not present — write:  
  `TODO: add link to official deployments list`
- If steps are clearly UI-driven but the exact labels are not in the dump — write a normal human step and add `TODO:` right next to the uncertain part.
- If the page is obviously related to another (`deposit` ↔ `withdraw`, `open account` ↔ `close account`) — you may add a tiny “See also …” line; if the exact target file is unknown, mark it:  
  `TODO: add link to withdraw page`
- For networks/addresses/limits/rates, avoid listing values. Use:
  - `TODO: add link to official deployments list`
  - `VERIFY: confirm supported networks in current app`
  - `VERIFY:` for time-sensitive numbers (e.g., max leverage, APY ranges, pool utilization, rewards, years live, audits count).

---

## 8. Conflict Handling

When two dumped sources contradict each other, the model must **show it**, not resolve it:

```markdown
SOURCE-CONFLICT: gearbox-docs says "Health Factor is visible on the main account screen".
SOURCE-CONFLICT: doc-gitbook says "Health Factor is inside account details".
TODO: agent to confirm actual location in current UI.
```

Also use conflict markers for legacy vs permissionless wording where applicable, for example:

```markdown
SOURCE-CONFLICT: Legacy quota/gauge-based rates vs Permissionless curator-set fixed premiums and bootstrapping rewards.
```