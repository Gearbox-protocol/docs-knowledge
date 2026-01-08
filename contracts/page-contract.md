# PAGE CONTRACT
## Binding Specification for a Documentation Page

This Page Contract defines the **complete and exclusive scope** of a single documentation page.

The model must treat this contract as **binding**:
- Concepts not listed below must not be introduced
- Topics listed under Anti-Scope must not be discussed
- Reader navigation must be explicitly resolved via Outbound Links

---

## 1. Objective

**Decision Enabled:**  
> What concrete understanding or decision must the reader be able to make after reading this page?

Rules:
- One sentence
- No narrative
- No background

---

## 2. Key Concepts

The page must cover **only** the following mental models:

- Concept 1  
- Concept 2  

Rules:
- Concepts may be conceptual or formal, depending on what best serves the Objective
- Formal elements (formulas, parameters, code snippets) are permitted **when they materially improve understanding**
- If such elements appear in the provided documentation snapshot, explicitly evaluate:
  - whether they are essential for this page’s Objective
  - or whether they should be removed and resolved via an outbound reference

---

## 3. Anti-Scope

The page must **explicitly not** cover:

- Topic A  
- Topic B  

Rules:
- Anti-Scope overrides all other instructions
- Forbidden topics must not appear even briefly
- Redirection via links is allowed; explanation is not

---

## 4. Outbound Links (Navigational Obligations)

After reading this page, the reader may reasonably ask follow-up questions.

Each question must be resolved via an explicit reference:

- **Question:** Where is X defined or configured?  
  → `some-other-page.md`

- **Question:** How is Y enforced?  
  → `another-page.md`

Rules:
- Links must resolve **questions**, not list components
- No dangling questions are allowed
- If this page is a leaf node, state this explicitly

---

## 5. Execution Constraints

- The page must be **cognitively self-contained**
- The page must not assume prior reading beyond the sitemap
- The page must conform to all System Instructions and Project Invariants


