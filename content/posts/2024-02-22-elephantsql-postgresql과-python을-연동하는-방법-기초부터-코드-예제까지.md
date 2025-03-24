---
author: Gunn Kim
date: '2024-02-22'
description: 이 글은 Streamlit 프레임워크를 활용해 파이썬으로 개발된 AI 기능이 탑재된 애플리케이션의 로그 데이터를 관리하고 분석하기
  위한 데이터베이스 통합의 중요성에 초점을 맞추고 있다. MongoDB와 PostgreSQL 사이의 선택 고민을 탐구하며, 강화학습에 적합한 구조화된
  데이터 축적을 위해 PostgreSQL을 선택한 과정을 소개한다. ElephantSQL을 통해 AWS 상에서 서비스로 제공되는 PostgreSQL의
  클라우드 기능을 강조하며, psycopg2 라이브러리를 사용해 PostgreSQL 데이터베이스에 연결하고 기본 데이터베이스 작업을 수행하는 방법을
  코드 스니펫과 함께 설명한다.
draft: true
keywords: &id001
- Tech
- ChatGPT
- python
- Web Dev
lastmod: '2025-03-21T02:44:00.000Z'
notion_id: b5e7ed83-08b0-47d0-ba23-977351c669ee
slug: Postgres-vs-MongoDB-Python-GenAI-App
subtitle: 'AI 기반 애플리케이션에서 데이터베이스 통합하기: PostgreSQL과 파이썬 사례 연구'
summary: 이 글은 Streamlit 프레임워크를 활용해 파이썬으로 개발된 AI 기능이 탑재된 애플리케이션의 로그 데이터를 관리하고 분석하기
  위한 데이터베이스 통합의 중요성에 초점을 맞추고 있다. MongoDB와 PostgreSQL 사이의 선택 고민을 탐구하며, 강화학습에 적합한 구조화된
  데이터 축적을 위해 PostgreSQL을 선택한 과정을 소개한다. ElephantSQL을 통해 AWS 상에서 서비스로 제공되는 PostgreSQL의
  클라우드 기능을 강조하며, psycopg2 라이브러리를 사용해 PostgreSQL 데이터베이스에 연결하고 기본 데이터베이스 작업을 수행하는 방법을
  코드 스니펫과 함께 설명한다.
tags: *id001
title: '**[ElephantSQL] PostgreSQL과 Python을 연동하는 방법: 기초부터 코드 예제까지**'
---

**PostgreSQL과 Python을 연동하는 방법: 기초부터 실습까지**

생성 AI 기술이 탑재된 현대 애플리케이션은 로그 데이터의 효율적인 관리와 분석을 위해 데이터베이스(DB) 연동의 중요성이 점점 증가하고 있다. 특히, 파이썬 언어로 개발된 애플리케이션에서는 사용자 인터페이스를 구축하기 위해 Streamlit 프레임워크를 주로 활용하는 추세다. 생성AI 프로젝트를 진행하면서 로그를 저장하기 위한 DB 선택을 고민하고, 실제 간략한 예시를 작성해 보았다.


# 1. 들어가며

### 데이터베이스 선택의 고민

애플리케이션 개발 초기 단계에서 가장 중요한 결정 중 하나는 적합한 데이터베이스를 선정하는 것이다. 이번 프로젝트에서는 MongoDB와 PostgreSQL이 후보군으로 올랐다. MongoDB는 NoSQL 데이터베이스의 대표주자로, 과거 프로젝트 경험 덕분에 개발자들에게 친숙하다. 클라우드 기반 서비스의 무료 이용 가능성은 MongoDB를 매력적인 옵션으로 만든다. 반면, PostgreSQL은 전통적인 SQL 데이터베이스의 강력한 기능을 제공하며, 최근에는 생성 AI 기술과의 통합 사례가 늘어나고 있는 추세다.


