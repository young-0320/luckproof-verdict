# 설계 결정 로그

> **로그는 "왜 이렇게 만들었나"에 대한 답이지 일지가 아니다.**
> 설계 수치는 `spec/` 에, 프롬프트와 답변은 `ai_log/` 에, **결정 근거와 버린 후보와 미결은 로그에.**

서식 규약은 **[FORMAT.md](FORMAT.md)**. 검사는 `python3 .claude/skills/log/check.py docs/log/<파일>`.

결번: 없음

| # | 로그 | 여기에만 있는 것 |
| - | ---- | ---------------- |
| 1 | [2단계 데이터 범위·원천·LLM 결정](1.data_scope_source_and_llm.md) | 시총 상위 350 → 날짜별 KOSPI200 으로 바꾼 이유, 네이버 → KRX 전환 이유, Gemini 를 안 쓰는 이유 |
