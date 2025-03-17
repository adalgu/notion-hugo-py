# 마이그레이션 기능 개선 (2025-03-17)

## 개요

Notion-Hugo 앱의 마이그레이션 기능을 개선하여 새로운 파일명 형식 설정을 지원하도록 했습니다. 기존 설정을 보존하면서 새로운 설정을 추가하는 방식으로 구현했습니다.

## 변경 사항

### 1. 설정 파일 관리 개선

마이그레이션 도구가 `notion-hugo.config.yaml` 파일을 처리하는 방식을 개선했습니다:

- 기존 설정 보존: 설정 파일이 이미 존재하는 경우, 내용을 로드하여 기존 설정을 유지
- 데이터베이스 설정 업데이트: 새로운 데이터베이스 정보만 업데이트
- 파일명 형식 설정 자동 추가: 파일명 설정이 없는 경우 기본값 추가

### 2. 마이그레이션 프로세스 개선

`src/notion_setup.py` 파일의 `update_config` 메서드를 다음과 같이 수정했습니다:

```python
def update_config(self, database_id: str, target_folder: str) -> None:
    # 기존 설정 파일이 있으면 로드
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notion-hugo.config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            try:
                config = yaml.safe_load(file) or {}
            except:
                config = {}
    else:
        config = {}
    
    # 마운트 설정 업데이트 또는 생성
    if 'mount' not in config:
        config['mount'] = {...}
    else:
        # 설정 유지하면서 업데이트
        ...
    
    # 파일명 설정 업데이트 또는 생성
    if 'filename' not in config:
        config['filename'] = {
            "format": "date-title",
            "date_format": "%Y-%m-%d",
            "korean_title": "slug"
        }
```

### 3. 설정 충돌 방지

동일한 데이터베이스에 대한 설정이 이미 존재하는 경우, 덮어쓰지 않고 대상 폴더만 업데이트하도록 변경했습니다:

```python
# 동일 데이터베이스가 있는지 확인
db_exists = False
for i, db in enumerate(config['mount'].get('databases', [])):
    if db.get('database_id') == database_id:
        config['mount']['databases'][i]['target_folder'] = target_folder
        db_exists = True
        break

# 없으면 추가
if not db_exists:
    config['mount']['databases'].append({
        "database_id": database_id,
        "target_folder": target_folder
    })
```

## 마이그레이션 기능 사용 방법

마이그레이션 기능은 다음과 같이 사용할 수 있습니다:

### 새 데이터베이스 설정

```bash
python notion_hugo_app.py --setup-db --parent-page PAGE_ID --db-name "My Hugo Blog"
```

### 기존 데이터베이스 마이그레이션

```bash
python notion_hugo_app.py --migrate-db --source-db SOURCE_DB_ID
```

### 대화형 모드

```bash
python notion_hugo_app.py --interactive
```

## 파일명 변경 시 마이그레이션 고려사항

파일명 형식을 변경할 때 고려해야 할 사항들:

1. **기존 파일**: 파일명 형식 변경은 새로 생성되는 파일에만 적용됩니다. 기존 파일은 자동으로 변환되지 않습니다.

2. **강제 재동기화**: 모든 페이지를 새 형식으로 변환하려면 `--full-sync` 옵션을 사용하세요.

3. **내부 링크**: 파일명이 변경되면 내부 링크가 깨질 수 있습니다. Hugo의 단축코드(`ref`, `relref`)를 사용하는 것이 좋습니다.

4. **이전 형식과의 호환성**: 매핑 테이블이나 리디렉션 메커니즘을 구현하는 것을 고려해 볼 수 있습니다.

## 향후 개선 계획

1. **자동 마이그레이션 도구**: 기존 파일을 새 형식으로 자동 변환하고 내부 링크를 업데이트하는 도구
2. **역매핑 지원**: 페이지 ID와 파일명 간의 매핑 테이블 유지
3. **URL 리디렉션**: 기존 URL 경로를 새 URL 경로로 리디렉션하는 메커니즘
