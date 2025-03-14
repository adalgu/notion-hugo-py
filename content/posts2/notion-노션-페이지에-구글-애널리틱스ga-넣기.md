---
title: "[Notion] 노션 페이지에 구글 애널리틱스(GA) 넣기"
lastmod: 2025-03-12T02:22:00.000Z
author: "Gunn Kim"
description: ""
notion_id: "98f036d8-1869-42f7-8a3b-0b1e5293b306"
---

노션 페이지를 도메인과 연결시키는 것을 해봤으니, 이제 노션 페이지에 구글 애널리틱스를 넣어보자.


구글 애널리틱스는 자바 스크립트를 이용하는 것이 일반적인데, 노션 페이지에선 자바 스크립트를 사용할 수 없다. 이러한 한계를 우회하는 것이 구글 애널리틱스의 Measurement Protocol다.

세상의 많은 능력자분들이 이미 이러한 고민을 했고, 솔루션까지 만들어 내었다.

- 참고한 사이트는 [http://blog.mskim.me/posts/google-analytics-with-notion-so/](http://blog.mskim.me/posts/google-analytics-with-notion-so/)
- [https://romantech.net/1072](https://romantech.net/1072) 는 위 사이트를 참고해서 사용법을 쉽게 설명해 놓았다.


방법은 간단하다. 능력자가 만든 프록시 서버를 이용해서 노션 페이지에 이미지를 삽입하면 된다.

- 이미지 링크 형태는 
- [https://notion-ga.ohwhos.now.sh/collect?tid=](https://notion-ga.ohwhos.now.sh/collect?tid=){트래킹 ID}&host={도메인}&page={경로}
- {트래킹 ID} :  구글 애널리틱스의 **UA-00000000-0** 형식의 추적 ID
- {도메인} : [**notion.so**](http://notion.so/)** **(노션 페이지와 연결할 것이므로)
- {경로} : **/notion/main** (반드시 / 슬래시로 시작하는 임의 경로를 넣어야 한다. GA에서 인식하는 페이지다.)


- 예시로 만든 링크는,
- [https://notion-ga.ohwhos.now.sh/collect?tid=](https://notion-ga.ohwhos.now.sh/collect?tid=)**UA-00000000-0**&host=[**notion.so**](http://notion.so/)&page=**/notion/main**


- 위와 같은 링크를, 노션에서 /image 하고 삽입하면 된다.
1. /image 입력하고, image 선택
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/375330ee-0316-46a9-86bb-3f324b52ada2/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466QDTJBNQP%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044904Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIHxsv0HO4bVtepYAD9QxGy3VF8kj8%2Fh35aNxDJHf0yQaAiAcXv%2F6pYVd6bE2kgDMEM30daydSbbxQrGeSzeA4E7i1CqIBAjl%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMlvTpXZGN%2FUdBkDjcKtwDrpEw%2BD5RD2K%2BochUY8msE7EuxMIyb2UaVETOBNYBbHOimt0nDgf662FvTpj0owYSJMr%2FpO8wRKc3EcifInb%2BwDpqFcEWh%2BV0AI7IJ6nAyCy5WyXsjCtm%2BP%2BbAFN5UcXegfdR8YCiOCtzSulB0Mi9aJZPBOFw4eaaaABu446uT9mxnYx9n9gAVm63B2nEKzgr7OqX3PAYUaWo1%2BfKzplZuN8G3seIfCaMdgjd8RcpcZQwlaFe3RfI%2BnRxIZCL7xSEEL8SbrK0h%2Fa5n8flkuNHN4N8gUOOHttxqM0wv9NfFFhqkUiTIcjJbJfle%2BkvIQ7Cz0FdcD2TRNs%2BFiyF5ETE0iJZG9522AzHp8OfgHqnAxknFCDt7mC01CCAMtJVqtTOATOdCL%2F8kZ7WOmwdbWtkcFW8L%2F8%2BuIlpOg4TDtUS4tgDHFge5OXz1LoPsZ8AHlFSurJE6eh9PjmXGDl1eVVzaXOqebJN07QuALJF6laTjVOz1gTDsOyyDoNbr8K6u7niFY9bN5tbZOwHBDJS7uo6DziWoLR9fD%2FIQ5I3c9imKf8CnnliJEJuBExbj6Yta6COvLkWTSJyniz%2F9%2FqheiW33iTkngXlVDlQbZiXBgGy1tBcO45PXiiRlyYCvCgwjs3OvgY6pgGMOnY%2Ftav3CwmumwyMDg3N8FKLr7kGFNuvHyuFXFfuoyLRZZS5tiFpg7xhlD610LKnXVduUDH4H%2BChGMK9r7jUhuQNwZGxzEFDh2EviBfI5WY29lBX%2FC4lzMhGONlTJ%2FWYHr210YxxBnXeYEyezS3oq3p%2F5eXRPwVPa%2BVQKBWNAdC42nBgFqt3agsZuf2Nt%2FVnLKGziPWNuKd%2Fgx51V%2Fszo%2FhELc00&X-Amz-Signature=53c30266eae1fdde9695c670c43c7e8be46bfb96a93cc9598b70b56584252feb&X-Amz-SignedHeaders=host&x-id=GetObject)

1. Embed link 선택하고, 위 예시 링크 삽입
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/5ec12e1a-ad69-4cc6-9ae0-47abbfdeb320/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466UYMK3YST%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044905Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQDOJ%2FcI8XSpAf1UTZZ9IvyRf7UZwCmtdmUQ%2B9jnguvNzAIhALZnKScLAzNUjzQ5JQY1ZxMJhw5o7E63K5vv8YsmAwmGKogECOX%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgzXYCPeF4v%2FKU4HwK8q3ANfJ61vlGq%2Bg5OMhwFfGd0LRDZCvr9M%2FKltGGWgfRrjq7a7FA2ndfSHyEU4Qt69xJNY0nT%2Fuqnj1Tpz9fRNJHyV1Hp8c4ijD%2FdzJWDPeplGBAEtKiQtL3gCwlXME8o6yh3HqhPKZgUDvCUfndprxgJQVbr4y86lgRsAEecKbLsI%2FZjrk4vl2zNKfIkQnFARAn9JJb%2FDS1xmt8ujmfAjkEBZhlLB6hcfXDsYatqyp4fd13rpWQxi7YU9jsCQDk9HgfkfvOyoCJCoMqkp48sCAnhpYbx9qFaVGDF0Qi0MxZNfIepX3vYdmY7Ap6PeKXbWV3mEWwt9BUozGzj6rw72G%2FVzuAtKAg4sK6pkAnTRYOocvJVO4K89k7aTNnvmtR23UU90BDSTLwgNox233P3QSCV7U5qlIdJDY4CLnjFmZHGlh1gBFbi9XkLkEfoce6tqqk0a85AbA3QKaJsCQccKaVYd0L8Owh4TltEvzNrC%2FpExPRsjwTS5j1WMMYgU0a9EIIEwHnImZ7nSb4J%2B2%2BPfdJWbZoFU1HhCIfawyO0MmnP99qCTL36fbtRh0GLu%2B9EGkOEMyAdCUxJSnKP00nJ8ZJzAwN1v%2BYWE%2FduJw5mPVnHkOV%2BIHZuX5SwwP%2BrrRjDWzM6%2BBjqkAaVbdaG4AG3uJ4U8COpBSuIbPcHAaa%2BRmlWPLJldFFZwxdlegT5yNK2RfePjTd1tPkN9NMMHWzWz%2FQ6B3uLCYrgAgUlcd5McqzBs6g7PWhMM8zsGnJ%2BqydgswJjLDG8jA4PcKCAdOe4qUs3gNyRLj%2BLCpEavdRqk2swfuCZa4IQc8%2FrlfIhOBrwHbEFiJjH0l1s%2FyYEFciQAP1Jln5GuBxWBMsZg&X-Amz-Signature=6d361437bd6fd5ff9727409750dc82b12aee03d9fc718921e14f29d5c83adcc8&X-Amz-SignedHeaders=host&x-id=GetObject)




이렇게 하면 아래와 같이 구글 애널리틱스에서 /notion/main 실시간으로 확인이 가능하다. 끝!

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/c38ef405-499b-4311-9bae-e079db68a063/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466TIMQE77Z%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044902Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCID2MV%2BVEeSVS5y713dz15nY4nZYfDcaKS4F%2FhCClk5IeAiAanwiq4i76hU2gcFIhOUiSsbgZBi4If1ZF8jea8LEd5iqIBAjl%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMpHA%2Fhp%2B3vW3j4xYMKtwDatNfEh%2F%2BB680debfac6VwRwT3qX0NLxDGAlQec5ABZIrNwgrBdWCgm36COwbChdftcB4TpMXuX8OPoJxUcj%2FZIgY0qo52hw06LKsvGtmc4%2FRPkvY9EHYEcJzSCiIWkU6NDiUKLjhmY1wdzM8B1FcvI0QKY%2BitZ1jNYZFMQs1%2Fk9Ar%2BiweP0oaJVg1A0I624RRsgOl48uagwNwPYvx3Kc5bH41S9L0TvTb2cErtero8Xg5SOUe62pjuCvCcHQf6hQa0n1anCFSFU02NO4g5a8RZYMFUT39D1%2F22R2Oc4yNWoQdZIv387GGdxQmGeogKwwy%2Fe0RCneQFxYcNoPFNnNXmD7iRqASFxMB4AaPJZWnWRjhGoollOqYcYsDYsaobOMz4HVqgc7b1HBBtsBpmKm3fQyOkQZtb8d8et5d94gRV4eEV%2FzZCSEAh6JEFcrpToyH6uyS1NwpHIltgMlEXe3GoaMsfstiRDZwajsiax3uy2aoZ1sjLF3YXJ%2Fe%2F%2FM6xTGfW1l4hCNQSO8U8YYm%2F5qnIyvAIgq9iFcVBiQ1tbCYw6%2BgiOceJSvwmanz2fOBJcjs24L0p3k6rjvqbr4LPN8YHQnyuqMp1Hjw1eOrrfNKUskGyg0oqRMuA6%2BTM4wl83OvgY6pgG8qxXpSvVk%2BhFmBHBk8VvoWnOaWnT%2FxgKEomPU5R8Zhr5VvbEynGyICN7xyT7ZL4AnqF3nYgQ%2FHni64xrvpHj4SBxi3VzQhbSqmkZvm4f3gtDz2Qk3BDrdl0dGXqPCg6NbcL8Y1LJUkZ3uxJq3Wb3IUn27Sc1fViaNmbgHx4nKwD%2BRxWAFyWdJN4Xsabrf05eUJi2pHmHbVbH5i8Af2djdM8AdDL6c&X-Amz-Signature=cba734cf2288b260cd168b1c74db098cd917b4a75c975a84d85ada80005d0f37&X-Amz-SignedHeaders=host&x-id=GetObject)



