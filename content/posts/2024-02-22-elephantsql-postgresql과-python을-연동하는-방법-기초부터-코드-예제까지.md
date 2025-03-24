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


![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/274558e5-f703-4399-8bca-f810e510ec31/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4ZR4YPI%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T062609Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEI7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDhsxMnnJC8KkHbA5WeO61hDy8BqKjeRiFO69WQhMeJywIgLheAk7J779veRBGgCL4GNRpbowTZ3qwB27AxZPZDaNgqiAQI5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDF2g3%2FUeJ0YImrfFEircA1xmo5JCPFOU2mDKJo43lJKs2jitYA6xgBgHFCyEWVEMIz0hugnOc2RnYRDHKynzms8VmISAUg5TakDB6lJH55XDtb%2Bxesma6gMEzT8FhWZC6DJ8FlYTfCRgnuE0v28XzQAgBiokayJWTnEsvMS7TJZ4Svq7wmeusXZhBQKKaR8pgQkrvhuY4AIsUBxvhckdaUu1gKWRPv4Pei%2Blis2GxFNUiK2ULaVeP6ttR82MPxlj%2Bp7dRz2D0dNDFPLGWXASax72oqw99Njv36ljt1qOI1qpJiFV2j21i3mKRxxBC%2BJ3OmMKbhjxPdwUYsZffXA0XySN0LcJphUjlsLd2l4DVyu4dfSY5cJjp0Jt2kif32kLHwYZyhrA5zJQ7Bug34VB3UA0xMWMYLMDOvfkAN5PVVSk6kuWC9CvF%2F%2BijBrWWeCPqm04wvhCnC3AKqmauWb%2FK02NSB%2BCswhocISJ7WAEpLk3G3CZ9%2FUM0vprzjqJTvysKw27%2Fzwpk5TUGqlRRuwxR9iAu7hcvOP3TyFrFUZWIEuh49PMcUGBMYsx83ruW3hl4RnDwiATiS6vY0oRrf0K%2F3h%2Fan8zx%2FPk2ZH%2Bau2bxVzDvZQUj9Nvg0ypd7JJC7J5Dyz35oCEiDnA6mMZMInjg78GOqUBZ3VCx916FbEEnZkApDcp6cImYcryngEEGGcJVV45QROZwFbxD%2Bp4wOweMJMVFojs0gWl%2Ftrm3tEeQLd4ko%2Fbo6n7K8Ud4qyL%2B0kaKrwBlys5wCEDdL4wL16EGvzm1R9mJUqlQxRVn2v03%2Bud6Oa5sd5D0b0W0al%2FmSxErRNazpNBNJuZ9wMiyLRWpIVLYpoKUMSXFos2uuZUkFENqhDnNfL13L0p&X-Amz-Signature=59b85e45242d314c1a9a4fbb38946bf957747e3adedb5fd4a2ee0478aeb09173&X-Amz-SignedHeaders=host&x-id=GetObject)

비록 MongoDB를 사용하여 로그 데이터를 관리하고, 필요에 따라 SQL 데이터베이스로 이전하는 방안도 고려 가능했지만, 프로젝트의 현재 요구 사항과 앱이 생성할 로그 데이터의 양을 고려했을 때, 어느 쪽을 선택해도 큰 문제가 없어 보였다. 그러나 최종적으로는 강화학습에 활용될 로그 데이터의 구조화와 축적의 중요성을 고려하여 PostgreSQL을 선택하기로 결정했다.

PostgreSQL은 강력하고 안정적인 오픈소스 관계형 데이터베이스 관리 시스템(RDBMS)입니다. 높은 확장성, 유연성, 보안성을 갖추고 있으며, 다양한 규모의 기업에서 사용되고 있습니다. 특히, 다음과 같은 특징은 데이터 기반 경제 시대에 기업들에게 큰 이점을 제공합니다.

