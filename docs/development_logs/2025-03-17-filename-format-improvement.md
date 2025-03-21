# 파일명 형식 개선 (2025-03-17)

## 개요

Notion 페이지를 마크다운 파일로 변환할 때 사용되는 파일명 형식을 개선하고, 사용자가 원하는 형식을 선택할 수 있는 설정 옵션을 추가했습니다.

## 변경 사항

### 1. 파일명 형식 설정 옵션 추가

`notion-hugo.config.yaml` 파일에 새로운 `filename` 섹션을 추가하여 파일명 형식을 설정할 수 있습니다:

```yaml
filename:
  # 파일명 형식: "uuid", "title", "date-title"
  format: "date-title"
  # 날짜 형식: 표준 Python 날짜 형식 문자열
  date_format: "%Y-%m-%d"
  # 한글 제목 처리: "as-is" (그대로 사용), "slug" (슬러그화만)
  korean_title: "slug"
```

### 2. 파일명 생성 로직 구현

다음 세 가지 파일명 형식을 지원합니다:

1. **uuid**: 기존 방식처럼 Notion 페이지 ID를 파일명으로 사용
2. **title**: 페이지 제목을 파일명으로 사용
3. **date-title**: 날짜와 제목을 조합 (예: `2025-03-17-getting-started.md`)

### 3. 한글 제목 처리 옵션

한글이 포함된 제목의 처리 방식을 설정할 수 있습니다:

- **as-is**: 한글을 그대로 사용
- **slug**: 특수문자 제거 및 공백을 하이픈으로 변환

### 4. 마이그레이션 기능 개선

마이그레이션 도구가 파일명 형식 설정을 유지하고 업데이트하도록 개선했습니다.

## 상세 변경 내역

### 파일 생성

- `src/utils/file_utils.py`: 파일명 생성 유틸리티 함수 구현
- `docs/filename-format-guide.md`: 상세 사용 가이드 작성

### 파일 수정

- `src/config.py`: 파일명 설정을 로드하는 기능 추가
- `src/render.py`: 새 파일명 생성 로직 적용
- `src/notion_setup.py`: 마이그레이션 기능 개선
- `notion-hugo.config.yaml`: 파일명 설정 옵션 추가

## 사용 방법

기존의 앱 실행 방식과 동일하게 사용할 수 있습니다. 설정에 따라 파일명이 자동으로 생성됩니다:

```bash
# 평소대로 실행
python notion_hugo_app.py

# 모든 페이지를 새 파일명 형식으로 업데이트하려면
python notion_hugo_app.py --full-sync
```

## 향후 개선 계획

1. 영문 변환 기능: 한글 제목을 영문으로 자동 변환하는 기능 추가
2. 더 다양한 파일명 템플릿 지원
3. 기존 파일명에서 새 파일명으로의 자동 마이그레이션 도구
