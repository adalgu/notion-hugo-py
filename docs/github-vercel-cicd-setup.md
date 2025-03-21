# GitHub Actions & Vercel CI/CD 설정 가이드

이 문서는 Notion-Hugo 프로젝트의 GitHub Actions와 Vercel CI/CD 자동화 설정 방법을 설명합니다.

## 현재 설정 상태

- ✅ GitHub 저장소와 Vercel 프로젝트 연결 완료
- ✅ GitHub Actions 워크플로우 파일 `.github/workflows/notion-sync.yml` 생성 완료
- ❌ GitHub Secrets에 Notion API 토큰 추가 필요

## GitHub Secrets 설정 방법

GitHub Actions 워크플로우에서 Notion API에 접근하려면 다음 방법 중 하나로 시크릿을 설정할 수 있습니다:

### 방법 1: GitHub CLI 사용 (권장)

GitHub CLI를 사용하면 명령줄에서 직접 시크릿을 설정할 수 있습니다:

```bash
# .env 파일에서 NOTION_TOKEN 값을 읽어 GitHub 시크릿으로 설정
gh secret set NOTION_TOKEN --body "$(grep NOTION_TOKEN .env | cut -d '=' -f2)"

# 또는 직접 값을 입력할 수도 있습니다
gh secret set NOTION_TOKEN
# 프롬프트가 표시되면 값 입력
```

### 방법 2: GitHub 웹 인터페이스 사용

1. GitHub 저장소 페이지로 이동합니다: https://github.com/adalgu/notion-hugo-py
2. 저장소 상단 메뉴에서 "Settings" 탭을 클릭합니다
3. 왼쪽 사이드바에서 "Secrets and variables" → "Actions"를 클릭합니다
4. "New repository secret" 버튼을 클릭합니다
5. 다음 정보를 입력합니다:
   - Name: `NOTION_TOKEN`
   - Secret: `.env` 파일의 NOTION_TOKEN 값을 붙여넣습니다
6. "Add secret" 버튼을 클릭하여 저장합니다

## 작동 방식

완전한 CI/CD 파이프라인은 다음과 같이 작동합니다:

1. **자동 또는 수동 트리거**:
   - 자동: 6시간마다 GitHub Actions 워크플로우 실행
   - 수동: GitHub 저장소의 Actions 탭에서 "Notion to Hugo Sync" 워크플로우 실행

2. **Notion 콘텐츠 동기화**:
   - GitHub Actions는 설정된 스케줄이나 수동 트리거에 따라 실행됩니다
   - Notion API를 통해 최신 콘텐츠를 가져와 마크다운으로 변환합니다
   - 변경사항이 있으면 GitHub 저장소에 자동 커밋합니다

3. **Vercel 자동 배포**:
   - GitHub 저장소에 새 커밋이 발생하면 Vercel이 자동으로 빌드와 배포를 시작합니다
   - Vercel은 vercel.json 설정에 따라 Hugo를 사용하여 사이트를 빌드합니다
   - 배포가 완료되면 사이트가 자동으로 업데이트됩니다

## 추가 설정 옵션

### GitHub Actions 워크플로우 스케줄 변경

`.github/workflows/notion-sync.yml` 파일에서 `cron` 표현식을 수정하여 실행 주기를 변경할 수 있습니다:

```yaml
schedule:
  - cron: '0 */6 * * *'  # 6시간마다 실행 (현재 설정)
  # - cron: '0 */12 * * *'  # 12시간마다 실행
  # - cron: '0 0 * * *'  # 매일 자정에 실행
  # - cron: '0 0 * * 1-5'  # 평일 자정에만 실행
```

### Vercel 배포 설정 조정

Vercel 대시보드에서 다음 설정을 확인하고 필요에 따라 조정할 수 있습니다:

1. Production Branch: 배포할 기본 브랜치 설정
2. Framework Preset: Hugo 설정 확인
3. Environment Variables: 필요한 환경 변수 추가

## 문제 해결

### GitHub Actions 워크플로우가 실행되지 않는 경우

- GitHub 저장소의 Actions 탭에서 워크플로우 상태 확인
- `NOTION_TOKEN` 시크릿이 올바르게 설정되었는지 확인
- 워크플로우 로그에서 오류 메시지 확인

### Vercel 배포가 실패하는 경우

- Vercel 프로젝트 대시보드에서 배포 로그 확인
- vercel.json 설정이 올바른지 확인
- 빌드 로그에서 오류 메시지 확인
