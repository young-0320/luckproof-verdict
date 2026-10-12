"""Convert a Claude Code session transcript (JSONL) into a Markdown conversation log for docs/ai_log/.

Usage: python3 .claude/skills/export-session/export_session.py <session.jsonl> <output.md>
Session files live in ~/.claude/projects/-home-young-dev-luckproof-verdict/<session-id>.jsonl

Rules: keep only what the user saw on screen -- user prompts and assistant replies, verbatim.
Drop thinking blocks, tool calls, tool results, system reminders and slash-command blocks.
Mask email addresses (submission documents must not contain personal data).
The output document itself stays in Korean because docs/ are Korean.
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone

KST = timezone(timedelta(hours=9))


def clean_user(text: str) -> str:
    """Strip harness-injected blocks from a user message; return "" if nothing user-written remains."""
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    text = re.sub(r"<local-command-caveat>.*?</local-command-caveat>", "", text, flags=re.S)
    text = re.sub(r"<command-name>.*?</command-name>\s*<command-message>.*?</command-message>\s*<command-args>.*?</command-args>", "", text, flags=re.S)
    text = re.sub(r"<local-command-stdout>.*?</local-command-stdout>", "", text, flags=re.S)
    return text.strip()


def redact(text: str) -> str:
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[이메일 가림]", text)


def main(src: str, dst: str) -> int:
    """Write the Markdown log to dst. Returns the number of utterances written."""
    out, session_id, first_ts = [], None, None
    for line in open(src, encoding="utf-8"):
        d = json.loads(line)
        if d.get("type") not in ("user", "assistant"):
            continue
        session_id = session_id or d.get("sessionId")
        ts = d.get("timestamp")
        first_ts = first_ts or ts
        stamp = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(KST).strftime("%H:%M") if ts else ""
        content = d["message"].get("content")
        if isinstance(content, str):  # plain user prompt
            text = clean_user(content)
            if text:
                out.append(f"## 사용자 ({stamp})\n\n{text}\n")
            continue
        for b in content:  # block list: only assistant text survives; tool_use/tool_result/thinking are dropped
            if b.get("type") == "text" and d["type"] == "assistant":
                out.append(f"## AI ({stamp})\n\n{b['text'].strip()}\n")
    day = datetime.fromisoformat(first_ts.replace("Z", "+00:00")).astimezone(KST).strftime("%Y-%m-%d")
    head = (f"# Claude Code 세션 대화 전문 — {day}\n\n"
            f"- 세션 ID: `{session_id}`\n- 모델: Claude Fable 5.1 (Claude Code)\n\n---\n\n")
    open(dst, "w", encoding="utf-8").write(redact(head + "\n".join(out)))
    return len(out)


if __name__ == "__main__":
    print(sys.argv[2], main(sys.argv[1], sys.argv[2]), "utterances")
