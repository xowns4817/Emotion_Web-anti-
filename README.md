# 🎭 감정 기반 콘텐츠 추천 웹 서비스

감정 상태 설문조사를 통해 사용자의 감정을 분석하고, 멀티 에이전트 기반으로 맞춤 콘텐츠(글귀, 영상, 사진)를 추천하는 웹 서비스입니다.

---

## 📐 아키텍처

```
사용자 (React) → Spring Boot (REST API / DB) → FastAPI + LangGraph (Agent)
                                              ← 콜백 (감정 분석 / 콘텐츠 추천 결과)
                                                         ↓
                                              MCP Client (stdio)
                                                         ↓
                                    Brave Search MCP Server (Public)
                                       또는 폴백 데이터 (로컬)
```

| 계층 | 기술 | 역할 |
|------|------|------|
| **프론트엔드** | React 18 + Vite + TypeScript | 설문 UI, 추천 결과 UI |
| **서비스 레이어** | Spring Boot 3.4.2 + JPA | 상태/DB 관리, REST API, 콜백 수신 |
| **오케스트레이션** | FastAPI + LangGraph + LangChain | 멀티 에이전트 워크플로우 |
| **LLM** | Google Gemini (gemini-2.0-flash) | 감정 분석 |
| **콘텐츠 소스** | Brave Search MCP (Public) + 폴백 | 글귀/영상/사진 검색 |
| **DB** | PostgreSQL 16 | 설문, 감정 기록, 추천 콘텐츠 저장 |

---

## 📁 프로젝트 구조

```
Emotion_Test_ANTI/
├── frontend/                    React + Vite + TypeScript
│   └── src/
│       ├── api/emotionApi.ts          API 호출 모듈
│       ├── types/index.ts             타입 정의 + 감정 색상/이모지
│       ├── pages/SurveyPage/          7문항 설문 UI
│       ├── pages/ResultPage/          감정 카드 + 콘텐츠 3탭
│       ├── App.tsx                    루트 컴포넌트
│       └── index.css                  다크모드 디자인 시스템
│
├── backend/                     Spring Boot 3.4.2
│   └── src/main/java/com/emotion/
│       ├── entity/                    JPA 엔티티 (3개)
│       ├── repository/                JPA Repository (3개)
│       ├── dto/                       DTO (6개)
│       ├── service/                   비즈니스 로직 (4개)
│       ├── controller/                REST Controller (3개)
│       └── config/                    CORS, WebClient 설정
│
├── agent/                       FastAPI + LangGraph
│   └── app/
│       ├── graph/                     LangGraph 상태/노드/워크플로우
│       ├── agents/                    감정 분석 / 콘텐츠 검색 Agent
│       ├── tools/                     Spring Boot 콜백 / MCP 클라이언트
│       ├── prompts/                   LLM 프롬프트
│       └── api/routes.py              /analyze 엔드포인트
│
├── docker-compose.yml           PostgreSQL 16 (포트 5433)
└── DESIGN.md                    상세 설계 문서
```

---

## 🚀 실행 방법

### 사전 요구사항
- **Docker** (PostgreSQL용)
- **Java 17+** (Spring Boot)
- **Node.js 18+** (React)
- **Python 3.12** (Agent 서버 — MCP SDK 요구)
- **Miniconda** (권장)
- **Node.js + npx** (Brave Search MCP 서버 실행용)

### 1. PostgreSQL 실행

```bash
docker-compose up -d
```

### 2. Agent 서버 실행 (Python)

```bash
# Miniconda 환경 생성 (Python 3.12 + MCP SDK)
conda env create -f agent/environment.yml
conda activate emotion-agent

# .env 파일 설정 확인
# - GOOGLE_API_KEY: 필수 (Gemini API)
# - BRAVE_API_KEY: 선택 (없으면 폴백 데이터 사용)

# Agent 서버 실행
python -m uvicorn app.main:app --port 8000 --reload
```

### 3. Spring Boot 실행

```bash
cd backend
./gradlew bootRun
```

### 4. React 프론트엔드 실행

```bash
cd frontend
npm install
npm run dev
```

