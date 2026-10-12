"""UserPromptSubmit hook: when the prompt asks to export/save the conversation, write the session
transcript to docs/ai_log/ and tell Claude what happened via additionalContext.

Reads {"prompt", "transcript_path", "cwd", ...} from stdin. Does nothing if the trigger phrase is absent.
Output path: docs/ai_log/<highest-numbered docs/workflow doc stem, minus the "단계" suffix>_대화전문_<today>.md
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from export_session import main as export  # noqa: E402

# Korean phrases only: "대화 내보내기", "세션 저장해", "대화 md로" ... Matching English here caused a
# false positive on file paths such as ".../export-session/SKILL.md".
TRIGGER = re.compile(r"(대화|세션)\s*(전문|원문|기록)?\s*(을|를)?\s*(내보내|저장|md|마크다운)")


def stage_name(root: Path) -> str:
    docs = sorted(root.glob("docs/workflow/[0-9]*_*.md"), key=lambda p: int(p.name.split("_")[0]))
    return docs[-1].stem.removesuffix("단계") if docs else "세션"


def run() -> None:
    data = json.load(sys.stdin)
    if not TRIGGER.search(data.get("prompt", "")):
        return
    root = Path(data.get("cwd") or ".")
    today = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")
    dst = root / "docs" / "ai_log" / f"{stage_name(root)}_대화전문_{today}.md"
    n = export(data["transcript_path"], str(dst))
    msg = (f"[export-session hook] Conversation log written to {dst.relative_to(root)} ({n} utterances). "
           f"The reply to this prompt is not included. Do not run the export again; report the result in one line.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}},
                     ensure_ascii=False))


if __name__ == "__main__":
    run()
