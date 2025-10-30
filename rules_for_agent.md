# Gearbox User Docs — Rules for the UI Agent

## 1. Input
The agent always starts from an existing `.md` file written by the model from `structure.md`.

This file may contain the following markers:

- `TODO: ...`
- `VERIFY: ...`
- `SOURCE-CONFLICT: ...`
- `SCREENSHOT: ...`

The agent **does not invent** new content and **does not change** the overall structure of the file. The agent only confirms, corrects, and completes what can be verified in the actual Gearbox UI (fork / current app).

---

## 2. Main Goal
**Compare the model’s text with the real Gearbox UI and resolve everything that can be resolved automatically.**

Priority order:

1. Close `VERIFY:` — confirm that the described thing is actually present/doable in the UI.
2. Close `TODO:` — if it’s about a UI element, label, button, screen, or visible limit.
3. Replace `SCREENSHOT:` with a concrete path + exact screen/state.
4. Resolve `SOURCE-CONFLICT:` if the UI shows the current truth.

If something cannot be checked in the current UI build, the agent keeps the marker and writes why.

---

## 3. What the Agent Checks in the UI

1. **Names of sections and buttons.**  
   - If the text says `Click **Deposit**` but the UI says `Supply`, the agent changes it to `Supply`.
   - If the UI label changes per network, the agent writes the one actually shown and may add: `(may appear differently on other networks)`.

2. **Order of steps.**  
   - If the model wrote 4 steps, but in UI you must approve first and only then deposit, the agent adds the missing step and removes the old `TODO:`.
   - The agent does not change the meaning — only fixes the real flow.

3. **Presence of screen/section.**  
   - If the text says “check in **History**” but the UI calls it `Activity`, the agent renames it to `Activity`.

4. **Visible limits / minimums.**  
   - If the UI shows min/max, the agent inserts those real numbers and removes the `TODO:`.
   - If the limit is clearly dynamic (network / balance / role), the agent writes:  
     `NOTE (agent): limit is dynamic, value taken from UI at verification time.`

5. **Transaction statuses.**  
   - If the text says `status "Success"` but UI shows `Completed`, the agent changes it to `Completed`.

---

## 4. Working with Markers

### 4.1 `VERIFY: ...`
- If the fact is confirmed in UI → agent deletes the `VERIFY:` line and replaces it with normal prose.
- If it is only partially confirmed → agent rewrites to:  
  `VERIFY (partial): on <network> it appears as "<actual text>"`
- If it cannot be checked (screen not present / feature off) →  
  `VERIFY (failed): not available in current UI build.`

### 4.2 `TODO: ...`
- If it is about UI / button / label / link that is visible → agent fills it in and removes `TODO:`.
- If it is about an external or non-UI thing (official deployments list, external policy, price source) → agent keeps `TODO:` and adds a short reason:  
  `TODO: link to official deployments list (not in UI, requires docs maintainers).`

### 4.3 `SCREENSHOT: ...`
- The agent does **not** generate images. The agent:
  1. Opens the corresponding screen.
  2. Notes the exact name/state of that screen.
  3. Replaces the line with a concrete path + description, e.g.:  
     `SCREENSHOT: /images/earn-deposit/deposit-form-opt-mainnet.png — form before wallet confirm, shows amount, APR, fee.`
- If the screen is not in this UI build →  
  `SCREENSHOT: SKIP — screen not present in current UI build.`

### 4.4 `SOURCE-CONFLICT: ...`
- The agent opens the UI and checks **how it is actually shown right now**.
- If the UI gives a single answer → the agent rewrites the paragraph to the correct one and removes `SOURCE-CONFLICT:`.
- If the UI does not fully settle it (depends on network / feature flag) → the agent keeps both but adds:  
  `NOTE (agent): both variants exist; current UI (<date>) shows: "<actual variant>".`

---

## 5. Things the Agent **Must Not** Do

- Must not rewrite the tone — it was set by the model.
- Must not simplify or “rephrase for fun”.
- Must not add new sections/headings that are not in the model file.
- Must not insert real contract addresses if they are not visible or not linked from the official list.
- Must not introduce advanced topics (adapters, feeds, permissionless) if the model did not.

---

## 7. Behavior When the Element Is Missing

If the agent cannot find in the UI what the model described:

- The agent **does not delete** the model’s text.
- The agent adds a line right after that paragraph:

  `NOTE (agent): element not found in current UI build, needs product check.`

This makes it clear that it is a **UI/model mismatch**, not a model mistake.

---

## 8. Output

The final output is the **same `.md` file**, but:

- with most `TODO:` / `VERIFY:` resolved (when UI allowed it),
- with real UI names for sections and buttons,
- with `SCREENSHOT:` lines pointing to real paths/state,
- with conflicts either removed (if UI decided) or annotated.

This file can be passed directly to human review/publishing.