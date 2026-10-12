---
name: export-session
description: Claude Code 세션의 대화 원문을 docs/ai_log/ 마크다운으로 내보낼 때 — "대화 전문 저장해", "세션 내보내기", "오늘 대화 md로". 사용자 발화와 AI 답변만 남기고 도구 호출·결과·내부 사고는 뺀다.
---

# 세션 대화 전문 내보내기

## 무엇을 남기나

**사용자가 화면에서 본 것만** — 사용자 발화와 AI 답변 원문. 도구 호출·도구 결과·AI 내부 사고·
시스템 리마인더·슬래시 명령은 뺀다. 이메일은 가린다. 규칙은 `export_session.py` 머리에 있다.

## 절차

1. **세션 파일** — 지금 세션 ID 는 스크래치패드 경로의 마지막 디렉터리 이름이다. 파일은
   `~/.claude/projects/-home-young-dev-luckproof-verdict/<세션ID>.jsonl`. 모르면 가장 최근 것:
   ```bash
   ls -t ~/.claude/projects/-home-young-dev-luckproof-verdict/*.jsonl | head -1
   ```
2. **출력 이름** — `docs/ai_log/<단계번호>_<단계이름>_대화전문_<YYYY-MM-DD>.md`.
   같은 날 같은 단계가 이미 있으면 덮어쓴다 (세션이 이어지면 전문도 길어진 것으로 바뀐다).
3. **실행**
   ```bash
   python3 .claude/skills/export-session/export_session.py <세션 jsonl> <출력 md>
   ```
4. **확인** — 출력에서 `@` 를 찾아 이메일이 남지 않았는지, `KRX_PW=`·`CHATKHU_API_KEY=` 뒤에
   실제 값이 없는지 본다. 세션 안에서 키를 다룬 적이 있으면 그 줄을 손으로 지운다.
5. **커밋** — `ai_log:` 접두로 한 단위.

## 주의

- 내보내기를 실행한 그 답변은 파일에 들어가지 않는다 (파일을 만든 뒤에 생긴다). 세션의
  마지막 일로 돌리거나, 다음 세션 시작 때 지난 세션 파일로 돌린다.
- `/clear` 는 새 세션 ID 를 만든다. 하루에 여러 세션이면 파일도 여럿이다.
