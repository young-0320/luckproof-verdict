"""Claude Code 세션 기록(JSONL) → docs/ai_log 대화 전문 마크다운

사용: python3 .claude/skills/export-session/export_session.py <세션 jsonl> <출력 md>
세션 파일: ~/.claude/projects/-home-young-dev-luckproof-verdict/<세션ID>.jsonl

변환 규칙: 사용자 발화와 AI 답변(화면에 보인 글)만, 원문 그대로. AI 내부 사고·도구 호출·도구 결과는 뺀다.
시스템 리마인더·슬래시 명령 블록은 지운다. 이메일 주소는 가린다 (제출물 개인정보 금지).
"""
import json
import re
import sys
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))


def clean_user(text: str) -> str:
    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", text, flags=re.S)
    text = re.sub(r"<local-command-caveat>.*?</local-command-caveat>", "", text, flags=re.S)
    text = re.sub(r"<command-name>.*?</command-name>\s*<command-message>.*?</command-message>\s*<command-args>.*?</command-args>", "", text, flags=re.S)
    text = re.sub(r"<local-command-stdout>.*?</local-command-stdout>", "", text, flags=re.S)
    return text.strip()


def redact(text: str) -> str:
    return re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[이메일 가림]", text)



def main(src: str, dst: str) -> None:
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
        if isinstance(content, str):
            text = clean_user(content)
            if text:
                out.append(f"## 사용자 ({stamp})\n\n{text}\n")
            continue
        for b in content:
            t = b.get("type")
            if t == "text" and d["type"] == "assistant":
                out.append(f"## AI ({stamp})\n\n{b['text'].strip()}\n")
    day = datetime.fromisoformat(first_ts.replace("Z", "+00:00")).astimezone(KST).strftime("%Y-%m-%d")
    head = (f"# Claude Code 세션 대화 전문 — {day}\n\n"
            f"- 세션 ID: `{session_id}`\n- 모델: Claude Fable 5.1 (Claude Code)\n"
            f"- 변환: `.claude/skills/export-session/export_session.py`. 사용자 발화와 AI 답변만 원문 그대로. "
            f"AI 내부 사고·도구 호출·도구 결과는 제외, 이메일은 가림.\n\n---\n\n")
    open(dst, "w", encoding="utf-8").write(redact(head + "\n".join(out)))
    print(dst, len(out), "blocks")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
