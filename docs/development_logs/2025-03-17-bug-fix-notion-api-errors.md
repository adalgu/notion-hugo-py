# Notion API 오류 및 메타데이터 파일 문제 해결

- **날짜**: 2025-03-17
- **작성자**: Gunn Kim
- **관련 이슈**: N/A
- **이전 로그**: [데이터베이스 설정](./2025-03-14-db-setup.md)

## 문제 상황

Notion-Hugo 프로젝트에서 다음과 같은 여러 오류가 발생했습니다:

1. Notion API를 통한 워크스페이스 루트에 데이터베이스 생성 시 다음 오류 발생:
   ```
   body.parent.page_id should be defined, instead was `undefined`.
   body.parent.database_id should be defined, instead was `undefined`.
   ```

2. 페이지 처리 중 NoneType 오류 발생:
   ```
   [Error] 페이지 처리 실패: 'NoneType' object has no attribute 'encode'
   ```

3. 메타데이터 파일 문제:
   ```
   [Warn] 메타데이터 파일 손상: [Errno 21] Is a directory: '.notion-hugo-state.json', 새로 생성합니다
   [Error] 메타데이터 저장 실패: [Errno 21] Is a directory: '.notion-hugo-state.json.tmp' -> '.notion-hugo-state.json'
   ```

4. 파라미터 불일치 문제:
   ```
   [Error] 페이지 저장 중 오류 발생: string indices must be integers
   ```

## 해결 전략

1. **Notion API 문제**: Notion API가 더 이상 직접 워크스페이스 루트에 생성하는 것을 지원하지 않아, 워크스페이스 내 접근 가능한 페이지를 검색한 후 그 페이지 아래에 데이터베이스를 생성하도록 변경

2. **메타데이터 파일 문제**: `.notion-hugo-state.json`이 디렉토리로 생성되어 있어 이를 삭제하고 파일로 대체

3. **NoneType 오류**: `compute_content_hash` 함수에 None 값 처리 로직 추가

4. **함수 파라미터 문제**: 
   - `save_page` 함수가 mount 객체 대신 target_folder 문자열을 받도록 수정
   - `batch_process_pages_with_metadata` 함수도 이에 맞게 수정

## 구현 세부사항

### 1. Notion API 문제 수정

`src/notion_setup.py` 파일에서 워크스페이스 루트에 데이터베이스 생성 로직을 변경했습니다:

```python
# 워크스페이스 루트에 생성하려면 사용자의 워크스페이스 루트 페이지 ID가 필요함
# Notion API는 더 이상 직접적인 parent={"type": "workspace"}를 지원하지 않음
print("워크스페이스 루트에 데이터베이스 생성 중...")
try:
    # 먼저 사용자의 루트 페이지 가져오기 시도
    search_results = self.notion.search(
        query="",
        filter={
            "value": "page",
            "property": "object"
        },
        page_size=10
    )
    root_pages = search_results.get("results", [])
    
    if not root_pages:
        raise ValueError("워크스페이스 루트 페이지를 찾을 수 없습니다. "
                        "--parent-page 옵션을 사용하여 특정 페이지 ID를 지정하세요.")
    
    # 첫 번째 페이지를 루트 페이지로 사용
    root_page_id = root_pages[0]["id"]
    
    # 선택한 페이지에 데이터베이스 생성
    database = self.notion.databases.create(
        parent={"type": "page_id", "page_id": root_page_id},
        title=title,
        properties=properties
    )
```

### 2. 메타데이터 파일 문제 해결

`.notion-hugo-state.json` 디렉토리를 삭제하고 파일로 대체했습니다:

```bash
rm -rf .notion-hugo-state.json
```

### 3. NoneType 오류 수정

`src/metadata.py` 파일에서 `compute_content_hash` 함수 수정:

```python
def compute_content_hash(self, content: str) -> str:
    """
    콘텐츠 해시 계산
    
    Args:
        content: 해시를 계산할 콘텐츠
        
    Returns:
        SHA-256 해시값
    """
    if content is None:
        content = ""
    
    if not isinstance(content, str):
        content = str(content)
        
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
```

### 4. 함수 파라미터 문제 수정

`src/render.py` 파일에서 `save_page` 함수 수정:

```python
def save_page(page: Dict[str, Any], notion: Client, target_folder: str) -> Optional[str]:
    """
    Notion 페이지를 마크다운 파일로 저장합니다.
    
    Args:
        page: Notion 페이지 객체
        notion: Notion API 클라이언트
        target_folder: 대상 폴더 이름
        
    Returns:
        저장된 콘텐츠 또는 None (오류 발생 시)
    """
    # ...코드 생략...
```

`src/notion_hugo.py` 파일에서 `batch_process_pages_with_metadata` 함수 수정:

