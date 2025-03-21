---
title: "숏코드 구현 (adsense, staticref 등)"
date: 2025-03-17T09:36:00+09:00
---

## 문제 상황

Hugo 빌드 과정에서 다음과 같은 오류가 발생했습니다:

```
Error: error building site: process: readAndProcessContent: "/content/posts/1b87522e-eb2f-812e-98e3-ecc6d8ebebc1.md:58:1": failed to extract shortcode: template for shortcode "adsense" not found
Error: error building site: process: readAndProcessContent: "/content/posts/1b87522e-eb2f-8144-806a-dde50eda3601.md:25:1": failed to extract shortcode: template for shortcode "adsense" not found
Error: error building site: process: readAndProcessContent: "/content/posts/1b87522e-eb2f-8190-80d7-f9fe4b00b50b.md:11:1": failed to extract shortcode: template for shortcode "staticref" not found
```

이전 테마에서 사용하던 숏코드가 현재 Hugo 사이트에 구현되어 있지 않아서 빌드 오류가 발생했습니다.

## 해결 방법

다음 숏코드들을 구현하여 문제를 해결했습니다:

1. **adsense.html**: 구글 애드센스 광고를 게시물 내에 삽입하기 위한 숏코드
2. **staticref.html**: static 폴더의 파일을 링크로 참조하기 위한 숏코드
3. **ref.html / relref.html**: 다른 문서를 참조하는 링크 생성 숏코드
4. **추가 숏코드**: 관련 오류를 해결하기 위해 다음 숏코드도 구현했습니다
   - video.html: 로컬 비디오 파일을 삽입하기 위한 숏코드
   - gdocs.html: 구글 문서를 삽입하기 위한 숏코드
   - tweet.html: 트위터 게시물을 삽입하기 위한 숏코드
   - list_tags.html: 태그 목록을 제공하는 숏코드
   - list_categories.html: 카테고리 목록을 제공하는 숏코드

## 구현 상세

### adsense.html
```html
<!-- Google AdSense 광고 코드 -->
<div class="adsense-container">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="ca-pub-YOUR_AD_CLIENT_ID"
       data-ad-slot="YOUR_AD_SLOT"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>
       (adsbygoogle = window.adsbygoogle || []).push({});
  </script>
</div>
```

### staticref.html
```html
{{ $path := .Get 0 }}
{{ $target := .Get 1 }}
<a href="{{ .Site.BaseURL }}{{ $path }}" {{ if eq $target "newtab" }}target="_blank" rel="noopener"{{ end }}>
  {{ .Inner }}
</a>
```

### ref.html / relref.html
```html
{{ $targetPath := .Get 0 }}
{{ if $targetPath }}
  {{ $permalink := "" }}
  {{ $fallbackURL := "/" }}
  
  {{ $err := "" }}
  {{ $permalink, $err = partial "safe-ref.html" (dict "Page" $ "Target" $targetPath) }}
  
  {{ if ne $err "" }}
    <!-- 페이지를 찾을 수 없으면 기본 홈 페이지 URL 반환 -->
    {{ $fallbackURL }}
  {{ else }}
    {{ $permalink }}
  {{ end }}
{{ else }}
  {{ errorf "Missing target path in ref shortcode. Example usage: {{< ref \"post/my-post.md\" >}}" }}
{{ end }}
```

## 결과

모든 필요한 숏코드를 구현하여 이제 Hugo 빌드가 정상적으로 진행됩니다. 

### 링크 참조 오류 해결

마이그레이션 과정에서 페이지 슬러그가 변경되어 발생하는 참조 오류(REF_NOT_FOUND)를 해결하기 위해 `safe-ref.html`과 `safe-relref.html` 파셜을 추가로 구현했습니다. 이 수정을 통해:

1. 참조된 페이지가 존재하지 않을 경우 기본 홈페이지('/')로 연결됩니다.
2. 기존 코드를 수정하지 않고도 오류 없이 사이트가 빌드됩니다.

앞으로 필요한 경우 추가 숏코드 구현이나 기존 코드 개선이 필요할 수 있습니다.
