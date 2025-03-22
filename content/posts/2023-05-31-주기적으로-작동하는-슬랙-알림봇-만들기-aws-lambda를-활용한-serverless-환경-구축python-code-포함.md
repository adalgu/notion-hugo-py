---
author: Gunn Kim
date: '2023-05-31'
draft: true
keywords: &id001
- python
lastmod: '2025-03-21T02:44:00.000Z'
notion_id: 2ffc4916-2bec-4a88-804d-066c815ee3e0
slug: serverless-gpt-slack
tags: *id001
title: '주기적으로 작동하는 슬랙 알림봇 만들기: AWS Lambda를 활용한 serverless 환경 구축(Python Code 포함)'
---

안녕하세요, 여러분. 오늘은 AWS Lambda를 이용하여 주기적으로 알림봇을 실행하는 방법에 대해 소개하려 합니다. 이 포스팅에서는 파이썬 코드를 사용하여 이를 Slack 팀채널에 알리는 알림봇을 만들어 볼 것입니다.

## 1. 웹훅 설정하기

- 주요 키워드: 웹훅, 토큰, URL, 메신저
알림을 보내기 위해서는 먼저 웹훅 설정이 필요합니다. 웹훅은 메신저에서 제공하는 URL입니다. 이 URL은 메신저에 메시지를 전송하는데 필요한 토큰을 포함하고 있습니다. 웹훅 URL은 슬랙, 노션 등의 메신저에서 생성할 수 있습니다. URL에 메시지를 포함하여 POST 요청을 보내면, 우리가 원하는 방식으로 커스터마이즈된 알림을 보낼 수 있습니다.

- 웹훅만드는 간단 스텝
1. 슬랙 앱을 만든다.(슬랙 메뉴중에 앱만들기라고 있음)
1. Incoming Webhooks 활성화(슬랙으로 들어가는 웹훅이라 incoming webhook)
1. 웹훅 생성 : 알림을 보낼 채널 선택
1. 웹훅 URL 복사!

상세한 내용은 아래 Slack 매뉴얼 참고

## 2. 코드 작성하기

- 주요 키워드: Python, POST 요청, Slack
웹훅 설정이 끝났다면, 이제 Python을 사용하여 POST 요청을 보내는 코드를 작성합니다. 이 코드는 Agit의 특정 그룹에 새 글을 등록하고, 이 결과를 Slack 팀방에 알리는 기능을 포함합니다.

```python
import requests
import time
from datetime import datetime

# private 정보는 마스킹 처리
url_slack = '<https://hooks.slack.com/services/XXXXXX>'
text = "@user1 @user2 @user3 ..."
title = "Weekly Meeting Alert"
dt = datetime.now()
ts = time.mktime(dt.timetuple())

def send_msg_to_slack(url, msg, title):
    slack_data = {"attachments": [{"color": "#e50000","fields": [{"title": title,"value": msg,"short": "false"}]}]}
    requests.post(url, json=slack_data).raise_for_status()

def lambda_handler(event, context):
    send_msg_to_slack(url_slack, text, title)
    return {'statusCode': 200, 'body': 'Post SUCCESS'}
```

## 3. AWS Lambda 함수 생성

- 주요 키워드: AWS Lambda, 함수 생성, 라이브러리, 계층 추가, 배포
다음으로, AWS Lambda에서 새 함수를 만들어 방금 작성한 파이썬 코드를 추가합니다. 이 함수는 AWS에서 제공하는 기본 계층을 활용하거나, 필요에 따라 사용자 계층에 라이브러리를 추가하여 설정할 수 있습니다.

사용자 계층에 라이브러리를 추가하려면, 로컬 환경에서 필요한 라이브러리를 다운받아 zip 파일로 압축하여 업로드하면 됩니다. 함수 작성과 라이브러리 설정이 완료되면 테스트를 진행한 후, 배포하여 실제로 함수가 작동하는지 확인합니다. 배포 단계를 건너뛰면 함수가 제대로 작동하는지 확인할 수 없는 경우가 있으므로, 처음 실행할 때는 꼭 배포 과정을 포함하세요.

## 4. EventBridge(CloudWatch Events) 설정하기

- 주요 키워드: EventBridge, CloudWatch Events, Cron 표현식, 주기 설정
AWS의 EventBridge(CloudWatch Events)를 설정하여 알림봇이 주기적으로 실행되도록 합니다. 이 과정에서 Cron 표현식을 사용하여 알림봇이 작동하는 주기를 설정합니다.