```python
# 페이지 처리 (수정된 save_page 함수는 target_folder를 받음)
content = save_page(page, notion, target_folder)
```

## 기술적 고려사항

1. **Notion API 변경 사항**: Notion API는 계속 진화하고 있으며, 이전에는 작동하던 기능이 변경될 수 있습니다. 특히 workspace 루트 접근 권한이 제한되어 있어 이제는 항상 특정 페이지나 데이터베이스를 부모로 지정해야 합니다.

2. **메타데이터 관리**: 메타데이터 파일이 디렉토리로 생성되는 원인은 명확하지 않지만, 파일 시스템 작업 시 항상 디렉토리와 파일 충돌에 대한 검사가 필요합니다.

3. **타입 안전성**: Python은 동적 타입 언어이지만, 타입 힌트와 적절한 검사를 통해 런타임 타입 오류를 방지할 수 있습니다. None 처리와 같은 방어적 코딩 기법이 필요합니다.

## 5. 한글 유니코드 이스케이프 시퀀스 문제 해결

노션에서 가져온 한글 제목이 다음과 같이 유니코드 이스케이프 시퀀스로 변환되는 문제가 발생했습니다:

```yaml
title: "\uC2DC\uC791\uD558\uAE30 - \uCCAB \uBC88\uC9F8 \uBE14\uB85C\uADF8 \uD3EC\uC2A4\
  \uD2B8"
```

### 원인 분석

`src/render.py` 파일의 `save_page` 함수에서 YAML 프론트매터를 생성할 때 `yaml.dump()` 함수를 사용합니다. 기본적으로 Python의 YAML 라이브러리는 비 ASCII 문자(한글 등)를 유니코드 이스케이프 시퀀스로 변환합니다.

### 구현 수정

`yaml.dump()` 호출에 `allow_unicode=True` 옵션을 추가하여 한글 문자가 그대로 유지되도록 수정했습니다:

```python
# 변경 전
frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)

# 변경 후
frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
```

### 결과

이제 생성된 마크다운 파일에서 한글이 올바르게 표시됩니다:

```yaml
title: "시작하기 - 첫 번째 블로그 포스트"
```

이 변경으로 노션에서 가져온 한글 제목이 Hugo 마크다운 파일에 유니코드 이스케이프 시퀀스가 아닌 원래 한글 문자로 저장됩니다. 이로써 마크다운 파일을 직접 편집할 때도 한글 제목을 쉽게 읽고 수정할 수 있게 되었습니다.

## 6. 코드베이스 정리 (중복 파일 제거)

프로젝트 루트 디렉토리에서 불필요하거나 중복된 파일들을 정리했습니다:

1. **main.py** - 삭제
   - `notion_hugo_app.py`와 기능이 중복됨
   - 기본적인 Notion-Hugo 변환 기능만 제공하며, 이미 `src` 폴더 내 모듈에 통합됨

2. **test.py** - 삭제
   - 테스트 목적의 파일로, `main.py`와 유사한 기능 수행
   - 메인 파이프라인이 이미 잘 구현되어 있어 불필요

3. **run_hugo.py** - 삭제
   - `hugo_preprocess.py`를 로드하여 사용하는 래퍼 스크립트
   - 이 기능은 이미 `src/notion_hugo.py`의 `run_hugo_pipeline()` 함수에서 `HugoProcessor` 클래스를 통해 구현됨

4. **hugo_preprocess.py** - 삭제
   - Hugo 빌드 전 오류 파일 처리 기능 담당
   - `src/hugo_processor.py`에 동일한 기능이 구현되어 있어 중복

### 코드베이스 정리 이점

- 프로젝트 구조가 더 깔끔해지고 직관적으로 변경됨
- 유지보수가 용이해짐 (여러 위치에 분산된 동일 기능 코드 제거)
- `notion_hugo_app.py`를 유일한 메인 진입점으로 표준화
- 모든 핵심 기능을 `src` 디렉토리 내에 구조화하여 모듈성 향상

## 다음 단계

1. 통합 테스트 추가: 다양한 Notion 페이지 구조에 대한 테스트 케이스 작성

2. 오류 로깅 개선: 디버그 정보를 좀 더 상세하게 기록하여 문제 분석 용이성 증대

3. 문서 업데이트: 사용자 가이드에 API 권한 및 데이터베이스 생성 관련 정보 추가

4. 예외 처리 강화: 메타데이터 파일 검증 및 오류 복구 기능 추가

5. 코드 리팩토링: 중복된 기능 통합 및 모듈 구조 개선 (루트 디렉토리 정리 이후)

## 참고 자료

- [Notion API 문서](https://developers.notion.com/reference/intro)
- [Python 예외 처리 가이드](https://docs.python.org/3/tutorial/errors.html)
- [Python 파일 시스템 작업](https://docs.python.org/3/library/os.path.html)