![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/274558e5-f703-4399-8bca-f810e510ec31/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665RCSBWDL%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T102045Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCICP6Q7vGW%2F6Gw2YsivPHtd5cak7EN5%2BVUu2yf%2FfNke0RAiEA28yOhHnQfnj041fs3A7klfwX%2BLOM02JhY9O5X8orPKcqiAQI6v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDKdlhPIFTFRr%2FpDfgCrcA9BI5aDi%2FS37NsoT%2FR0rY%2BAkYiSd0kpOfLynyyJZKzYHQTTFLi7eTjDw3M0x5SLuRK75Px%2Bwpi5WBjxy7p%2Fu9sPyGjoiOHcQ1BX6bDIIOuIh0nz6aYBzYrjTxCA3YFxxDHT41YjbbTJlcop0r5Osg4uKDAj4uOATVFSIcSpG0lOn4%2FNAFnIeANj%2BCyzQdjVS17FJQ8YW18nOtS0CM2xRHWetb0fDt9ZdqH5PvOqWtFAzbAlAdQIwW%2BUEyFyTvR4tjtJ1t7NVvUWgjen3D96ZXH1XTm%2FxGqEbxK0dfVJ%2FeoV%2BOXdjWXFbnrvZpN4NVQjmaxhLdpDoChudjFFr7fh2IY6ruFkM5OhGpGpZdv6Ps8UqVsmXBlSDHGlMCaeBO1%2FgtzgBzHJCzri2uEV4jVgJvxXgbRz2U2U5dTM21U%2BNH09N1Wxwr3pGH7YMz7nPYpHouHkZCesOvuO7keSpsjmedmkGyl9c5koWFsYdC2thQEquoMlP73RUWXQhOiO3U7WDUooV2mHv0i08KQtew7mvCmSePVucOwKZ2xRgTsmmWffmdECV8mt3QX6v%2Fnux0pxhX8Uztlzi8kaUVXYVy5MooPuj3ivJumCF5ntTrnOKsjm5NJotsfiCwwMhIiJSMLXEhL8GOqUBb%2FbcQxAR2mVSPqU3%2F1KJLX4HCf6276jR6ufFj7WOGkgiPFJXdNa%2FuNIO1TYTHhjZFan3M4udfKBLu1f8uCZZ4Uw%2BU1H5lzQRJz1ZQC2AUfMvVn%2FBkJrPcZqMTTh3D40oFJdMpLDfSRLWK0K54RoYNgg4Cnqpn1j6fCzT6%2FVe3mcR7mVB%2FBQteEl%2BMdAZFIzkce%2FhlimZP5ZPxKgJz8CSUEFYV2SD&X-Amz-Signature=57ac6dcf1c38ac126a4b4afc81f6e122543cc709f5149092ce6dc7e8f351ad71&X-Amz-SignedHeaders=host&x-id=GetObject)

비록 MongoDB를 사용하여 로그 데이터를 관리하고, 필요에 따라 SQL 데이터베이스로 이전하는 방안도 고려 가능했지만, 프로젝트의 현재 요구 사항과 앱이 생성할 로그 데이터의 양을 고려했을 때, 어느 쪽을 선택해도 큰 문제가 없어 보였다. 그러나 최종적으로는 강화학습에 활용될 로그 데이터의 구조화와 축적의 중요성을 고려하여 PostgreSQL을 선택하기로 결정했다.

PostgreSQL은 강력하고 안정적인 오픈소스 관계형 데이터베이스 관리 시스템(RDBMS)입니다. 높은 확장성, 유연성, 보안성을 갖추고 있으며, 다양한 규모의 기업에서 사용되고 있습니다. 특히, 다음과 같은 특징은 데이터 기반 경제 시대에 기업들에게 큰 이점을 제공합니다.

