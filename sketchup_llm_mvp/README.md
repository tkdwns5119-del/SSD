# SketchUp 연동 LLM MVP

자연어 명령을 받아 SketchUp 모델을 생성/수정하는 최소 동작 예시입니다.

## 구조

- `sketchup_extension/llm_bridge.rb`: SketchUp Ruby 확장 진입점
- `server/main.py`: FastAPI 기반 LLM 명령 파서/검증 서버

## 동작 흐름

1. SketchUp 메뉴 `Extensions > LLM Bridge > Open Command Panel` 실행
2. 명령 입력 (예: `가로 4m 세로 3m 높이 2.7m 박스 만들어줘`)
3. Ruby 확장이 로컬 서버(`http://127.0.0.1:8000/parse`) 호출
4. 서버가 JSON 액션 반환
5. Ruby에서 액션 검증 후 모델 생성

## 서버 실행

```bash
cd sketchup_llm_mvp/server
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8000
```

## 지원 액션(MVP)

- `create_box`: width/depth/height(mm)
- `move_selection`: dx/dy/dz(mm)

## 주의

- 실제 상용화 전에는 인증/권한/감사로그/명령 화이트리스트를 반드시 강화하세요.
- LLM이 생성한 원문 코드를 실행하지 말고, 검증된 스키마(JSON)만 실행하세요.
