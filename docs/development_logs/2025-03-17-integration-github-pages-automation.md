# [GitHub Pages 배포 자동화 설정]

- **날짜**: 2025-03-17
- **작성자**: Gunn.kim
- **관련 이슈**: 없음
- **이전 로그**: [GitHub Actions & Vercel CI/CD 설정](./2025-03-17-integration-github-vercel-cicd-setup.md)

## 문제 상황
Notion-Hugo 프로젝트를 GitHub Pages에 배포하는 과정을 자동화할 필요가 있었습니다. 수동으로 설정하는 과정은 복잡하고, 오류가 발생하기 쉬우며, 반복적인 작업을 요구했습니다.

## 해결 전략
배포 과정을 자동화하기 위해 `scripts/github-pages-setup.sh` 셸 스크립트를 작성했습니다. 이 스크립트는 GitHub 저장소 생성, 코드 푸시, GitHub Pages 활성화, Notion API 토큰 설정, GitHub Actions 워크플로우 실행까지의 모든 과정을 자동화하여 사용자가 한 번의 명령으로 배포를 완료할 수 있도록 지원합니다.

## 구현 세부사항
### 1. 자동화 스크립트 (`github-pages-setup.sh`)
- **사전 요구사항 검사**: `git`과 `gh` (GitHub CLI)가 설치되어 있고, 사용자가 `gh`에 로그인했는지 확인합니다.
- **환경 설정**: `.env` 파일에서 `NOTION_TOKEN`과 같은 환경 변수를 로드하고, 사용자가 지정하지 않은 경우 GitHub 사용자 이름을 기반으로 저장소 이름을 설정합니다.
- **저장소 관리**: 원격 저장소가 없는 경우 새로 생성하고, 이미 존재하는 경우 사용자에게 충돌 해결 옵션(강제 푸시 등)을 제공합니다.
- **GitHub Pages 활성화**: GitHub API를 호출하여 저장소에 GitHub Pages 기능을 활성화합니다.
- **보안**: `gh secret set` 명령을 사용하여 `NOTION_TOKEN`을 GitHub Actions의 시크릿으로 안전하게 설정합니다.
- **워크플로우 트리거**: 설정이 완료되면, Notion 동기화 및 Hugo 빌드를 위한 GitHub Actions 워크플로우를 수동으로 트리거합니다.

### 2. 수동 설정 가이드
- 스크립트 사용이 어려운 경우를 대비하여, GitHub 웹사이트에서 저장소 생성부터 Actions 실행까지의 전 과정을 수동으로 진행할 수 있는 상세 가이드를 문서에 포함했습니다.

## 기술적 고려사항
- **사용자 편의성**: 스크립트는 대화형 프롬프트를 통해 사용자에게 진행 상황을 알리고, 필요한 경우 선택지를 제공하여 사용자 경험을 향상시켰습니다.
- **오류 처리**: 스크립트 실행 중 발생할 수 있는 일반적인 문제(인증 오류, 토큰 누락, 저장소 충돌 등)에 대한 해결 방법을 문서에 명시하여 사용자가 쉽게 문제를 해결할 수 있도록 했습니다.
- **유연성**: 사용자가 `REPO_NAME` 환경 변수나 명령줄 인수를 통해 원하는 저장소 이름을 지정할 수 있도록 하여 유연성을 높였습니다.

## 다음 단계
- 스크립트에 대한 테스트 케이스를 추가하여 안정성을 높입니다.
- Windows 환경에서의 호환성을 검토하고, 필요한 경우 PowerShell 스크립트를 추가로 제공합니다.

## 참고 자료
- [GitHub Pages 문서](https://docs.github.com/en/pages)
- [GitHub CLI 문서](https://cli.github.com/manual/)
