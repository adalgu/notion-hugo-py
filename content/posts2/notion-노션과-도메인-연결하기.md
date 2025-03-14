---
title: "[Notion] 노션과 도메인 연결하기"
lastmod: 2025-03-12T02:22:00.000Z
author: "Gunn Kim"
description: ""
notion_id: "736f0e70-d77e-447a-9cb9-a7b85b984c96"
---

```markdown
Hugo blog powered by Notion
(노션으로 휴고 블로그 포스팅 하기)

Hugo로 빌드한 gunn.kim이라는 웹사이트를 운영중이고,
여기에 Notion을 붙여보려고 시도 중. 현재 1단계 진행
~~- (3단계) 노션을 작성한 글이 자동으로 블로그로 빌드되거나, (API+CI/CD)
- (2단계) 노션으로 작성한 글 리스트를 블로그로 볼 수 있거나, (HUGO, 자바 등으로 리스트 구현)~~
- (1단계) 노션 공개 페이지와 도메인 연결 (서버리스 컴퓨팅으로 간단한 코드를 돌려서 연결)

제목처럼 휴고 블로그를 완전히 노션과 붙인 것 3단계인데, 1단계부터 단계적으로 구현해볼 생각.

일단은 클라우드플래어(cloudflare)의 서버리스 컴퓨팅 서비스인 Workders를 이용하여 
notion의 공개 페이지와 도메인을 연결해 보았음.
```


Hugo(Static Site Generator의 하나)로 만든 블로그를 운영 중인데, Notion을 붙여보는 방법을 고민하고 있었다.

- 역시나 세상은 넓고, 비슷한 생각을 하는 사람은 많고, 단순히 생각에 그치지 않고 실행에 옮기고, 구현하는 능력자들이 많다.
- 궁극적으로는 노션에서 작성한 posts가 hugo로 자동으로 build되는 블로그를 고민하고 있는데,


일단은 중간 단계로 노션의 공개 페이지와 도메인을 붙여보는 것을 시도해 보았다.

