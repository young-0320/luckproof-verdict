#!/usr/bin/env python3
"""Mechanical check of the log convention -- only the things a human reader tends to miss.

The convention itself is docs/log/FORMAT.md; this script is not the convention.
Usage: python3 .claude/skills/log/check.py docs/log/1.xxx.md
Section headings, id prefixes and FAIL messages are Korean literals because the log documents are Korean.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LOGS = REPO / "docs" / "log"
INDEX = REPO / "docs" / "log" / "README.md"
SECTIONS = ["## 결정", "## 근거", "## 미결"]   # "## 산출물" is optional, so not required here
KINDS = [("D", "## 결정"), ("U", "## 미결")]   # id kind -> the section that defines it
DEAD_SECTIONS = ["작업 내용", "미결 의사결정"]  # sections the convention retired
DEAD_FIELDS = ["성격", "작성"]                  # header fields the convention retired


def gaps(index: str) -> set[str]:
    """Numbers on the README "결번" (retired) line. They have no file, so no link is required."""
    line = re.search(r"^#+\s*결번.*$", index, re.M)
    return set(re.findall(r"\d+", line.group())) if line else set()


def section(text: str, head: str) -> list[str]:
    """Lines of the `## <head>` section, closed by the next `## `."""
    out, on = [], False
    for l in text.splitlines():
        if l.startswith("## "):
            on = l.strip() == head
        elif on:
            out.append(l)
    return out


def ids(lines: list[str], num: str, kind: str) -> tuple[dict[str, bool], list[str]]:
    """Ids this log defines -> whether a back-annotation sits under them. Also returns duplicate ids.

    A bullet opens the span of its id; the next bullet or heading closes it.
    A `> **20…` line inside the span is a back-annotation (indented or not).
    Only ids carrying this log's own number count as definitions; other numbers are citations.
    """
    out, dup, cur = {}, [], None
    for l in lines:
        if m := re.match(rf"^- .*?\[{kind}(\d+)-(\d+)\]", l):
            cur = f"{m.group(1)}-{m.group(2)}" if m.group(1) == num else None
            if cur:
                if cur in out:
                    dup.append(cur)
                out.setdefault(cur, False)
        elif re.match(r"^(- |#)", l):
            cur = None
        elif cur and re.match(r"\s*> \*\*20", l):
            out[cur] = True
    return out, dup


def unlabeled(lines: list[str], kind: str) -> list[str]:
    """Bullets without an id -- nothing to cite when the decision is later overturned."""
    return [l.strip()[:44] for l in lines
            if l.startswith("- ") and not re.search(rf"\[{kind}\d+-\d+\]", l)]


def crossref() -> list[str]:
    """Every decision/open item cited as overturned or closed must carry a back-annotation -- needs all logs."""
    defined, annotated, cites = {}, set(), {}
    for f in sorted(LOGS.glob("[0-9]*.md")):
        num, text = f.name.split(".")[0], f.read_text(encoding="utf-8")
        for kind, head in KINDS:
            got, _ = ids(section(text, head), num, kind)
            for i, noted in got.items():
                defined[kind + i] = f.name
                if noted:
                    annotated.add(kind + i)
        for k, i in re.findall(r"\[([DU])(\d+-\d+)\][^\n]{0,8}?(?:뒤집|닫)", text):
            cites.setdefault(k + i, f.name)

    bad = []
    for i in sorted(cites.keys() - annotated):
        if defined.get(i) == cites[i]:
            continue                      # a mention inside the defining log is not a citation
        where = defined.get(i)
        bad.append(f"[{i}] — {cites[i]} 가 뒤집었다는데 "
                   + (f"{where} 에 추기가 없다" if where else "정의한 로그가 없다"))
    return bad


def check(target: Path) -> list[str]:
    bad = []
    text = target.read_text(encoding="utf-8")
    index = INDEX.read_text(encoding="utf-8")
    num = target.name.split(".")[0]

    for s in SECTIONS:
        if not re.search(rf"^{re.escape(s)}", text, re.M):
            bad.append(f"골격 누락 — {s}")

    # A log number must be linked at its first mention; `[로그 23 부록 A](...)` also counts.
    # The log's own number and retired numbers have no file, so they are exempt.
    linked = {n for n in re.findall(r"\[로그 (\d+)[^\]]*\]\([^)]+\.md\)", text)}
    # A range (~) or a counter suffix after the number is not a reference -- "로그 9개", "로그 1~15".
    seen = set(re.findall(r"로그 (\d+)(?![\d~])(?!\s*[개편건줄])", text))
    for n in sorted(seen - linked - gaps(index) - {num}, key=int):
        bad.append(f"로그 {n} — 링크가 한 번도 안 걸렸다")

    for _, tgt in re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", text):
        if not (target.parent / tgt).exists():
            bad.append(f"깨진 링크 — {tgt}")

    if f"]({num}." not in index:
        bad.append(f"목록 미등재 — docs/log/README.md 에 로그 {num} 행이 없다")

    # Retired sections/fields: the only boundary violations catchable by fixed strings.
    # Procedures and numbers in the artifact table vary each time -- a human checks those.
    for name in DEAD_SECTIONS:
        if re.search(rf"^#+ .*{name}", text, re.M):
            bad.append(f"폐지된 절 — `## {name}`")
    for name in DEAD_FIELDS:
        if re.search(rf"^- \*?\*?{name}\*?\*?\s*:", text, re.M):
            bad.append(f"폐지된 머리말 필드 — `{name}`")

    # Ids are the handle for overturn/close cross-referencing; required in both sections.
    for kind, head in KINDS:
        lines = section(text, head)
        # A table defeats all three checks at once: bullets without ids pass (unlabeled), definitions
        # drop out of the crossref denominator (ids), and no annotation span opens. The convention
        # assumes bullets, so tables are rejected outright.
        if any(l.lstrip().startswith("|") for l in lines):
            bad.append(f"{head} 가 표다 — 불릿으로 쓴다 (ID·추기 검사가 비켜간다)")
        got, dup = ids(lines, num, kind)
        for b in unlabeled(lines, kind):
            bad.append(f"{head} ID 없음 — `[{kind}{num}-n]` 을 단다: {b}")
        for d in sorted(set(dup)):
            bad.append(f"[{kind}{d}] 가 두 번 정의됐다")

    return bad


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(f"usage: {Path(__file__).name} <log file>")
    target = Path(sys.argv[1]).resolve()

    bad = check(target)
    for b in bad:
        print(f"  FAIL  {b}")
    print(f"{target.name}: {'통과' if not bad else str(len(bad)) + '건'}")

    missing = crossref()
    for m in missing:
        print(f"  MISS  {m}")

    notes = sum(1 for f in LOGS.glob("[0-9]*.md")
                for l in f.read_text(encoding="utf-8").splitlines()
                if re.match(r"\s*> \*\*20", l))
    print(f"추기 {notes}곳 · 인용 대조 "
          f"{'통과' if not missing else str(len(missing)) + '건'}")
    return 1 if bad or missing else 0


if __name__ == "__main__":
    sys.exit(main())
