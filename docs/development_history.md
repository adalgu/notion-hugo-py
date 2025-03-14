# Notion-Hugo 통합 파이프라인 개발 로그

이 문서는 Notion-Hugo 통합 파이프라인 프로젝트의 개발 로그 및 변경 사항을 목록화한 인덱스입니다.
각 링크는 해당 개발 단계의 상세 로그로 연결됩니다.

## 개발 로그

### 2025-03-14

- [통합 파이프라인 구현](./development_logs/2025-03-14-integration.md): Notion 변환 기능과 Hugo 전처리 기능을 통합한 완전한 파이프라인 구현
- [노션 DB 자동 설정 및 마이그레이션 기능 추가](./development_logs/2025-03-14-db-setup.md): 노션 데이터베이스 자동 설정 및 마이그레이션 기능 추가

## 개요

Notion-Hugo 통합 파이프라인은 Notion을 CMS로 사용하여 작성한 콘텐츠를 Hugo 정적 사이트 생성기에 자동으로 연결하는 도구입니다.
이 프로젝트는 다음과 같은 핵심 기능을 제공합니다:

1. Notion 데이터베이스 자동 설정 및 마이그레이션
2. Notion API를 통한 콘텐츠 가져오기
3. 마크다운 변환 및 Hugo 호환 처리
4. Hugo 전처리 및 빌드 자동화
5. 오류 처리 및 복구 메커니즘

## 주요 기능

- Notion 데이터베이스에서 콘텐츠 가져오기
- 마크다운으로 변환 및 Hugo 콘텐츠 저장
- Hugo 전처리를 통한 빌드 오류 방지
- Hugo 빌드 및 서버 실행
- 노션 데이터베이스 자동 설정 및 샘플 콘텐츠 생성
- 기존 노션 데이터베이스에서 마이그레이션

## 사용 방법

기본 사용 방법:

```bash
# 전체 파이프라인 실행
python notion_hugo_app.py

# 새 데이터베이스 설정
python notion_hugo_app.py --setup-db --parent-page=YOUR_PAGE_ID

# 기존 데이터베이스 마이그레이션
python notion_hugo_app.py --migrate-db --source-db=SOURCE_DB_ID --parent-page=TARGET_PAGE_ID
```
