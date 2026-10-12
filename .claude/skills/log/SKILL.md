---
name: log
description: Write or revise a design-decision log in docs/log/ — when the user says "로그 써줘", "오늘 결정 정리해줘", "설계 결정 남겨", or after a decision is made and its rationale must be recorded. Follows the docs/log/FORMAT.md convention, registers the log in the index, and back-annotates overturned decisions.
---

# Writing a decision log

## Read first

**`docs/log/FORMAT.md`.** It is the single source of truth for what a log contains and omits, the
skeleton, the header fields and the per-section rules. This skill does not restate the convention;
below is only what the convention does not say: **order of work and verification.**

## Procedure

1. **Number** — `ls docs/log/` to take the next number. Never reuse a retired number (the `결번`
   line in `docs/log/README.md`).
2. **Skeleton** — start from `TEMPLATE.md` in this folder. The template and the log body are in
   Korean; section headings (`## 결정`, `## 근거`, `## 산출물`, `## 미결`) are literal and checked
   by `check.py`.
3. **Body** — write per the convention. Decision bullets carry `[D<n>-k]` ids, open-decision bullets
   carry `[U<n>-k]` ids.
4. **Back-annotation** — open every log named in the header's `관련` field. If this log overturns or
   closes a decision there, add a `> **YYYY-MM-DD — …**` quote block *under that bullet in the old
   log*. Writing only in the new log leaves the old one reading as if the matter were still open.
5. **Index** — add one row to the table in `docs/log/README.md`. This is the step most often missed.

## Verify

```bash
python3 .claude/skills/log/check.py docs/log/<file>
```

Catches missing sections, unlinked log numbers, broken links, missing index rows, bullets without
ids, and overturned ids that lack a back-annotation. Whether the content respects the convention's
boundary (rationale, rejected options, open decisions — not procedures or results) is a human judgment.