- notion의 공개 페이지 ↔ https://notion.gunn.kim
- 특정 페이지를 메인 페이지로 해서 서브페이지들을 만들면, 만드는 대로 도메인이 연결된다!
- 참고한 사이트는 아래와 같다.
- [https://romantech.net/1046](https://romantech.net/1046)
- cloudflare의 workers를 이용하는 방법인데,
- 간단한 코드를 실행하여 노션의 공개 페이지를 지정한 도메인으로 지속적으로 포워딩해주는 것으로 이해가 된다.
- 아래 코드를 cloudflare의 Workers에 넣으면 된다. 

```python
# 출처: https://romantech.net/1046 [로맨테크]

const MY_DOMAIN = "서브 도메인 주소"
const START_PAGE = "노션 공개 페이지 주소"
addEventListener('fetch', event => {
event.respondWith(fetchAndApply(event.request))
})
const corsHeaders = {
"Access-Control-Allow-Origin": "*",
"Access-Control-Allow-Methods": "GET, HEAD, POST,PUT, OPTIONS",
"Access-Control-Allow-Headers": "Content-Type",
}
function handleOptions(request) {
if (request.headers.get("Origin") !== null &&
request.headers.get("Access-Control-Request-Method") !== null &&
request.headers.get("Access-Control-Request-Headers") !== null) {
// Handle CORS pre-flight request.
return new Response(null, {
headers: corsHeaders
})
} else {
// Handle standard OPTIONS request.
return new Response(null, {
headers: {
"Allow": "GET, HEAD, POST, PUT, OPTIONS",
}
})
}
}
async function fetchAndApply(request) {
if (request.method === "OPTIONS") {
return handleOptions(request)
}
let url = new URL(request.url)
let response
if (url.pathname.startsWith("/app") && url.pathname.endsWith("js")) {
response = await fetch(`https://www.notion.so${url.pathname}`)
let body = await response.text()
try {
response = new Response(body.replace(/www.notion.so/g, MY_DOMAIN).replace(/notion.so/g, MY_DOMAIN), response)
// response = new Response(response.body, response)
response.headers.set('Content-Type', "application/x-javascript")
console.log("get rewrite app.js")
} catch (err) {
console.log(err)
}
} else if ((url.pathname.startsWith("/api"))) {
response = await fetch(`https://www.notion.so${url.pathname}`, {
body: request.body, // must match 'Content-Type' header
headers: {
'content-type': 'application/json;charset=UTF-8',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
},
method: "POST", // *GET, POST, PUT, DELETE, etc.
})
response = new Response(response.body, response)
response.headers.set('Access-Control-Allow-Origin', "*")
} else if (url.pathname === `/`) {
let pageUrlList = START_PAGE.split("/")
let redrictUrl = `https://${MY_DOMAIN}/${pageUrlList[pageUrlList.length-1]}`
return Response.redirect(redrictUrl, 301)
} else {
response = await fetch(`https://www.notion.so${url.pathname}`, {
body: request.body, // must match 'Content-Type' header
headers: request.headers,
method: request.method, // *GET, POST, PUT, DELETE, etc.
})
}
return response
}
```

- 마치 aws의 람다(lambda)와 비슷한 서버리스 컴퓨팅이나 Gitlab의 CI/CD와 유사한 기반으로 구현되는 것으로 보인다.
- (이후) 워커스를 이용하니 웰컴 메일이 왔는데, 서버리스 앱이라고 명시적으로 해놓았다.
- 점점 더 서버리스관련 서비스들이 더 많이 눈에 띈다.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/730b71a8-106c-4d8b-a757-8eb4edd1c903/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466XUWON43I%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044859Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDPjOGqX3PftOfY1Ie9qzp5WnLrNtepSP9SNoayx41wYAIgfLAYgGOaSl9Q8MrqkAXPANkhqGhi%2FI5sLofdZ%2FsgLhEqiAQI5f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDOGXZApo4Hep0JdWdyrcA%2BLKMVZKr9uhiz%2FkKNYHepA3EBhDvxrF21TJKnuhwKZA%2FByw4ALpd9n%2BJ1u609TFCHGbpwHeGxc%2FYoyJPHZishFHZi9PgtmJhODl83eUdNUKQJZpzHoEG1I15puHqcFu5R%2FOng9w%2FOs2AKp%2BPxp05uFk3qKTobYwnpnXIKK28DlsTdqHWSzVL%2FaUzYJjTZvFEApV8HUIps%2FC6Lr5BDRtijEpKYW5KLiz0HdtaqhaAY7F4Hwdipn9izD4HexBDD4LUuZlAO1oElAa3tVd9rvqP6Y9E50zGTMWPTdw2cOcE4mqPdNZN18IHbqFsYHdNAhz4trCPsk08MYY4nSX8BKpDu3CF%2BhQ5ecMAdWgoG6ohTyN1fcphlf3dtvVqs%2FXV19kZMGVuQ1mRZKSDXAGJLev2VV3vr90LJppRVU04fDEz3JzL%2FVKvRdWwObB2drsfwS2Hsaze06RYdS53dYe2EqdaHQZyhl3oRcN8uR9RDrcXgJxMFGcVeDSiEozS5LJL8Eu7nwzLxCKJIlkwQCHyEKvZzEKexgVp8ClggLAHd0l%2FFvFbIxC1oDYi6xSvzPM%2BHfHN71M6rTJ6iBI5MugfUQp1DikTTELxHkMzGZokmaI0bHWwTlLqa7WIpH538rWMPLMzr4GOqUB4pi6ETK1xYMz8JGDMdUQrghPBmMuKUlQ78Ai1hjKByVxSnpJIrkpignFrDCcDjoSpks8tRxca2pSVNMQUv3HoACxKWj1tsW54exMqqRQgF9QLXY6CBzB1L1hbH4leuA5TcTU6uBKDLmH4Bu%2BH%2FDrNFdax%2FmXBVSSLMC6sRigLAWzZ1nbLdDuarsO7EBBja%2FEBc%2FcMbZh9aiUMd9jqku%2BOh9tRWQX&X-Amz-Signature=498030618d10e3bddd61e887ed75c2a3b44b4073c9b003508d9a4e66745bf59a&X-Amz-SignedHeaders=host&x-id=GetObject)

- 암튼, 위 참고 사이트에서 아주 상세하게 설명을 해주고 있어서, 쉽게 노션과 도메인을 연결할 수 있었다.


앞으로는,

- [https://gunn.kim에](https://gunn.xn--kim-568n/) [https://notion.gunn.kim](https://notion.gunn.xn--kim-568n/) 의 메인 페이지에 올라온 새로운 페이지들 목록을 보여줄 수 있는 기능을 구현해 보고자 한다.
- 그리고, 일부 능력자들이 구현해 놓을 것처럼, 노션에 글을 쓰면 블로그에 바로 포스팅되는 기능도 구현해 보고자 한다.
- [https://blog.kowalczyk.info/article/88aee8f43620471aa9dbcad28368174c/how-i-reverse-engineered-notion-api.html](https://blog.kowalczyk.info/article/88aee8f43620471aa9dbcad28368174c/how-i-reverse-engineered-notion-api.html)
- 위 방법은 노션의 API를 리버스 엔지니어링을 해서 비공식 API 연결 라이브러리를 이용하는 것으로 짐작된다.(자세히는 아직 모르겠다.)
- 노션에서 공식 API를 오픈할 예정이라, 향후에는 공식 API를 이용한 다양한 연계 어플이 나올 것으로 보인다. (personal pro 이상 플랜에서만 지원)
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/4d750c6c-d830-4352-a81b-5e27d459b8a1/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665GDEG6JX%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044901Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIG2KB7y5tibp9zvSMIF5ehJMTdHUGamc8NIKigReLdcxAiATBUJt2g80Sx4HaazPcG7fLxxWO6EZohxj31KyCm87JCqIBAjl%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMixiUWQLQ9PpGoYJ7KtwDOaWxtx%2BsH85uiFuXmlnZc1wtH1H04Ncy2mvSdMk02dkcQPmXWnmbqlnWOUdHCrmAYe4pO4I6VJYaJrBfFSzB9ZxcRjU%2BhyyUhCkJ0b6eOajZmuBgt%2BcQa0gfWBBSVJXqL0etBo9R%2FW7CbdykUyrDSe3GEAYUqgIEXtD9olFnud99Jemf%2FSLHFhZ0RCt%2F7j58gZlCTUrL0OgX8X6wOBaXb7rp4Dg31dHAy0mPblIZtyfe7QcjA5%2F%2FQpuC0kSyf1M2S0bWYvdnzwY1vNUdSr7bToQM24Dnm7n%2BLggSsFrWv%2Fxmk4x%2Byw2e6Casi%2Fwu8sBQQxGeX6c8csFwgCx50TVXCS%2Bnb%2BGxsZY3oxLDMFSo2MrWbfxQPXsdRvkIOGSBjeE0H9zOpVAhdLsPwJjBfpV9jWVL1IxSHux3E8No3lYVZeYfplZIRUIvK33OBdhbjf8M%2Bx5Wz2Ec45pm0WjiEc8Z%2BeSRaZV44agGX%2B3m9NmCF5jxVXdjNEpyq1US8szgn7B4KQwL9m3EYW3WEciAwe5Pb1%2FpwEV1asONAuVfM9K9aaVSInFcd2iYa2TjkK54C2En1SGDJ4paVH7NDbreHGi8HSHx76zjwXn6tRnenNnC4Lg7soLnvEg9HXO3y9wwl83OvgY6pgEWTwgyJSg82joIFf49rA6MD16lNWVPrBgtHPC74EPNOJK9E0irj0yJCTh8HGI%2BK6k%2BFen5QiC8m1VZJafj7JCx36aCUvZ3Qgwdnlcpgtcok%2B6J1FYMOod%2FbNHYkV7ugwx0a3y8o3vvrAX5aPILiuKRIUYBcXbzuJG3DZwD4s45VGmn%2FqzXUQdJgKuzGPE45WNQ58XT%2FnpwHhSJPgt9Ex%2FDJfKbDuOk&X-Amz-Signature=5b1b768ce3768148bbcff9d43484b87009446c27a6223dfefbaf373df734fc9c&X-Amz-SignedHeaders=host&x-id=GetObject)



결과적으로,

- [gunn.kim](http://gunn.kim/)의 about 페이지에도 설명을 해놓았지만, 외장 두뇌 궁극적 버전의 prototype이 나올 수 있을 것으로 보인다.
- 정보를 오거나이징하고 퍼블리쉬함으로써 뇌를 비우고, 뇌를 아끼는 방법!


