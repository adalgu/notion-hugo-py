# 통합 파이프라인 구현 (2025-03-14)

## 요약

노션 변환 기능과 Hugo 전처리 기능을 통합하여 완전한 파이프라인을 구현했습니다. 이 작업을 통해 노션에서 콘텐츠를 가져와 마크다운으로 변환하고, Hugo 빌드 오류를 방지하는 전처리를 수행한 후 최종 빌드까지 한 번에 수행할 수 있게 되었습니다.

## 주요 변경사항

### 1. Hugo 전처리 모듈화 (`src/hugo_processor.py`)

- `hugo_preprocess.py`를 `src/hugo_processor.py`로 이동
- 기존 `hugo_integration.py` 기능과 통합
- 주요 클래스:
  - `HugoProcessor`: Hugo 관련 작업을 관리하는 메인 클래스
  - `HugoPreprocessor`: 빌드 오류를 일으킬 수 있는 문제 파일 처리
- 주요 기능:
  - 구조 확인 및 디렉토리 생성 (`ensure_structure`)
  - 콘텐츠 저장 (`save_content`)
  - 전처리 실행 (`preprocess`)
  - 빌드 실행 (`build`)
  - 서버 실행 (`run_server`)
  - 콘텐츠 정리 (`clean_content`)

### 2. 통합 파이프라인 구현 (`src/notion_hugo.py`)

- Notion API 호출, 마크다운 변환, Hugo 전처리, 빌드를 순차적으로 실행
- 주요 함수:
  - `run_notion_pipeline`: Notion에서 콘텐츠를 가져와 마크다운으로 변환
  - `run_hugo_pipeline`: Hugo 전처리 및 빌드 실행
  - 기존 `src/index.py`의 함수들을 통합하여 재사용
- 명령줄 인터페이스 구현
  - `--notion-only`: Notion 변환만 수행
  - `--hugo-only`: Hugo 전처리 및 빌드만 수행
  - `--no-build`: 빌드 단계 건너뛰기
  - `--hugo-args`: Hugo에 추가 인자 전달

### 3. 진입점 스크립트 생성 (`notion_hugo_app.py`)

- 프로젝트 루트에 사용자가 쉽게 실행할 수 있는 진입점 스크립트 생성
- `src.notion_hugo` 모듈의 `main` 함수 호출
- 모듈 경로 추가로 다양한 위치에서 실행 가능

### 4. README 업데이트

- 통합 파이프라인 사용법 설명
- 다양한 실행 옵션 설명
- 프로젝트 구조 업데이트
- 문제 해결 가이드 추가

## 기술적 세부사항

### 에러 처리 메커니즘

- Hugo 빌드 오류가 있는 파일을 자동으로 식별
- 오류 패턴 및 알려진 문제 shortcode 목록 사용
- 문제 파일을 임시 디렉토리로 이동시켜 빌드 진행
- 빌드 완료 후 원래 위치로 파일 복원
- 오류 로그를 JSON 형식으로 저장 (`docs/build_errors.json`)

### 인터럽트 처리

- `SIGINT` 신호(Ctrl+C) 처리
- 인터럽트 발생 시 이동된 파일 복원
- 일관된 종료 코드 사용 (130: SIGINT에 의한 종료)

### 모듈 간 상호작용

```
notion_hugo_app.py
    ↓
src/notion_hugo.py
    ↓
  ┌────────────────────┐
  ↓                    ↓
Notion 파이프라인       Hugo 파이프라인
(src/index.py)         (src/hugo_processor.py)
```

## 향후 개선 사항

- 병렬 처리 도입으로 대규모 데이터베이스 처리 성능 개선
- 변경된 페이지만 선택적으로 업데이트하는 증분 처리 메커니즘
- 더 상세한 로깅 및 모니터링 기능
- 웹 인터페이스 또는 GUI 추가 가능성

## 테스트 방법

전체 파이프라인 테스트:

```bash
python notion_hugo_app.py
```

Notion 변환만 테스트:

```bash
python notion_hugo_app.py --notion-only
```

Hugo 전처리만 테스트:

```bash
python notion_hugo_app.py --hugo-only
```

서버 모드로 테스트:

```bash
python notion_hugo_app.py --hugo-args="server -D"
```