- **낮은 총 소유 비용(TCO):** PostgreSQL은 오픈소스 소프트웨어이기 때문에 라이선스 비용이 발생하지 않습니다. 또한, 다양한 플랫폼에서 운영 가능하며, 관리 및 유지 보수가 용이하여 TCO를 크게 절감할 수 있습니다.
- **뛰어난 성능:** PostgreSQL은 멀티 코어 프로세서 및 고속 저장 장치를 활용하여 최상의 성능을 제공합니다. 또한, 다양한 데이터 유형을 지원하고, 복잡한 쿼리를 효율적으로 처리하여 데이터 분석 작업을 지원합니다.
- **높은 확장성:** PostgreSQL은 수 페타바이트의 데이터까지 확장 가능하며, 수백만 명의 동시 사용자를 지원합니다. 기업의 데이터가 증가하더라도 쉽게 확장하여 대응할 수 있습니다.
- **강력한 보안:** PostgreSQL은 다양한 보안 기능을 제공하여 데이터를 안전하게 보호합니다. 암호화, 접근 제어, 감사 추적 등의 기능을 통해 데이터 유출 및 침해를 방지할 수 있습니다.
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/0714b38d-01fa-4c94-9c56-ca80167fa498/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4667WX7LRDT%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T102045Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBgA%2Bet%2Bh0oRLy4HFvxm0BSSPI2LnXZ6BoRBsdfHbugSAiAH75CekMBUT7IrorU%2B9ZVa%2FcQRusGjaIrtb%2FX3iUmCViqIBAjq%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMXDdAbXAJiPO1v%2FA%2BKtwDY3lA4g2vBqVMhebz2X1mzvPu6kfeYhyzm7B383h0VRzsRAHTDssdkhZSJbtixmpAUgUmXSXf3dVFiSt%2B%2Ftpq8G%2BfPSDW3hM104qNcxzdI2WiMurDxnKAjxaEF7uFt8e1e4H5aHma99E5CMZnCHkIVmXNp8aI9QYr29Yev4RYzaUmle37f9WJ86Lud5Td6Q7Wc2L292uPLJlrlv5Y3VnA58G6PuIa0WJcWy%2FedyfyTWraLBwNnL130vM0CbM1uFXcgus1yg3L6Tgkzr32BuN2kcZZnvmIhpVZ4inc8mJJe4PT%2F4knk1Ip0fO2hVg9qH9O%2FPwgMQt%2FhMM6t%2Bxp2KF5vmh8glU%2BBB%2FqVv1Vxdh%2BFBKUSffrsH7DFoh8fZV%2FlgoRXErcqbSPyq2BrFYxC239AMI4aNHHaSvQTYlF93KrgEXlnTse%2BbFBmFaSsfVaBWf8f%2B0PvRrTHXGQe%2BjXmnfvYmbcbvHuc29i%2B82VjpaJ%2BAWpwVeJELI5hylohFnKNwc%2F6jGTi0gFDEIldNw1UbJJF1s6iTIVJuRloSCX2C%2BsxwyWwo%2Bd9Ge%2BbtXzyUMgp54QMi4FkKkvFcCtss6oYTHKk3abY4EyfvGYfKPJZCQdASscX1I%2F6kgmUSO2ZvswvMWEvwY6pgF3BO5h3bHYGMltM6V%2FYhK%2FDPdWL8GPDORQj0pC5uaIRPzySqC5s1%2B9eAnS2vHvlX9gxS16uFyi36sfPiMZ%2FD6gGNrsmIEMwnCw%2FroVU0fVqYCvk9VW0dkyUs3238egcWm5KaQOgYcROoQSRYtxpH%2BbS6DWtVohBqjKKy5gMKXgawug7jlEX0niuRwkx9ZslNVUO6izcWPS%2B7zwnEqR%2FMC27te6tUbA&X-Amz-Signature=f79c90b1afdd6ce5f5b77fd53df8ddbf8825631b1c2833fac2b3c62e4b779823&X-Amz-SignedHeaders=host&x-id=GetObject)


### 클라우드에서의 PostgreSQL 활용

