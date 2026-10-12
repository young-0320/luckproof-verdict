"""UserPromptSubmit 훅: 프롬프트에 "대화 내보내기/저장" 류 문구가 있으면 세션 전문을 docs/ai_log/ 에 쓴다.

stdin 으로 {"prompt", "transcript_path", "cwd", ...} 를 받는다. 문구가 없으면 아무것도 하지 않는다.
출력 이름: docs/ai_log/<가장 높은 번호의 workflow 문서 이름에서 '단계' 를 뺀 것>_대화전문_<오늘>.md
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from export_session import main as export  # noqa: E402

TRIGGER = re.compile(r"(대화|세션).{0,12}(내보내|저장|md|마크다운)|export.{0,8}session", re.I)


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
    msg = (f"[export-session 훅] 대화 전문을 {dst.relative_to(root)} 에 저장했다 ({n}개 발화). "
           f"이 답변 자체는 포함되지 않는다. 다시 내보내기를 돌리지 말고 결과만 한 줄로 알려라.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": msg}},
                     ensure_ascii=False))


if __name__ == "__main__":
    run()