- **낮은 총 소유 비용(TCO):** PostgreSQL은 오픈소스 소프트웨어이기 때문에 라이선스 비용이 발생하지 않습니다. 또한, 다양한 플랫폼에서 운영 가능하며, 관리 및 유지 보수가 용이하여 TCO를 크게 절감할 수 있습니다.
- **뛰어난 성능:** PostgreSQL은 멀티 코어 프로세서 및 고속 저장 장치를 활용하여 최상의 성능을 제공합니다. 또한, 다양한 데이터 유형을 지원하고, 복잡한 쿼리를 효율적으로 처리하여 데이터 분석 작업을 지원합니다.
- **높은 확장성:** PostgreSQL은 수 페타바이트의 데이터까지 확장 가능하며, 수백만 명의 동시 사용자를 지원합니다. 기업의 데이터가 증가하더라도 쉽게 확장하여 대응할 수 있습니다.
- **강력한 보안:** PostgreSQL은 다양한 보안 기능을 제공하여 데이터를 안전하게 보호합니다. 암호화, 접근 제어, 감사 추적 등의 기능을 통해 데이터 유출 및 침해를 방지할 수 있습니다.
![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/0714b38d-01fa-4c94-9c56-ca80167fa498/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466XZPEKELH%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T062610Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEI7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIBos%2F6p6K%2BDP4%2B2P5wTuxUyWB6SV693HVbEL1nAsB4sgAiBBamL%2BCB3A%2B5Lg26z816b18hYUS%2BwXXdZwhtO%2Fxw5lzCqIBAjn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMVPzHokMhv47eVwfvKtwDIchR%2Fz5w5KMhmtrEwYWaZwbI%2FtzJQTbFm2A8p2y9n2IHbHSc62bmoEp6eeW0Fq6Xpt8AjzUjRKMf5qFYJfMVNcM378iL8ZX4G4PQFB0bJnDgHnpCoYq2Q%2FyE6nkAVcBhSpHUMxP3ZVtMBUJJITquqlTgzwWLykvOP%2FKxNqMRt383mQQj5M%2BmdI8QPEy9pZDd%2BA4VCEc%2BQMqt5FepO0dcZfS7pVxUR05Uf1mISbqUNZG7OZx914DVA%2BsgPQUmfjAX4WNB8f5fPqgNcMp84t%2FQb8vdTt6cln6lI%2BFvV907u4AqGFx%2BK4p9z5zH9pzjf7uVB9wV3SOPCkApcOnWaFg%2FfS2ipbiB3tQHvxkyZKV%2FhC0NiRp6WbkYmcGXPKo5ktmHcTgDjZayM9XYKsnAllEkWaXzZbtbSNffrNhwREJY5dR4s4f5q3UFoRBDaXO%2FNYX6eiSpvd4i%2BANJZo87673rKpyphcD%2Bs3924Sm3iLZROsKj6rvz9HI%2BAGPCfyYADQbgw9v7sY9ZkBzyIVcvveX1v5knwVptYr2bSYslVmXJIsSRdtB6UTJxPc369PlodpeNkdG%2B55T%2Fj%2Bgn7uhwmxo7IVyaQI2qbGkO5DjcVl48L%2FgqdQDdTSBq3H4W9mIw5%2BKDvwY6pgGu025Utewbwu%2FY9v4bJq78dyaqdRZirivNY%2Bdi5sJviaYLYvw8jqHKW0GUCrivKUa%2Fn%2FVx0Qa0Tfx5nJu9yow2hENdP4XpEWJf0Lovc%2BsFq6a393yJJqaJjgoZA%2F%2FeIghoCWXOKaJlRNQeTe%2BjDJPqOYwL33SIjmcZy8PAKO3mUrXNo8bavC7avdWdO%2F7AYPemQuu9eqVyLC%2Bsezjv0I0xJzZu2YfD&X-Amz-Signature=1a657f6d81557a13a27a1a35f2dd822b07e4a1205c38643a1c852e17c69f1c33&X-Amz-SignedHeaders=host&x-id=GetObject)


### 클라우드에서의 PostgreSQL 활용

