---
name: export-session
description: Claude Code 세션의 대화 원문을 docs/ai_log/ 마크다운으로 내보내는 도구. 보통은 훅이 자동으로 돌리므로 Claude 가 직접 부를 일은 드물다 — 훅이 안 돌았거나 지난 세션 파일을 내보낼 때만.
---

# 세션 대화 전문 내보내기

## 보통은 훅이 한다

`.claude/settings.json` 의 UserPromptSubmit 훅이 매 프롬프트를 보고, "대화 내보내기 해줘" ·
"세션 저장해" · "대화 md로" 같은 문구가 있으면 `hook.py` 가 바로 내보낸다. 결과는 Claude 에게
additionalContext 로 전달되므로 **Claude 는 다시 돌리지 말고 그 결과만 한 줄로 알린다.**

## 무엇을 남기나

**사용자가 화면에서 본 것만** — 사용자 발화와 AI 답변 원문. 도구 호출·도구 결과·AI 내부 사고·
시스템 리마인더·슬래시 명령은 뺀다. 이메일은 가린다.

## 손으로 돌릴 때 (훅이 안 돌았거나 지난 세션일 때)

```bash
ls -t ~/.claude/projects/-home-young-dev-luckproof-verdict/*.jsonl | head -3   # 세션 파일 찾기
python3 .claude/skills/export-session/export_session.py <세션 jsonl> docs/ai_log/<단계>_대화전문_<YYYY-MM-DD>.md
```

출력 이름 규칙은 훅과 같다: `<가장 높은 번호의 workflow 문서 이름에서 "단계" 를 뺀 것>_대화전문_<날짜>.md`.
같은 날 같은 단계는 덮어쓴다.

## 확인·커밋

출력에서 `@` 와 `KRX_PW=`·`CHATKHU_API_KEY=` 뒤에 실제 값이 없는지 본다. 커밋은 `ai_log:` 접두로 한 단위.

## 한계

- 내보내기를 실행한 프롬프트에 대한 답변은 파일에 없다 (훅이 답변 전에 돈다). 세션 마지막 일로
  돌리거나 다음 세션에서 지난 세션 파일로 다시 돌린다.
- `/clear` 는 새 세션 ID 를 만든다.