PostgreSQL은 일반적으로 로컬 환경에서 설치하여 사용되지만, 최근에는 클라우드 서비스 형태로도 제공되는 추세다. 이러한 변화는 개발자들에게 더 큰 유연성과 편의성을 제공한다. 이번 프로젝트에서는 'ElephantSQL'이라는 서비스를 통해 PostgreSQL을 클라우드 환경에서 활용하기로 결정했다. ElephantSQL은 'PostgreSQL as a Service'라는 컨셉 아래, 몇 가지 간단한 설정만으로 데이터베이스를 쉽게 구축하고 사용할 수 있게 해준다. AWS 기반으로 운영되는 이 서비스는 개발자들에게 최대 20MB의 데이터 저장 공간을 무료로 제공한다.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/cbf1c15e-91a6-4778-965c-386750619ba1/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665RCSBWDL%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T102045Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCICP6Q7vGW%2F6Gw2YsivPHtd5cak7EN5%2BVUu2yf%2FfNke0RAiEA28yOhHnQfnj041fs3A7klfwX%2BLOM02JhY9O5X8orPKcqiAQI6v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDKdlhPIFTFRr%2FpDfgCrcA9BI5aDi%2FS37NsoT%2FR0rY%2BAkYiSd0kpOfLynyyJZKzYHQTTFLi7eTjDw3M0x5SLuRK75Px%2Bwpi5WBjxy7p%2Fu9sPyGjoiOHcQ1BX6bDIIOuIh0nz6aYBzYrjTxCA3YFxxDHT41YjbbTJlcop0r5Osg4uKDAj4uOATVFSIcSpG0lOn4%2FNAFnIeANj%2BCyzQdjVS17FJQ8YW18nOtS0CM2xRHWetb0fDt9ZdqH5PvOqWtFAzbAlAdQIwW%2BUEyFyTvR4tjtJ1t7NVvUWgjen3D96ZXH1XTm%2FxGqEbxK0dfVJ%2FeoV%2BOXdjWXFbnrvZpN4NVQjmaxhLdpDoChudjFFr7fh2IY6ruFkM5OhGpGpZdv6Ps8UqVsmXBlSDHGlMCaeBO1%2FgtzgBzHJCzri2uEV4jVgJvxXgbRz2U2U5dTM21U%2BNH09N1Wxwr3pGH7YMz7nPYpHouHkZCesOvuO7keSpsjmedmkGyl9c5koWFsYdC2thQEquoMlP73RUWXQhOiO3U7WDUooV2mHv0i08KQtew7mvCmSePVucOwKZ2xRgTsmmWffmdECV8mt3QX6v%2Fnux0pxhX8Uztlzi8kaUVXYVy5MooPuj3ivJumCF5ntTrnOKsjm5NJotsfiCwwMhIiJSMLXEhL8GOqUBb%2FbcQxAR2mVSPqU3%2F1KJLX4HCf6276jR6ufFj7WOGkgiPFJXdNa%2FuNIO1TYTHhjZFan3M4udfKBLu1f8uCZZ4Uw%2BU1H5lzQRJz1ZQC2AUfMvVn%2FBkJrPcZqMTTh3D40oFJdMpLDfSRLWK0K54RoYNgg4Cnqpn1j6fCzT6%2FVe3mcR7mVB%2FBQteEl%2BMdAZFIzkce%2FhlimZP5ZPxKgJz8CSUEFYV2SD&X-Amz-Signature=fa025d24aa5be1b77ffcc38ac4f73bbe6bd6bee7fcaafd092d8b649b6fce2b5e&X-Amz-SignedHeaders=host&x-id=GetObject)


# **2. 파이썬에서 PostgreSQL 사용 코드 설명**

psycopg2 라이브러리를 사용하면 Python 코드에서 PostgreSQL 데이터베이스에 쉽게 연결하고 작업할 수 있다.


**1. 라이브러리 불러오기**

```python
import psycopg2
```

PostgreSQL과 Python을 연결하는 `psycopg2` 라이브러리를 불러온다.


**2. 연결 문자열 설정**

```python
# 데이터베이스 연결 정보 설정
server='floppy.db.elephantsql.com'
dbname='User & Default database'
user='User & Default database'
password='Password'

conn_string = f"dbname={dbname} user={user} host={host} password={password}"
```

