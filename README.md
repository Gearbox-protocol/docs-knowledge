# Gearbox Docs Workspace

This repository is the working space for the new version of Gearbox user documentation.

## What’s inside

- `structure.md` — the approved two-level structure of user docs (what we write and in what order).
- `rules_for_model.md` — rules for the model that works on top of existing docs. It must use the dumped materials (mainly `dev_docs` and `doc_gitbook`) and leave markers: `TODO:`, `VERIFY:`, `SOURCE-CONFLICT:`, `SCREENSHOT:`.
- `rules_for_agent.md` — rules for the UI agent: how to walk the forked frontend, how to resolve markers, what to update, and what to leave untouched.
- `user_docs_model.md` — user docs produced by the model from existing data (drafts with markers).
- `user_docs_agent.md` — user docs after the agent pass (markers resolved where possible).
- other files — legacy/old docs used as reference.

## UI agent connection

The agent is expected to work against the current draft frontend:

- App: `http://draft.client-v3.pages.dev/?dev-mode=false`
- Related change: `613c722 - feat: mock connection`

The agent should use this build to confirm button labels, screen names, and step order.

## How to work with it

1. Read `structure.md` first and create a page **with exactly the same name**.
2. The model writes a `.md` page and leaves all unknown/UI-dependent parts as markers.
3. The agent goes through the actual frontend above, resolves markers, and fills in real button/screen names.
4. After that the file can go to human review and publication.