### 5. 브라우저 접속

```
http://localhost:5173
```

---

## 🔌 포트 매핑

| 서비스 | 포트 |
|--------|------|
| React (Frontend) | `5173` |
| Spring Boot (Backend) | `8080` |
| FastAPI (Agent) | `8000` |
| PostgreSQL (Docker) | `5433` |

---

## 🔄 핵심 플로우

```
1. 사용자가 7문항 설문 작성 → 제출
2. Spring Boot: 설문 저장 (DB) → FastAPI에 분석 요청
3. FastAPI: LangGraph 워크플로우 실행
   ├── [Node 1] 감정 분석 (Gemini LLM) → Spring Boot 콜백
   └── [Node 2] 콘텐츠 검색
        ├── Brave Search MCP 호출 (API 키 있을 때)
        └── 폴백 데이터 사용 (API 키 없을 때)
        → Spring Boot 콜백
4. Spring Boot: 결과 DB 저장
5. 프론트엔드: 폴링으로 결과 수신 → 감정 카드 + 콘텐츠 표시
```

---

## 📊 데이터 모델

| 테이블 | 설명 |
|--------|------|
| `survey_response` | 설문 응답 (sessionId, answers JSON, status) |
| `emotion_record` | 감정 분석 결과 (primaryEmotion, score, detail JSON) |
| `content_recommendation` | 추천 콘텐츠 (type, title, body, source, score) |

---

## ⚙️ 환경 변수

### Agent 서버 (`agent/.env`)

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `GOOGLE_API_KEY` | Google Gemini API 키 | (필수) |
| `LLM_MODEL` | LLM 모델명 | `gemini-2.0-flash` |
| `BRAVE_API_KEY` | Brave Search API 키 | (선택, 없으면 폴백 데이터) |
| `SPRING_BOOT_URL` | Spring Boot URL | `http://localhost:8080` |

### Spring Boot (`backend/src/main/resources/application.yml`)

| 설정 | 설명 | 기본값 |
|------|------|--------|
| `spring.datasource.url` | PostgreSQL URL | `jdbc:postgresql://localhost:5433/emotion_db` |
| `agent.server.url` | FastAPI Agent URL | `http://localhost:8000` |

---

## 🔑 Brave Search API 키 설정 (선택)

Agent 서버는 **Brave Search MCP**를 통해 실시간 웹 검색을 수행합니다. 
API 키가 없는 경우 **로컬 폴백 데이터**로 자동 전환되므로 키 없이도 정상 작동합니다.

### API 키 발급 (무료)
1. https://brave.com/search/api/ 접속
2. Free Plan 선택 — **월 2,000회 무료**
3. API 키 복사 (예: `BSAxxxxxxxxx...`)
4. `agent/.env` 파일 수정:
   ```bash
   BRAVE_API_KEY=발급받은키입력
   ```
5. Agent 서버 재시작

### 작동 방식
- **API 키 있을 때**: Brave Search로 YouTube 영상/글귀/이미지 실시간 검색
- **API 키 없을 때**: 감정별 큐레이팅된 로컬 데이터 사용 (70+ 명언, Pexels 이미지, YouTube 링크)

---

## 🗺️ 개발 로드맵

- [x] **Phase 1**: 프로토타입 (설문 → 감정 분석 → 콘텐츠 추천)
- [ ] **Phase 2**: 로그인/회원가입 (이름, 성별, 나이, 직업) + JWT 인증
- [ ] **Phase 3**: 기간별 감정 추이 그래프 + 리포트

---

## 🛠️ 기술 스택

| 분류 | 기술 |
|------|------|
| Frontend | React 18, Vite, TypeScript, Vanilla CSS |
| Backend | Spring Boot 3.4.2, JPA, Gradle (Kotlin DSL) |
| Agent | FastAPI, LangGraph, LangChain, MCP SDK |
| LLM | Google Gemini (gemini-2.0-flash) |
| MCP | Brave Search MCP (Public) + 폴백 데이터 |
| DB | PostgreSQL 16 (Docker, 포트 5433) |
| Infra | Docker Compose, Miniconda |