데이터베이스 이름, 사용자 이름, 호스트, 비밀번호를 변수에 저장하고, `f-string`을 사용하여 연결 문자열을 생성한다. 해당 정보들은 ElephantSQL에서 Instance를 생성한 이후에 확인할 수 있다.

![ElephantSQL에서 확인할 수 있는 DB세팅 정보](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/4c1c7fdd-c1db-48e0-8f05-e77688bac196/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665RCSBWDL%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T102045Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCICP6Q7vGW%2F6Gw2YsivPHtd5cak7EN5%2BVUu2yf%2FfNke0RAiEA28yOhHnQfnj041fs3A7klfwX%2BLOM02JhY9O5X8orPKcqiAQI6v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDKdlhPIFTFRr%2FpDfgCrcA9BI5aDi%2FS37NsoT%2FR0rY%2BAkYiSd0kpOfLynyyJZKzYHQTTFLi7eTjDw3M0x5SLuRK75Px%2Bwpi5WBjxy7p%2Fu9sPyGjoiOHcQ1BX6bDIIOuIh0nz6aYBzYrjTxCA3YFxxDHT41YjbbTJlcop0r5Osg4uKDAj4uOATVFSIcSpG0lOn4%2FNAFnIeANj%2BCyzQdjVS17FJQ8YW18nOtS0CM2xRHWetb0fDt9ZdqH5PvOqWtFAzbAlAdQIwW%2BUEyFyTvR4tjtJ1t7NVvUWgjen3D96ZXH1XTm%2FxGqEbxK0dfVJ%2FeoV%2BOXdjWXFbnrvZpN4NVQjmaxhLdpDoChudjFFr7fh2IY6ruFkM5OhGpGpZdv6Ps8UqVsmXBlSDHGlMCaeBO1%2FgtzgBzHJCzri2uEV4jVgJvxXgbRz2U2U5dTM21U%2BNH09N1Wxwr3pGH7YMz7nPYpHouHkZCesOvuO7keSpsjmedmkGyl9c5koWFsYdC2thQEquoMlP73RUWXQhOiO3U7WDUooV2mHv0i08KQtew7mvCmSePVucOwKZ2xRgTsmmWffmdECV8mt3QX6v%2Fnux0pxhX8Uztlzi8kaUVXYVy5MooPuj3ivJumCF5ntTrnOKsjm5NJotsfiCwwMhIiJSMLXEhL8GOqUBb%2FbcQxAR2mVSPqU3%2F1KJLX4HCf6276jR6ufFj7WOGkgiPFJXdNa%2FuNIO1TYTHhjZFan3M4udfKBLu1f8uCZZ4Uw%2BU1H5lzQRJz1ZQC2AUfMvVn%2FBkJrPcZqMTTh3D40oFJdMpLDfSRLWK0K54RoYNgg4Cnqpn1j6fCzT6%2FVe3mcR7mVB%2FBQteEl%2BMdAZFIzkce%2FhlimZP5ZPxKgJz8CSUEFYV2SD&X-Amz-Signature=3070d1463321cc9508e7688d816efb3367837d8ccfe7b3abf71294f1e781c8f1&X-Amz-SignedHeaders=host&x-id=GetObject)


**3. 데이터베이스 연결**

```python
conn = psycopg2.connect(conn_string)
```

연결 문자열을 사용하여 PostgreSQL 데이터베이스에 연결한다.


**4. 커서 생성**

```plain text
cursor = conn.cursor()
```

데이터베이스 쿼리를 실행하고 결과를 처리하는 커서를 생성한다.


**5. 테이블 생성**

```plain text
create_table_query = '''
CREATE TABLE IF NOT EXISTS mytable (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50)
)
'''

cursor.execute(create_table_query)
```

`mytable`이라는 이름의 테스트용 테이블을 생성하는 SQL 쿼리를 실행한다. 테이블은 `id`, `name`, `email` 컬럼으로 구성된다.


**6. 데이터 삽입**

