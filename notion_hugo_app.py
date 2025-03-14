#!/usr/bin/env python3
"""
Notion-Hugo 통합 애플리케이션

Notion에서 콘텐츠를 가져와 마크다운으로 변환하고, 
Hugo 전처리를 통해 오류 파일을 처리한 후 Hugo 빌드를 실행하는 통합 파이프라인입니다.

실행 방법:
    python notion_hugo_app.py [options]

기본 옵션:
    --notion-only: Notion에서 마크다운 변환만 실행
    --hugo-only: Hugo 전처리 및 빌드만 실행
    --no-build: Hugo 빌드 단계 건너뛰기
    --hugo-args="...": Hugo에 전달할 인자 (예: --hugo-args="server --minify")

증분 처리 옵션:
    --incremental: 변경된 페이지만 처리 (기본값)
    --full-sync: 모든 페이지 강제 재처리
    --state-file=PATH: 메타데이터 파일 위치 (기본값: .notion-hugo-state.json)
    --dry-run: 실제 변환 없이 변경사항만 확인

데이터베이스 설정 옵션:
    --setup-db: 새 노션 데이터베이스 생성 및 설정
    --parent-page=PAGE_ID: 노션 상위 페이지 ID (선택사항, 지정하지 않으면 워크스페이스 루트에 생성)
    --db-name=NAME: 생성할 데이터베이스 이름 (기본값: 'Hugo Blog Posts')
    --target-folder=FOLDER: 컨텐츠 대상 폴더 (기본값: 'posts')

데이터베이스 마이그레이션 옵션:
    --migrate-db: 기존 노션 데이터베이스에서 마이그레이션
    --source-db=DB_ID: 소스 데이터베이스 ID (마이그레이션 시 필요)
    --parent-page=PAGE_ID: 노션 상위 페이지 ID (선택사항, 지정하지 않으면 워크스페이스 루트에 생성)

예시:
    # 워크스페이스 루트에 새 데이터베이스 설정
    python notion_hugo_app.py --setup-db --db-name="My Blog Posts"
    
    # 특정 페이지 아래에 새 데이터베이스 설정
    python notion_hugo_app.py --setup-db --parent-page=123456789abcdef --db-name="My Blog Posts"
    
    # 기존 데이터베이스를 워크스페이스 루트로 마이그레이션
    python notion_hugo_app.py --migrate-db --source-db=123456789abcdef
    
    # 기존 데이터베이스를 특정 페이지로 마이그레이션
    python notion_hugo_app.py --migrate-db --source-db=123456789abcdef --parent-page=987654321fedcba
    
    # 일반 파이프라인 실행
    python notion_hugo_app.py
"""

import sys
import os

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 통합 파이프라인 모듈 임포트
from src.notion_hugo import main

if __name__ == "__main__":
    main()