예를 들어, 매주 목요일 오전 10시에 알림봇이 작동하도록 설정하려면, Cron 표현식을 `**cron(0 1 ? * 5 *)**`로 설정하면 됩니다. 단, 이때 시간은 GMT 기준으로 설정해야 하므로, 로컬 시간에 따라 적절히 조절해야 합니다. 서울 시간은 GMT+9이므로, 오전 10시를 GMT로 표현하려면 10에서 9를 빼서 1로 설정합니다.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/b915b615-5b1a-4d52-a3cd-be05d613964f/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663LHXJ2DW%2F20250322%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250322T091907Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEGEaCXVzLXdlc3QtMiJGMEQCIDRhOBkiAhJ%2Fyf4xPmlmS3PeQ08smkvfOunb2gXaVtgrAiARlSBOwX6u0moRJ2hTSxhnwyVCAGgdybqCBOCT3xUWqiqIBAi6%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMPQLaGdDMEB%2Fv6wzIKtwDIcb3fDep18y3ek86mgavbYIEaafzzZz3YYAGpj8OYqNJwQhstZnQA3DZxz0ER29SmjZO3d8zmG99IQxPMfGzb78%2FGd%2FOexF6mSE%2F%2BRU34L0i0EBLHsY9ORE6y44%2FcvdWo1zV02Af%2F2c73sRoetzSBnSRmwAeVhN2F%2BQvtPA4PAorX0LGNUGv5%2Ft0TvhTvYSj4uiuGP3xyZrXEF%2BLnsefSvFQ4BHEhi6ot0ZYjbkfa9ZBTxhv7Mm%2BJ5dsiDMDO5ZWbNfjdfeXwxjBUyN968kN64Cizxp3oKsTMGfxFncDNgvWkFlh%2FIrw4nuZPWfm8YSPQIGIY5LfFYj%2B%2Fb6HpmyXZ3x%2BXsA2A0UHEPaf%2B8vYSpK51%2FUHCG8OacfuC8o0yRGykzrhZr6hOUZE4WvmUt4TpOfgCHAjRMppXS1bGV8lgGWZDAx6ISay8tQuokWjaKnyiu1QX9v0Dmwoln72rnGxV9YjJUh2aFVqiZmFoMnSiJaq%2FEv33isQg93l81IhoEOR8N%2FxzJSKibw8CYvwEaqNjfqTik8Lnf5fLznE6xiCbl4TE1sPh24TVhDYEwGnK9z49yr3Py24Fa7fQ%2BxW5DaSVAocsNx2wIwkKJjiKcTpmhahtDrJ6o08bYdl2Xkwsuv5vgY6pgEPQ8UmQ2x4JEMckin%2F5%2F%2FGDjhN9DSnW98%2F1SJByuiLvK8v3oyKYN0EcmbeJmbT3Xf0lweOI%2B3dWLbqRfPKJ7wRseGtm5MzuIe3jIN6Ew3YsrcFnSCDtoDBu%2FsK8hLi%2BjqRbp6FdjW7yJED0q27IXU0nsCHqfJmVk9e037xl8jT09CPMFVmo9eylet0zubYzpUX5KBO5T2hfDvlMt3jaNw5O87Pjr%2Bg&X-Amz-Signature=27e1e42d588a329ae8ae48dc6372b7cdb55c62fee4bcb9307956c13c2a55d92b&X-Amz-SignedHeaders=host&x-id=GetObject)

## 5. 응용하기

- 주요 키워드: 알림봇, 조건 설정, 응용
이제 주기적으로 알림봇을 설정하는 것을 완료하였습니다. 우리가 만든 알림봇의 구조는 이렇습니다: 어떤 조건(예: 목요일 오전 10시)이 충족되면, 사내 커뮤니케이션툴에 포스팅하고, 슬랙의 팀 채널에 알림을 올립니다. 이 구조를 바탕으로 다양한 방식으로 응용해 볼 수 있습니다.

예를 들어, 카카오에서 만든 아지트에 알림을 보내고 싶다면, 위에서 만든 코드에 아래 강조한 코드만 추가하면 됩니다.

```python
import requests
import time
from datetime import datetime

# private 정보는 마스킹 처리
url_slack = 'https://hooks.slack.com/services/XXXXXX'
**url_agit = 'https://agit.in/webhook/XXXXXX'   **
text = "@user1 @user2 @user3 ..."
title = "Weekly Meeting Alert"
dt = datetime.now()
ts = time.mktime(dt.timetuple())

def send_msg_to_slack(url, msg, title):
    slack_data = {"attachments": [{"color": "#e50000","fields": [{"title": title,"value": msg,"short": "false"}]}]}
    requests.post(url, json=slack_data).raise_for_status()


**def send_msg_to_agit(url, text, title, starts, ends):
    payload = {"text": text, "schedule": {"title": title, "color": "pink", "is_allday": "true", "starts_at": starts, "ends_at": ends}}
    requests.post(url, json=payload)**


def lambda_handler(event, context):
**    send_msg_to_slack(url_slack, text, title)**
    send_msg_to_agit(url_agit, text, title, ts, ts+3600)
    return {'statusCode': 200, 'body': 'Post SUCCESS'}
```


아래와 같이 조건에 부합하면, 노션에 기록하고, 알림까지 하는 봇도 위와 같은 방식으로 쉽게 만들 수 있습니다. 또는 ChatGPT API를 활용해서 뉴스 요약 봇도 만들 수 있습니다.

> `조건 : 코스피 지수가 2500을 돌파했다.
실행 : 노션에 기록하고, 슬랙에 알림`

그럼, 각자의 환경에 맞게 알림봇을 만들어보세요. 다음 시간에는 다른 흥미로운 프로젝트로 찾아뵙겠습니다. 감사합니다!

