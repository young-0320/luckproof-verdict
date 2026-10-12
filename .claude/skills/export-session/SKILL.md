---
name: export-session
description: Export a Claude Code session transcript to docs/ai_log/ as a Markdown conversation log (user prompts and assistant replies only). A UserPromptSubmit hook normally runs it automatically, so invoke this skill only when the hook did not fire or when exporting a past session's file.
---

# Export session transcript

## The hook usually does this

The UserPromptSubmit hook in `.claude/settings.json` inspects every prompt. When it contains a Korean
phrase such as "대화 내보내기 해줘", "세션 저장해" or "대화 md로", `hook.py` exports immediately and
returns the result to Claude as additionalContext. **Claude must not run the export again; it reports
the result in one line.**

## What the export keeps

Only what the user saw on screen: user prompts and assistant replies, verbatim. Tool calls, tool
results, thinking blocks, system reminders and slash-command blocks are dropped. Email addresses are
masked. The output document is in Korean (headings `## 사용자`, `## AI`) because docs/ are Korean.

## Running it by hand (hook did not fire, or a past session)

```bash
ls -t ~/.claude/projects/-home-young-dev-luckproof-verdict/*.jsonl | head -3   # find the session file
python3 .claude/skills/export-session/export_session.py <session.jsonl> docs/ai_log/<stage>_대화전문_<YYYY-MM-DD>.md
```

Naming rule, same as the hook: `<stem of the highest-numbered docs/workflow doc, minus "단계">_대화전문_<date>.md`.
Same stage on the same day overwrites.

## Verify and commit

Check the output for `@` and for real values after `KRX_PW=` or `CHATKHU_API_KEY=`. Commit as one unit
with the `ai_log:` prefix.

## Limits

- The reply to the prompt that triggered the export is not in the file (the hook runs before the reply).
  Run it as the last action of a session, or re-run on the previous session's file next time.
- `/clear` starts a new session id, so one day can have several files.
