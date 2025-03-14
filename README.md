# Notion-Hugo 통합 파이프라인

노션 데이터베이스/페이지를 마크다운으로 변환하고, Hugo 빌드 전 오류 파일을 처리하여 완전한 빌드 파이프라인을 제공하는 Python 애플리케이션입니다.

## 개요

이 프로젝트는 다음 기능을 제공합니다:

1. **Notion 데이터베이스 설정**: 새 노션 데이터베이스 자동 생성 및 기존 데이터베이스 마이그레이션
2. **증분 처리 시스템**: 변경된 페이지만 처리하여 성능 최적화
3. **Notion 콘텐츠 가져오기**: Notion API를 통해 데이터베이스와 페이지에서 콘텐츠를 가져옵니다.
4. **마크다운 변환**: Notion 블록을 Hugo 호환 마크다운으로 변환합니다.
5. **Hugo 전처리**: 빌드 오류를 일으킬 수 있는 문제 파일을 식별하고 처리합니다.
6. **Hugo 빌드**: 최종 웹사이트를 생성합니다.

## 목차

- [설치 방법](#설치-방법)
- [초기 설정](#초기-설정)
  - [Notion 데이터베이스 설정](#notion-데이터베이스-설정)
  - [기존 데이터베이스 마이그레이션](#기존-데이터베이스-마이그레이션)
  - [수동 설정](#수동-설정)
- [파이프라인 실행](#파이프라인-실행)
  - [전체 파이프라인 실행](#전체-파이프라인-실행)
  - [증분 처리 옵션](#증분-처리-옵션)
  - [기타 실행 옵션](#기타-실행-옵션)
- [Docker 환경](#docker-환경)
  - [기본 사용법](#기본-사용법)
  - [Docker 환경 변수](#docker-환경-변수)
  - [Docker 고급 옵션](#docker-고급-옵션)
- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [문제 해결](#문제-해결)
- [라이선스](#라이선스)

## 설치 방법

1. 저장소 클론

```bash
git clone https://github.com/yourusername/notion-hugo-py.git
cd notion-hugo-py
```

2. 필요한 패키지 설치

```bash
pip install notion-client python-dotenv pyyaml fs tabulate
```

3. `.env` 파일 생성 및 Notion API 토큰 설정

```
NOTION_TOKEN=your_notion_integration_token
# 선택 사항: 설정 파일 경로 지정 (기본값: 프로젝트 루트의 notion-hugo.config.yaml)
# NOTION_HUGO_CONFIG=/path/to/your/config.yaml
```

## 초기 설정

### Notion 데이터베이스 설정

#### 워크스페이스 루트에 데이터베이스 생성

```bash
python notion_hugo_app.py --setup-db --db-name="Hugo Blog Posts"
```

#### 특정 페이지 아래에 데이터베이스 생성

```bash
python notion_hugo_app.py --setup-db --parent-page=YOUR_PAGE_ID --db-name="Hugo Blog Posts"
```

#### 옵션

- `--parent-page`: 데이터베이스를 생성할 상위 노션 페이지 ID (선택 사항)
- `--db-name`: 생성할 데이터베이스 이름 (기본값: "Hugo Blog Posts")
- `--target-folder`: 콘텐츠 대상 폴더 (기본값: "posts")

### 기존 데이터베이스 마이그레이션

#### 워크스페이스 루트로 마이그레이션

```bash
python notion_hugo_app.py --migrate-db --source-db=SOURCE_DB_ID
```

#### 특정 페이지로 마이그레이션

```bash
python notion_hugo_app.py --migrate-db --source-db=SOURCE_DB_ID --parent-page=TARGET_PAGE_ID
```

#### 옵션

- `--source-db`: 소스 데이터베이스 ID (필수)
- `--parent-page`: 새 데이터베이스를 생성할 상위 노션 페이지 ID (선택 사항)
- `--target-folder`: 콘텐츠 대상 폴더 (기본값: "posts")

### 수동 설정

`notion-hugo.config.yaml` 파일에 Notion 데이터베이스와 페이지를 수동으로 설정할 수 있습니다:

```yaml
mount:
  manual: true
  databases:
    - database_id: "your_database_id"
      target_folder: "posts"
  # 개별 페이지 지정
  # pages:
  #   - page_id: "your_page_id"
  #     target_folder: "pages"
```

또는 단일 Notion 페이지에서 하위 데이터베이스와 페이지를 자동으로 가져오도록 설정:

```yaml
mount:
  manual: false
  page_url: "https://www.notion.so/your-workspace/your-page-id"
```

## 파이프라인 실행

### 전체 파이프라인 실행

기본 명령어로 Notion 페이지 가져오기 및 Hugo 빌드까지 모두 실행:

```bash
python notion_hugo_app.py
```

### 증분 처리 옵션

#### 변경된 페이지만 처리 (기본값)

```bash
python notion_hugo_app.py --incremental
```

#### 모든 페이지 강제 재처리

```bash
python notion_hugo_app.py --full-sync
```

#### 변경사항만 확인 (실제 변환 없음)

```bash
python notion_hugo_app.py --dry-run
```

#### 메타데이터 파일 경로 지정

```bash
python notion_hugo_app.py --state-file=/path/to/your/state.json
```

### 기타 실행 옵션

```bash
# Notion 변환만 실행
python notion_hugo_app.py --notion-only

# Hugo 전처리 및 빌드만 실행
python notion_hugo_app.py --hugo-only

# 빌드 단계 건너뛰기
python notion_hugo_app.py --no-build

# Hugo에 추가 인자 전달 (예: 서버 실행)
python notion_hugo_app.py --hugo-args="server -D"
```

## Docker 환경

### 기본 사용법

```bash
# 환경 변수 설정 (.env 파일에 NOTION_TOKEN 설정)
echo "NOTION_TOKEN=your_notion_token" > .env

# 개발 서버 실행
docker-compose up

# 백그라운드에서 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서버 중지
docker-compose down
```

### Docker 환경 변수

`docker-compose.yml` 파일에서 다음 환경 변수를 설정할 수 있습니다:

- `NOTION_TOKEN`: Notion API 토큰 (필수)
- `HUGO_ENVIRONMENT`: Hugo 환경 (기본값: development)
- `HUGO_ENABLEGITINFO`: Git 정보 활성화 (기본값: true)

### Docker 고급 옵션

```bash
# 특정 명령어로 실행 (예: 증분 처리 비활성화)
docker-compose run --rm notion-hugo --full-sync

# 테스트 모드 실행
docker-compose run --rm notion-hugo --dry-run

# Hugo 서버 옵션 변경
docker-compose run --rm notion-hugo --hugo-args="server --minify --disableFastRender"

# 다른 메타데이터 파일 사용
docker-compose run --rm notion-hugo --state-file=custom-state.json
```

## 주요 기능

### Notion 데이터베이스 관리

- 노션 워크스페이스 루트 또는 특정 페이지에 데이터베이스 자동 생성
- 샘플 블로그 포스트 자동 생성으로 빠른 시작
- 기존 데이터베이스에서 Hugo 호환 형식으로 마이그레이션
- 타입 검증 및 속성 자동 변환

### 증분 처리 시스템

- JSON 기반 메타데이터 저장으로 변경된 페이지만 처리
- 페이지의 `last_edited_time`을 추적하여 변경사항 감지
- 진행 상황 상세 로깅 및 통계 제공
- 고아 파일 자동 정리 (더 이상 존재하지 않는 페이지)

### Notion 블록 지원

- 단락, 제목, 목록, 할 일 목록, 토글, 코드 블록, 인용, 구분선, 이미지
- 테이블, 컬럼, 임베드, 북마크, 외부 파일
- 중첩 블록 지원 (토글 안의 목록 등)
- Notion 프론트매터 자동 변환 (태그, 생성일, 카테고리 등)

### Hugo 전처리 및 빌드

- 빌드 오류가 발생할 수 있는 파일 자동 감지 및 처리
- 오류 로그 생성 및 문제 파일 추적
- shortcode 지원 및 검증
- 증분 빌드 지원 (변경된 파일만 처리)

## 프로젝트 구조

```
notion-hugo-py/
├── src/
│   ├── config.py          # 설정 관리
│   ├── file.py            # 파일 처리
│   ├── helpers.py         # 유틸리티 함수
│   ├── hugo_processor.py  # Hugo 전처리 및 빌드 관리
│   ├── index.py           # Notion 변환 로직
│   ├── markdown_converter.py # 마크다운 변환
│   ├── metadata.py        # 증분 처리 메타데이터 관리
│   ├── notion_api.py      # Notion API 통합
│   ├── notion_hugo.py     # 통합 파이프라인
│   ├── notion_setup.py    # 노션 DB 설정 및 마이그레이션
│   ├── render.py          # 렌더링 로직
│   └── types.py           # 타입 정의
├── data/
│   └── error_temp/        # 문제 파일 임시 보관소
├── docs/
│   ├── build_errors.json  # 빌드 오류 로그
│   └── development_logs/  # 개발 로그
├── .notion-hugo-state.json # 증분 처리 메타데이터
├── docker-compose.yml     # Docker 설정
├── Dockerfile             # Docker 빌드 설정
├── notion_hugo_app.py     # 메인 실행 파일
└── notion-hugo.config.yaml # 설정 파일
```

## 문제 해결

### Notion API 오류

- Notion 통합 토큰이 올바르게 설정되었는지 확인하세요.
- 통합에 필요한 권한이 부여되었는지 확인하세요.
- 데이터베이스 ID와 페이지 ID가 올바른지 확인하세요.

### 증분 처리 관련 문제

- 메타데이터 파일(`.notion-hugo-state.json`)이 손상된 경우, 파일을 삭제하고 `--full-sync` 옵션으로 재실행하세요.
- 동기화 일관성 문제가 발생하면 `--full-sync` 옵션을 사용하여 모든 페이지를 다시 처리하세요.
- 충돌 문제가 발생하면 백업 파일(`.notion-hugo-state.json.bak`)을 확인하세요.

### Hugo 빌드 오류

- Hugo가 시스템에 설치되어 있는지 확인하세요.
- Hugo 테마가 올바르게 설치되었는지 확인하세요.
- 문제 파일은 `docs/build_errors.json`에서 확인할 수 있습니다.

### Docker 관련 문제

#### 포트 충돌

이미 1313 포트가 사용 중인 경우, `docker-compose.yml` 파일에서 포트 매핑을 변경하세요:

```yaml
ports:
  - "1314:1313" # 호스트의 1314 포트를 컨테이너의 1313 포트에 매핑
```

#### 권한 문제

볼륨 마운트에서 권한 문제가 발생할 경우, Docker를 실행하는 사용자가 프로젝트 디렉토리에 대한 적절한 권한을 가지고 있는지 확인하세요.

#### 메타데이터 파일 접근 문제

Docker 볼륨 설정이 메타데이터 파일(`.notion-hugo-state.json`)을 마운트하는지 확인하세요. `docker-compose.yml` 파일에 다음 설정이 있어야 합니다:

```yaml
volumes:
  - ./:/app
  - ./.notion-hugo-state.json:/app/.notion-hugo-state.json
```

## 라이선스

GPL-3.0
