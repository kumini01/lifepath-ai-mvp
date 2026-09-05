# 🧭 LifePath AI MVP

AI 기반 개인 생애주기 통합관리 플랫폼의 실행 가능한 MVP입니다.

## 핵심 사용자 흐름
프로필 등록 → 생애 이벤트 등록 → Dashboard 확인 → To-Do 관리 → AI Life Coach 상담

## 기능
- Life Dashboard: 이벤트/미완료 할 일/가족 현황 요약
- My Life: 교육·경력·가족·주거·자산·건강·노후 이벤트 관리
- To-Do: 마감일과 완료 상태 관리
- 가족: 가족 구성원 기본정보 관리
- AI Life Coach: 등록 데이터를 컨텍스트로 활용한 AI 상담
- 설정: 개인 프로필 관리

## 기술 스택
- Python
- Streamlit
- SQLite
- OpenAI Responses API

## 실행
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

AI Life Coach 메뉴에서 OpenAI API Key를 입력하면 AI 상담 기능을 사용할 수 있습니다. API Key는 SQLite DB에 저장하지 않습니다.

## 프로젝트 구조
```text
lifepath-ai-mvp/
├── app.py
├── db.py
├── ai_service.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/              # 실행 시 자동 생성
```

## MVP 다음 단계
PostgreSQL/FastAPI/Next.js 전환, 인증, 문서 OCR, RAG, 공공 API, 알림 서비스를 단계적으로 추가할 예정입니다.
