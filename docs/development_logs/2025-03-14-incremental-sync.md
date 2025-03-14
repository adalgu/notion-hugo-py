# 증분 처리 기능 구현

## 개요

노션-휴고 통합 파이프라인에 증분 처리 기능을 추가했습니다. 이 기능은 변경된 페이지만 처리하여 동기화 시간을 크게 단축하고, 불필요한 파일 재생성과 API 호출을 방지합니다.

## 주요 기능

1. **메타데이터 기반 상태 추적**

   - 페이지별 처리 상태 및 수정 시간 추적
   - 콘텐츠 해시값 저장으로 변경 여부 확인
   - 고아 파일 자동 정리

2. **증분 처리 기능**

   - 변경된 페이지만 선택적으로 처리
   - 수정 시간(last_edited_time) 비교
   - 테스트 모드(dry-run) 지원

3. **명령행 인터페이스 개선**
   - `--incremental`: 변경된 페이지만 처리 (기본값)
   - `--full-sync`: 모든 페이지 강제 재처리
   - `--state-file`: 메타데이터 파일 위치 지정
   - `--dry-run`: 실제 변환 없이 변경사항만 확인

## 기술적 구현 내용

### 메타데이터 관리 클래스 (`src/metadata.py`)

```python
class MetadataManager:
    """Notion-Hugo 메타데이터 관리 클래스"""

    def __init__(self, file_path: str = ".notion-hugo-state.json"):
        self.file_path = file_path
        self.metadata = self._load_or_create()

    def get_changed_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """변경된 페이지만 필터링"""
        # 메타데이터 없거나 수정 시간이 다른 페이지만 반환

    def update_page_status(self, page_id: str, **kwargs) -> None:
        """페이지 상태 업데이트"""
        # 처리 결과 메타데이터에 저장
```

### 메타데이터 파일 구조

```json
{
  "last_sync": "2023-03-14T15:30:00Z",
  "version": "1.0",
  "pages": {
    "page_id_1": {
      "last_edited": "2023-03-14T10:15:00Z",
      "processed_at": "2023-03-14T10:30:00Z",
      "hash": "sha256_content_hash",
      "status": "success",
      "target_path": "content/posts/page-title.md"
    }
  }
}
```

### 증분 처리 알고리즘

1. 이전 실행에서 생성된 메타데이터 로드
2. 데이터베이스의 모든 페이지 ID와 `last_edited_time` 값 조회
3. 이전에 처리되지 않았거나 `last_edited_time`이 변경된 페이지만 필터링
4. 필터링된 페이지만 처리하여 마크다운으로 변환
5. 처리 결과를 메타데이터에 저장

### 고아 파일 처리

1. 이전에 처리된 페이지 ID 목록과 현재 페이지 ID 목록 비교
2. 더 이상 존재하지 않는 페이지 ID에 해당하는 파일 삭제
3. 삭제된 페이지 ID를 메타데이터에서도 제거

## 성능 향상

- **API 호출 감소**: 변경된 페이지만 상세 콘텐츠 요청
- **처리 시간 단축**: 재처리가 필요 없는 페이지 건너뛰기
- **디스크 I/O 감소**: 불필요한 파일 쓰기 방지

## 사용 방법

기본적으로 증분 처리가 활성화되어 있어 특별한 설정 없이 최적화된 동기화가 가능합니다:

```bash
# 기본 실행 (증분 처리 활성화)
python notion_hugo_app.py

# 모든 페이지 강제 재처리
python notion_hugo_app.py --full-sync

# 테스트 모드로 변경 사항만 확인
python notion_hugo_app.py --dry-run

# 메타데이터 파일 위치 지정
python notion_hugo_app.py --state-file=.my-state.json
```

## 향후 개선 방향

1. **병렬 처리**: 여러 페이지를 동시에 처리하여 성능 향상
2. **변경 감지 고도화**: 콘텐츠 해시 기반 비교로 API 응답 변경 대응
3. **충돌 해결 메커니즘**: 여러 프로세스가 동시에 실행될 경우 처리
4. **SQLite 기반 상태 관리**: 대규모 사이트용 확장 가능한 상태 저장소