```python
cursor.execute("INSERT INTO mytable (name, email) VALUES (%s, %s)", ("Alice", "alice@example.com"))
cursor.execute("INSERT INTO mytable (name, email) VALUES (%s, %s)", ("Bob", "bob@example.com"))
cursor.execute("INSERT INTO mytable (name, email) VALUES (%s, %s)", ("Charlie", "charlie@example.com"))
```

`INSERT` 쿼리를 사용하여 테이블에 데이터를 삽입한다. `%s` 플레이스홀더는 삽입될 값을 나타낸다.


**7. 변경사항 커밋**

```plain text
conn.commit()
```

데이터베이스에 변경사항을 저장한다.


**8. 데이터 조회**

```plain text
cursor.execute("SELECT id, name, email FROM mytable")
rows = cursor.fetchall()

for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
```

`SELECT` 쿼리를 사용하여 테이블에서 데이터를 조회한다. `fetchall()` 메서드를 사용하여 결과를 모두 가져온다.


**9. 커서 및 연결 종료**

```plain text
cursor.close()
conn.close()
```

사용 후에는 커서와 데이터베이스 연결을 종료하여 리소스를 해제한다.


# 3. 전체 코드 예시

이제 전체 코드를 통해 파이썬에서 PostgreSQL을 사용하는 과정을 확인할 수 있다. ElephantSQL에서 제공하는 데이터베이스 정보를 활용하여 연결 문자열을 구성하고, psycopg2 라이브러리를 통해 데이터베이스에 연결한다. 이후 테이블 생성, 데이터 삽입, 데이터 조회 및 처리, 그리고 마지막으로 커서 및 연결 종료까지의 전 과정을 아래 코드에서 볼 수 있다.

```javascript
import psycopg2

# 데이터베이스 연결 정보 설정
server='floppy.db.elephantsql.com' #elephatSQL에서 생성한 DB 정보 활용
dbname='User & Default database'   #elephatSQL에서 생성한 DB 정보 활용
user='User & Default database'     #elephatSQL에서 생성한 DB 정보 활용
password='Password'                #elephatSQL에서 생성한 DB 정보 활용

# 연결 문자열 생성: 데이터베이스 서버의 위치, 사용자 이름, 비밀번호 등을 포함
conn_string = f"dbname={dbname} user={user} host={server} password={password}"

# psycopg2를 사용하여 데이터베이스에 연결
conn = psycopg2.connect(conn_string)

# 데이터베이스 작업을 위한 커서 생성
cursor = conn.cursor()

# 'mytable'이라는 이름의 새 테이블을 생성하는 SQL 쿼리.
# 테이블에는 id(기본 키), 이름, 이메일 필드가 포함됩니다.
create_table_query = '''
CREATE TABLE IF NOT EXISTS mytable (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50)
)
'''

# 생성한 SQL 쿼리를 실행하여 테이블 생성
cursor.execute(create_table_query)

# 'mytable' 테이블에 새로운 데이터를 삽입하는 SQL 쿼리 실행
# 여기서는 Alice, Bob, Charlie라는 세 명의 사용자를 추가합니다.
cursor.execute("INSERT INTO mytable (name, email) VALUES (%s, %s)", ("Alice", "alice@example.com"))
cursor.execute("INSERT INTO mytable (name, email) VALUES (%s, %s)", ("Bob", "bob@example.com"))
cursor.execute("INSERT INTO mytable (name, email) VALUES (%s, %s)", ("Charlie", "charlie@example.com"))

# 데이터베이스에 대한 변경사항(여기서는 데이터 삽입)을 커밋하여 확정
conn.commit()

# 'mytable' 테이블에서 모든 데이터를 선택하는 SQL 쿼리 실행
cursor.execute("SELECT id, name, email FROM mytable")

# 실행한 쿼리의 결과를 모두 가져오기
rows = cursor.fetchall()

# 가져온 결과를 반복하여 출력
# 각 행의 ID, 이름, 이메일을 출력합니다.
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")

# 사용한 커서와 데이터베이스 연결 종료
cursor.close()
conn.close()
```



[끝]


