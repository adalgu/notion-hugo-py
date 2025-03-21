# 노션-휴고 속성 매핑 시스템 개선

**날짜:** 2025년 3월 17일

## 개요

노션 데이터베이스 속성과 Hugo 프론트매터 간의 매핑 시스템을 전면 개선했습니다. 기존 단순한 매핑 구조에서 보다 체계적이고 확장 가능한 시스템으로 업그레이드하였습니다.

## 주요 변경 사항

### 1. 속성 체계 개선

속성 구분을 사용자 관점에서 보다 직관적으로 재구성했습니다:

#### 기존 구조
- 필수 속성 (Required Properties)
- 선택적 속성 (Optional Properties)
- 특수 속성 (Special Properties)

#### 새 구조
- 최소한 속성 (Minimal Properties)
  - 블로그 게시에 필수적인 기본 속성, 이것만 있어도 발행 가능
- 추천 속성 (Recommended Properties)
  - 콘텐츠 제어 속성: skipRendering, isPublished, expiryDate 등
  - 메타데이터 속성: description, summary, lastModified, slug 등
  - 분류 속성: categories, tags, keywords 등
  - 테마 지원 속성: featured, subtitle, linkTitle, layout 등

### 2. 새로운 프로퍼티 추가

Hugo 프론트매터의 공식 문서를 참고하여 아래 속성들을 새롭게 추가했습니다:

- **summary**: 콘텐츠 요약 (description이 있으면 그 값을 기본값으로 사용)
- **keywords**: SEO 키워드 (tags가 있으면 그 값을 기본값으로 사용)
- **lastModified**: 마지막 수정일 (notio
n의 last_edited_time 자동 매핑)
- **expiryDate**: 만료일 (이후에는 사이트에서 제거)
- **weight**: 페이지 정렬 순서
- **linkTitle**: 링크용 짧은 제목
- **layout**: 사용할 템플릿 레이아웃

### 3. 속성 명칭 변경

몇 가지 속성의 이름을 보다 직관적으로 변경했습니다:

- **doNotRendering** → **skipRendering**
  - "렌더링하지 않음"보다 "렌더링 건너뛰기"가 행동을 명확히 표현
  - 노션→마크다운 변환 단계에서 건너뛰는 작업임을 명확히 함

### 4. 불필요한 중복 속성 제거

- **category** 속성 제거: Hugo 프론트매터의 `categories`와 일치시키기 위해 복수형 **categories**만 유지
- **draft** 속성 제거: **isPublished**와 역의 관계로 사용자 관점에서 하나만 노출 (내부적으로는 draft로 변환)

### 5. fallback 메커니즘 개선

데이터가 부족할 때 자동으로 대체값을 사용하는 메커니즘을 강화했습니다:

- **summary** ← description (설명을 요약으로 사용)
- **keywords** ← tags (태그를 SEO 키워드로 사용)
- **lastmod** ← last_edited_time (시스템 수정시간 사용)
- **date** ← created_time (발행일이 없으면 생성시간 사용)

## 코드 변경 내용

### 1. PropertyMapper 클래스 전면 개편

- 속성 그룹을 더 명확히 구분하고 처리 로직 개선
- fallback 로직을 별도 메서드로 분리하여 확장성 향상
- 콘텐츠 제어 속성(skipRendering, isPublished) 처리 개선

### 2. 노션 DB 템플릿 업데이트

- 새로운 속성 구조를 반영한 데이터베이스 속성 정의
- 샘플 포스트에 새로운 속성들 추가하여 사용법 시연
- 자주 사용되는 테마별 속성들 추가

### 3. 문서화 개선

- README.md에 상세한 속성 매핑 테이블 추가
- 각 속성 그룹별로 설명 제공
- 테마 의존적인 속성들 명확히 구분

## 마이그레이션 고려사항

기존 doNotRendering 속성은 하위 호환성을 위해 계속 지원합니다. PropertyMapper 클래스의 should_skip_page 메서드에서 skipRendering과 doNotRendering 둘 다 확인하도록 구현되어 있습니다.

## 향후 개선 방향

1. 테마별 지원 속성 세트 구성
   - 각 Hugo 테마마다 지원하는 특수 속성 목록 제공
   - 테마별 프리셋 선택 기능 추가

2. 속성 유효성 검증 강화
   - 날짜 형식 검증
   - 필수 속성 누락 시 경고

3. 노션 UI에서 속성 설명 제공
   - 노션 DB 속성에 설명 추가하여 사용자 안내