PostgreSQL은 일반적으로 로컬 환경에서 설치하여 사용되지만, 최근에는 클라우드 서비스 형태로도 제공되는 추세다. 이러한 변화는 개발자들에게 더 큰 유연성과 편의성을 제공한다. 이번 프로젝트에서는 'ElephantSQL'이라는 서비스를 통해 PostgreSQL을 클라우드 환경에서 활용하기로 결정했다. ElephantSQL은 'PostgreSQL as a Service'라는 컨셉 아래, 몇 가지 간단한 설정만으로 데이터베이스를 쉽게 구축하고 사용할 수 있게 해준다. AWS 기반으로 운영되는 이 서비스는 개발자들에게 최대 20MB의 데이터 저장 공간을 무료로 제공한다.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/cbf1c15e-91a6-4778-965c-386750619ba1/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4ZR4YPI%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T062609Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEI7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDhsxMnnJC8KkHbA5WeO61hDy8BqKjeRiFO69WQhMeJywIgLheAk7J779veRBGgCL4GNRpbowTZ3qwB27AxZPZDaNgqiAQI5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDF2g3%2FUeJ0YImrfFEircA1xmo5JCPFOU2mDKJo43lJKs2jitYA6xgBgHFCyEWVEMIz0hugnOc2RnYRDHKynzms8VmISAUg5TakDB6lJH55XDtb%2Bxesma6gMEzT8FhWZC6DJ8FlYTfCRgnuE0v28XzQAgBiokayJWTnEsvMS7TJZ4Svq7wmeusXZhBQKKaR8pgQkrvhuY4AIsUBxvhckdaUu1gKWRPv4Pei%2Blis2GxFNUiK2ULaVeP6ttR82MPxlj%2Bp7dRz2D0dNDFPLGWXASax72oqw99Njv36ljt1qOI1qpJiFV2j21i3mKRxxBC%2BJ3OmMKbhjxPdwUYsZffXA0XySN0LcJphUjlsLd2l4DVyu4dfSY5cJjp0Jt2kif32kLHwYZyhrA5zJQ7Bug34VB3UA0xMWMYLMDOvfkAN5PVVSk6kuWC9CvF%2F%2BijBrWWeCPqm04wvhCnC3AKqmauWb%2FK02NSB%2BCswhocISJ7WAEpLk3G3CZ9%2FUM0vprzjqJTvysKw27%2Fzwpk5TUGqlRRuwxR9iAu7hcvOP3TyFrFUZWIEuh49PMcUGBMYsx83ruW3hl4RnDwiATiS6vY0oRrf0K%2F3h%2Fan8zx%2FPk2ZH%2Bau2bxVzDvZQUj9Nvg0ypd7JJC7J5Dyz35oCEiDnA6mMZMInjg78GOqUBZ3VCx916FbEEnZkApDcp6cImYcryngEEGGcJVV45QROZwFbxD%2Bp4wOweMJMVFojs0gWl%2Ftrm3tEeQLd4ko%2Fbo6n7K8Ud4qyL%2B0kaKrwBlys5wCEDdL4wL16EGvzm1R9mJUqlQxRVn2v03%2Bud6Oa5sd5D0b0W0al%2FmSxErRNazpNBNJuZ9wMiyLRWpIVLYpoKUMSXFos2uuZUkFENqhDnNfL13L0p&X-Amz-Signature=7a303331d58fb209c42b61ebb34d74a04c64ce49c769b2f332adaf6e1dd1c439&X-Amz-SignedHeaders=host&x-id=GetObject)


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

![ElephantSQL에서 확인할 수 있는 DB세팅 정보](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/4c1c7fdd-c1db-48e0-8f05-e77688bac196/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466W4ZR4YPI%2F20250324%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250324T062609Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEI7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQDhsxMnnJC8KkHbA5WeO61hDy8BqKjeRiFO69WQhMeJywIgLheAk7J779veRBGgCL4GNRpbowTZ3qwB27AxZPZDaNgqiAQI5%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDF2g3%2FUeJ0YImrfFEircA1xmo5JCPFOU2mDKJo43lJKs2jitYA6xgBgHFCyEWVEMIz0hugnOc2RnYRDHKynzms8VmISAUg5TakDB6lJH55XDtb%2Bxesma6gMEzT8FhWZC6DJ8FlYTfCRgnuE0v28XzQAgBiokayJWTnEsvMS7TJZ4Svq7wmeusXZhBQKKaR8pgQkrvhuY4AIsUBxvhckdaUu1gKWRPv4Pei%2Blis2GxFNUiK2ULaVeP6ttR82MPxlj%2Bp7dRz2D0dNDFPLGWXASax72oqw99Njv36ljt1qOI1qpJiFV2j21i3mKRxxBC%2BJ3OmMKbhjxPdwUYsZffXA0XySN0LcJphUjlsLd2l4DVyu4dfSY5cJjp0Jt2kif32kLHwYZyhrA5zJQ7Bug34VB3UA0xMWMYLMDOvfkAN5PVVSk6kuWC9CvF%2F%2BijBrWWeCPqm04wvhCnC3AKqmauWb%2FK02NSB%2BCswhocISJ7WAEpLk3G3CZ9%2FUM0vprzjqJTvysKw27%2Fzwpk5TUGqlRRuwxR9iAu7hcvOP3TyFrFUZWIEuh49PMcUGBMYsx83ruW3hl4RnDwiATiS6vY0oRrf0K%2F3h%2Fan8zx%2FPk2ZH%2Bau2bxVzDvZQUj9Nvg0ypd7JJC7J5Dyz35oCEiDnA6mMZMInjg78GOqUBZ3VCx916FbEEnZkApDcp6cImYcryngEEGGcJVV45QROZwFbxD%2Bp4wOweMJMVFojs0gWl%2Ftrm3tEeQLd4ko%2Fbo6n7K8Ud4qyL%2B0kaKrwBlys5wCEDdL4wL16EGvzm1R9mJUqlQxRVn2v03%2Bud6Oa5sd5D0b0W0al%2FmSxErRNazpNBNJuZ9wMiyLRWpIVLYpoKUMSXFos2uuZUkFENqhDnNfL13L0p&X-Amz-Signature=305c978c5128bf87c216677971772dc032b532a3d11bab4a6060cb1403a42e42&X-Amz-SignedHeaders=host&x-id=GetObject)


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


