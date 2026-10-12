# 협업 규칙

> **이 문서는** 폴더 배치와 문서 층 구분을 정한다. 작업 방식은 `CLAUDE.md`, 지금 상태와 결정은
> `project_context.md`, 단계별 할 일은 `docs/workflow/`.

## 1. 폴더 구조

```
luckproof-verdict/
├── CONTRIBUTING.md        # 이 문서 — 폴더 배치와 문서 4층 구분
├── README.md              # 사람용 입구 — 작품 소개 (서식3의 원천). 선별본과 어긋나면 안 된다
├── CLAUDE.md              # 에이전트 작업 방식 — 규칙만. project_context.md 를 @import
├── project_context.md     # 지금 상태 · 확정된 결정 · 미결 · 문서 지도. 단계가 바뀌면 갱신
├── pyproject.toml         # uv 프로젝트. `uv run python -m luckproof.data.fetch`
├── luckproof/             # 코드
│   └── data/              # 시세 수집 (fetch.py) → data/prices.duckdb
├── data/          (.gitignore)   # 시세 DB. 스크립트로 재생성. 커밋 금지
├── .env           (.gitignore)   # KRX_ID · KRX_PW · CHATKHU_API_KEY. 커밋 금지
├── .claude/skills/         # log (설계 결정 로그 작성) · export-session (세션 대화 전문 내보내기)
└── docs/
    ├── ai_log/            # 1층 — AI 대화 전문
    ├── ai_log_선별본/     # 2층 — 서식4 제출용 선별
    ├── log/               # 3층 — 설계 결정의 의도 (규약 FORMAT.md, 목록 README.md)
    ├── spec/              # 4층 — 설계 자체
    ├── workflow/          # 단계별 할 일과 완료 기준
    ├── 심사기준.md         # 심사표
    └── 참가자 제출서류*.pdf   # 서식1~5 원문. 판단 기준은 항상 이 PDF
```

## 2. 문서 네 층

같은 일이 네 군데에 다른 모양으로 남는다. **한 층에 있는 것을 다른 층에 되풀이하지 않는다.**

| 층 | 경로 | 담는 것 | 규칙 |
| -- | ---- | ------- | ---- |
| 1 | `docs/ai_log/` | AI 대화 전문 | 원문 그대로. 편집하지 않음. 1단계는 ChatKHU 내보내기, 2단계부터는 Claude Code 세션 기록을 변환해 저장 |
| 2 | `docs/ai_log_선별본/` | 서식4 제출용 선별 | 요약 블록 + 프롬프트 원문 + 답변 요지 + 내 판단 + 검증 + 버전 변화. 수용뿐 아니라 기각·철회·범위 결정을 적는다 |
| 3 | `docs/log/` | 설계 결정의 의도. 왜 정했나, 버린 후보, 미결 | 규약 `docs/log/FORMAT.md`. 스킬 `/log`. 검사 `python3 .claude/skills/log/check.py docs/log/<파일>` |
| 4 | `docs/spec/` | 설계 자체. 수치와 조건만 건조하게 | 왜 그 값인가는 `docs/log/` 로 링크 |

어디에 쓸지 애매하면: 프롬프트와 답변이면 1, 심사위원에게 보일 것이면 2, "왜"면 3, "무엇"이면 4.
절차와 할 일은 네 층 어디도 아니고 `docs/workflow/`.

## 3. 배치 기준

1. **소스와 생성물 분리** — 사람이 쓴 텍스트와 코드만 커밋한다. 시세 DB는 `data/`, 키는 `.env`.
   둘 다 `.gitignore`.
2. **제출물에 개인정보·API 키 금지** — 대화 전문을 저장할 때 시스템 메시지와 이메일을 지운다.
3. **AI가 준 출처·수치·라이선스는 확인 없이 옮기지 않는다** — 확인해서 틀린 걸 잡은 기록이 가장
   강한 증빙이다. 그 기록은 1층(원문)과 2층(선별)에 남긴다.

## 4. git

- 작성자는 Young 단일. 공동 저자 줄을 붙이지 않는다.
- 작업 단위별로 커밋한다 (문서 하나, 단계 하나, 기능 하나).
