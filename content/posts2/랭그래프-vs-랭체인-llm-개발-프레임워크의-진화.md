---
title: "랭그래프 vs. 랭체인 : LLM 개발 프레임워크의 진화"
lastmod: 2025-03-12T02:22:00.000Z
author: ""
description: "대규모 언어 모델(LLM) 기반 애플리케이션 개발이 급증하면서 랭체인(LangChain)과 랭그래프(LangGraph)가 주목받고 있습니다. 이 글에서는 두 프레임워크의 특징, 차이점, 그리고 실제 적용 사례를 살펴봅니다. AutoGPT와의 유사성을 통해 각 프레임워크를 이해하고, 나스닥 지수 분석 및 포트폴리오 최적화 예제를 통해 LangGraph의 실용성을 확인해보세요."
notion_id: "a063422b-25be-4986-a0ee-9e94ab71c275"
---

## AI 개발의 새로운 지평

인공지능 기술의 급속한 발전으로 대규모 언어 모델(LLM)을 활용한 애플리케이션 개발이 폭발적으로 증가하고 있습니다. 이러한 흐름 속에서 LLM 개발을 위한 프레임워크도 빠르게 진화하고 있는데, 오늘은 그 중 가장 주목받고 있는 랭체인(LangChain)과 랭그래프(LangGraph)에 대해 알아보겠습니다.

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/a7818b90-aed3-4bac-bfe2-f6dd54d4b94b/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466ZVJRCD4U%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044722Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIGP6oNNFZxvTpcSPdFrtcYIKka2eIP%2B69z4r6cb3MQyjAiEAs2m1qVZr%2BOJDDpjoRtaDIyZwIJS78PMnk1cQlFww6c8qiAQI5f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDEOcz2RTe5TuM3GP5CrcA9VRCIKqqXk6YjIrmz8me%2BBR5vGWCXl49FFnp44l8jBjDu8L4XMFt8K4Wnc21e8DTfla0VFvKd7u62OMKLi%2BdzkFv0tWeaNV6vpd%2FUx1MmARMTOky9G5vN9oG1UFYMkR%2Fl%2FKTAkHAR5uO2aIdhSuEdidKyIXGFvOAgjqGTqvka35VPnVVaB7zDHkR%2BZ9pzKeq3aq7IVrDhimuDfdcUrphQo6oRC8UIYfFVHQUSUl2l7aYE3KY84777NGdFUHmWinNOI3yQpKxNKFMLpz%2B%2F7pLB021Q0JvI7f8upUxZzLIIYAryXSkZPz%2FgerYDd4dMDRsM9ELhA3DLy7f9lqKc3bZQ3%2Fs8NOCNXGhGjVL52v1C0iqzU5SQob8uzi1pVDmnPIFuOlItammfB6Rgc9jiA70BLd0K8Na%2FXor75MDmZRS6PSWGflEf5q%2Bgd3k2QQWsxi%2F9nKsq8YPheDQQeVMj9PkqbvUxhU7trHmIfzJN65cVgLQdBLKDBaxDi2wDyExqySJMYhCO7ddsqTBuSLQV7BZy8aHjI3IYcVUje%2FVlbA3%2FVxOFq%2FmWYeA%2FF4fZ2ZhkiQ5wdobx7I9AIomUr7BQmZxvBOO1Cl1rtMQ%2FEtvhZ55SziUzaoD2yq0kTlwq1RMPvMzr4GOqUBdX4PHux5oAQO4YHG1LyA%2BvcbR8qYG3nhmQC%2FsXY59vEtHBhTtIHvevbC3yOxucZ%2FiZl6yA7I4I0blMdj7AWjWGt1nR9Csn%2FE86p7DzEpUFyzTwhcrkJlgGWbGwbqnaKFV26Qm0nIf4IaznEfHnvJSNyj5mt5XigrYF4BSTtyDqQNzds6j2P9%2BdZ%2F7AMCwklGy1BblvzPf1yIg7JWd7l%2F5tc70iP8&X-Amz-Signature=bb7d35a94fccf1158e232dbbacbd43ae90fed39a97e0f51dd80648d55d373b01&X-Amz-SignedHeaders=host&x-id=GetObject)

![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/bc41caab-fb96-4302-b0f8-9c591c1444f2/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4663PCMRYUM%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044722Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIEY4VNx8nY2w2SmJt7x%2FFnGQJzpAAk%2BxGPnWOqdYA1CUAiBhluk7pPXUXDu9Fc9Y6eohGu4xAk3c2DHfQtYnG0MZkCqIBAjl%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIM0zO%2FvYB8rATwkJImKtwDmHUAWiY8jKvSGO7oYWJpsUZFh%2BCYIKsoc7AKsSvsmtYWyVTw8vPibaWCBM5jkf%2FMC%2FAL9ITFWluNRqLbsnQ9hgIPaPWl1FrWATgXNk44OtI1ZRoP5vHoQDXt7dOT3Y04cZbgLnLHLP8PbHEJQyf63KaWEf2YSaCKhG2vfip%2FWZUF41QX%2BdrxnBP1ppFmdCXUsdiDR5suww0VvazWRvH0%2FInsBsjAbixpK64rZ17kj5k7hraQCh%2FLvIpg%2Bm8iyhGkOZM4CCLQDIBkjRbafFBOKLRlFEb80QR%2F%2Bf5eTDrbrnxPuYs677bgp99PL7T7A56nMMw%2FkcBuYl06KfH7KDJsCU7Q119xUmflm4yzQskP4thBxm%2Fg50iuvHVbWM7u%2FIwIgKDU9mSubfmKP%2FhCPVzwntKYOujFZWT9bRQ34gTZd4UVDdy16ZexlhDkyu9P6CLJPnz9SIjo0jyCZ8QmGv3w6hFNcVJrQw9Im0lEconC3D1jyE%2B6jYW6I7Pth8CvvCzNkWd8RR1c3gQsLaJDP80BX3B8dRMHm5x4Elxuh90MihsbazMAUMn3%2BAQdojzT0dY7aLwwvnWlH8ouQ3wo7izpWYlzng8RvrI2YrUvy0g1wrg6fKo1%2BbpWtbNbx3Yw38zOvgY6pgF8Pis8MgdIdMrtEtsCVTT47qp%2FjIq9K78r0hbvnudKi%2FT3QzYlrC0bYsEjA%2BOR3OT0A35%2BUdkE3BZyY%2Fp4v8u69JRofU8ORxmH131h6S8nmeqYcpFhxtvuZSFG3QKEOLmd7QjHhbaqtj5Q67PKRwmxI1EcGWTzzo2PyfMqskQMEN6VdROX7H0S5DmppusGvKrPjcKspSAfqLWhVdLp%2Fgd2dUh2U6kC&X-Amz-Signature=fe41289d769bd0f4905b6eacf605734bd791c346c733cc044e6a63ba28bca060&X-Amz-SignedHeaders=host&x-id=GetObject)

랭그래프(LangGraph)는 대규모 언어 모델(LLM)을 사용하여 복잡한 시스템을 구축하기 위한 Python 라이브러리입니다. 이는 랭체인(LangChain) 프레임워크의 일부로, 다음과 같은 특징을 가지고 있습니다:

1. 상태 관리: 복잡한 대화 및 작업 흐름에서 상태를 관리합니다.
1. 그래프 기반 구조: 노드와 엣지를 사용하여 작업 흐름을 정의합니다.
1. LLM 통합: 대규모 언어 모델과 쉽게 통합됩니다.
1. 유연한 워크플로우: 복잡한 대화 시스템이나 다단계 작업을 모델링할 수 있습니다.
1. 재사용 가능한 컴포넌트: 다양한 애플리케이션에서 재사용할 수 있는 컴포넌트를 만들 수 있습니다.

LangGraph는 주로 다음과 같은 상황에서 사용됩니다:

- 복잡한 대화형 AI 시스템 구축
- 다단계 추론이 필요한 작업 자동화
- 동적인 의사결정 트리 구현
- AI 에이전트 시스템 개발

이 라이브러리를 사용하면 개발자들이 더 쉽게 복잡한 AI 시스템을 구축하고 관리할 수 있습니다. LangGraph는 상태 기계의 개념을 LLM과 결합하여, 더 강력하고 유연한 AI 애플리케이션을 만들 수 있게 해줍니다.

## 랭그래프와 랭체인 비교

랭체인은 구성 요소들을 직선으로 연결하여 작업을 처리하는 기차와 같습니다. 각 칸(구성 요소)이 순차적으로 연결되어 있어, 작업이 진행됨에 따라 각 칸을 거쳐가게 됩니다. 반면 랭그래프는 여러 노드(에이전트)들이 협업하여 작업을 수행하는 네트워크입니다. 각 노드가 서로 연결되어 있어, 필요에 따라 다양한 경로를 통해 작업을 처리할 수 있습니다.

## 

## 랭체인(LangChain): LLM 개발의 기초

### 랭체인의 정의와 용도

랭체인은 언어 모델 기반의 애플리케이션을 개발하기 위한 프레임워크입니다. 쉽게 말해, LLM을 사용한 프로그래밍을 더 쉽고 효율적으로 할 수 있게 도와주는 도구라고 볼 수 있습니다.

랭체인을 사용하면 다음과 같은 다양한 애플리케이션을 만들 수 있습니다:

- 챗봇 또는 개인 비서
- 문서나 구조화된 데이터에 대한 Q&A 시스템
- 코드 작성 및 이해
- API와의 상호작용
- 그 외 다양한 생성형 AI 애플리케이션

### 랭체인의 주요 특징

랭체인의 핵심 특징은 모듈성과 유연성입니다. 랭체인은 다음과 같은 6개의 주요 모듈로 구성되어 있습니다:

1. **모델 I/O**: 언어 모델과의 인터페이스
1. **데이터 연결**: 애플리케이션별 데이터와의 인터페이스
1. **체인**: 호출 시퀀스 구축
1. **에이전트**: 상위 지시문에 따라 체인이 사용할 도구를 선택
1. **메모리**: 체인 실행 간의 애플리케이션 상태 유지
1. **콜백**: 체인의 중간 단계를 기록 및 스트리밍

이러한 모듈식 구조 덕분에 개발자는 필요한 기능만을 선택적으로 사용하거나 조합할 수 있어 매우 유연한 개발이 가능합니다.


![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/523e3f34-0c33-4912-97e9-9fc80ef6199b/DALLE_2024-07-03_17.45.13_-_A_visual_representation_of_LangChain_framework_with_interconnected_modules_labeled__Model_I_O_Data_Connection_Chain_Agent_Memory_Callback_depict.webp?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664CMXMMRF%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044721Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIHiR%2B1GsE5IoIRZAjYj95jep%2FcP3xARpS7OD6i1IUGNDAiEA6GEz3jbqugV2lRiI8WJjk6%2FHJe9Z7L8b1xBT4h4fgAAqiAQI5f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDJ%2BrV9Nq%2FiVM9bzzqyrcAw4f6ft2vFthDPHGIXdXJrTSB%2FHCHeZg%2BvVQfwXX5POTYy8EpPWLi8e2ahnmSUZdhcbeL6bxSQVKnFrBerq%2Fd3LrEiMJXR4sQL%2BuRDJqkJTVaEuYP%2BbZ5W9vYhVdlvYHGCuajqBP9WY1zOYI5Y8qT3UMlfsE3rKG4%2BpnIgiGK%2BTonuVlRoIdHe%2FVFFPy5e8%2FR9lA5hJz%2Bf1UqirxD23VN0Fom0mzMmktNmyFMi6VSFAlmbwSIScYqEwe7cPvA9JR5d9CxBWgagBXVoTN8VR%2FrF%2Fc9JEGPl8O3P65AXjtmACvQYMYBc%2FZCzELRhHBNnuSBwix%2FuTv7OfwsWeuTUCU%2FnG%2F3%2BXok%2FdjnyCjqMHcXEECUSEdzdzBHodobrxpzOKfe8k8XJIxchKdMT5cYoE7iJHJEzK39xbHCpaCq992y2MOL3qgw%2BQksCuWG0TGr0LCn69QLJg7EbAl2fJ44qVtzLvjtKJJ6UI%2BevfMNhd4CO9RTt%2BYvyyNIPToDuFwhjRrJfjhL8uVfhMp%2BzF9EuMJ4gHDO%2B%2FbkUKdQrWjgpSy4MzobHU%2F5I6hk2I08J3icOMNte%2FPVr7DK%2FWy53aPH3g5JsS2I6FS%2BxK6tuzPzNWrzpyu7r5G%2FxG8PHRXLC%2BRMM3Mzr4GOqUB%2BBZg5tbwHPjpCVzP2qIf1kdW6dkQGwI4z0YLsXFIuJ7yCLPjwjAd5pVM1tB9KTZAdXP6D4DiFYO6uVb1LxfnOg3yn%2FcVtAy9r6h3RblpI2wroXGfMw9%2FJBSw3KUHPXeBtVXGi3x%2FciIo907EHZJoZDFu7PxkTfFFgtWqItWrgGmTv45SO7Axe1ILJ4tdKAJphmqdDLER6Ye%2FBbRLFKGb89kUNkRa&X-Amz-Signature=6e0023768737c4dca5a5f8d3211dc113cbc2a27d7207ee909b6d23f3f5ea5caf&X-Amz-SignedHeaders=host&x-id=GetObject)

## 랭그래프(LangGraph): LLM 개발의 진화

### 랭그래프의 정의와 특징

랭그래프는 랭체인의 확장 버전 또는 보완적인 프레임워크로 볼 수 있습니다. 랭그래프는 LLM 애플리케이션의 복잡한 워크플로우를 그래프 구조로 모델링하고 관리하는 데 특화되어 있습니다.

랭그래프의 주요 특징은 다음과 같습니다:

1. **사이클 기반 구조**:
- 랭그래프의 가장 큰 특징은 사이클을 가진다는 점입니다.
- 기존의 멀티 에이전트 시스템이 단순히 여러 에이전트를 무작위로 활용하는 것과 달리, 랭그래프는 명확한 흐름도를 가지고 있습니다.
1. **글로벌 상태 관리**:
- 랭그래프는 글로벌 상태(State)를 정의하고, 이를 여러 에이전트가 공유할 수 있게 합니다.
- 이를 통해 전체 시스템의 일관성을 유지하고 효율적인 정보 공유가 가능합니다.
1. **조건부 실행**:
- 랭그래프는 특정 조건에 따라 다른 에이전트를 실행할 수 있는 유연성을 제공합니다.
- 이를 통해 상황에 따른 동적인 워크플로우 구성이 가능합니다.
1. **시각화**:
- 랭그래프는 복잡한 워크플로우를 그래프 형태로 시각화할 수 있어, 전체 프로세스를 쉽게 이해하고 관리할 수 있습니다.



![](https://prod-files-secure.s3.us-west-2.amazonaws.com/94f51666-273a-443d-bf89-42827b5b6876/f505dde8-35df-451f-9e76-a06117ee2ec3/Untitled.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4664CMXMMRF%2F20250314%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20250314T044721Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIHiR%2B1GsE5IoIRZAjYj95jep%2FcP3xARpS7OD6i1IUGNDAiEA6GEz3jbqugV2lRiI8WJjk6%2FHJe9Z7L8b1xBT4h4fgAAqiAQI5f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDJ%2BrV9Nq%2FiVM9bzzqyrcAw4f6ft2vFthDPHGIXdXJrTSB%2FHCHeZg%2BvVQfwXX5POTYy8EpPWLi8e2ahnmSUZdhcbeL6bxSQVKnFrBerq%2Fd3LrEiMJXR4sQL%2BuRDJqkJTVaEuYP%2BbZ5W9vYhVdlvYHGCuajqBP9WY1zOYI5Y8qT3UMlfsE3rKG4%2BpnIgiGK%2BTonuVlRoIdHe%2FVFFPy5e8%2FR9lA5hJz%2Bf1UqirxD23VN0Fom0mzMmktNmyFMi6VSFAlmbwSIScYqEwe7cPvA9JR5d9CxBWgagBXVoTN8VR%2FrF%2Fc9JEGPl8O3P65AXjtmACvQYMYBc%2FZCzELRhHBNnuSBwix%2FuTv7OfwsWeuTUCU%2FnG%2F3%2BXok%2FdjnyCjqMHcXEECUSEdzdzBHodobrxpzOKfe8k8XJIxchKdMT5cYoE7iJHJEzK39xbHCpaCq992y2MOL3qgw%2BQksCuWG0TGr0LCn69QLJg7EbAl2fJ44qVtzLvjtKJJ6UI%2BevfMNhd4CO9RTt%2BYvyyNIPToDuFwhjRrJfjhL8uVfhMp%2BzF9EuMJ4gHDO%2B%2FbkUKdQrWjgpSy4MzobHU%2F5I6hk2I08J3icOMNte%2FPVr7DK%2FWy53aPH3g5JsS2I6FS%2BxK6tuzPzNWrzpyu7r5G%2FxG8PHRXLC%2BRMM3Mzr4GOqUB%2BBZg5tbwHPjpCVzP2qIf1kdW6dkQGwI4z0YLsXFIuJ7yCLPjwjAd5pVM1tB9KTZAdXP6D4DiFYO6uVb1LxfnOg3yn%2FcVtAy9r6h3RblpI2wroXGfMw9%2FJBSw3KUHPXeBtVXGi3x%2FciIo907EHZJoZDFu7PxkTfFFgtWqItWrgGmTv45SO7Axe1ILJ4tdKAJphmqdDLER6Ye%2FBbRLFKGb89kUNkRa&X-Amz-Signature=0137e9ca95abee2f07b7af658b4251958ebcfdbc897230ac41302545e66a8d24&X-Amz-SignedHeaders=host&x-id=GetObject)

## AutoGPT를 통한 랭체인과 랭그래프의 이해

### AutoGPT 소개

AutoGPT에 대해 모르시는 분들을 위해 간단히 설명드리겠습니다. AutoGPT는 GPT-4와 같은 대규모 언어 모델을 사용하여 자동으로 작업을 수행하는 AI 에이전트입니다. 사용자가 목표를 제시하면, AutoGPT는 그 목표를 달성하기 위해 필요한 단계들을 자동으로 계획하고 실행합니다. 예를 들어, 웹 검색, 데이터 분석, 코드 작성 등 다양한 작업을 연속적으로 수행할 수 있습니다.

### 랭체인과 AutoGPT의 유사성

랭체인은 AutoGPT의 기본 도구 세트와 유사합니다:

- 검색 도구, 코드 실행 도구, 데이터 분석 도구 등 다양한 도구(모듈)를 제공합니다.
- 각 도구는 독립적으로 사용할 수도 있고, 여러 도구를 순서대로 사용해 복잡한 작업을 수행할 수도 있습니다.
- AutoGPT가 다양한 기능을 조합해 작업을 수행하는 것처럼, 랭체인도 다양한 모듈을 조합해 AI 애플리케이션을 구축할 수 있습니다.

### 랭그래프와 AutoGPT의 유사성

랭그래프는 AutoGPT의 작업 계획 및 실행 프로세스와 유사합니다:

- AutoGPT가 목표를 달성하기 위해 여러 단계의 작업을 계획하고 실행하는 것처럼, 랭그래프는 복잡한 AI 워크플로우를 그래프 형태로 모델링하고 실행합니다.
- 각 작업 단계를 노드로, 단계 간의 전환을 엣지로 표현하여 전체 프로세스를 시각화하고 관리할 수 있습니다.
- AutoGPT가 작업 진행 상황을 계속 추적하고 업데이트하는 것처럼, 랭그래프도 글로벌 상태를 통해 전체 프로세스의 상태를 관리합니다.

## 랭그래프의 장점

랭그래프는 다음과 같은 주요 장점을 제공합니다:

1. **유연성**:
- 복잡한 AI 워크플로우를 유연하게 설계할 수 있습니다.
- 필요에 따라 노드를 추가하거나 엣지를 조정하여 프로세스를 쉽게 변경할 수 있습니다.
1. **재사용성**:
- 한 번 설계한 워크플로우의 일부를 다른 프로젝트에서 쉽게 재사용할 수 있습니다.
- 이는 개발 시간을 크게 단축시키고 효율성을 높일 수 있습니다.
1. **디버깅 용이성**:
- 그래프 구조로 인해 각 단계별로 실행 결과를 확인하고 디버깅하기 쉽습니다.
- 문제가 발생한 정확한 지점을 쉽게 파악하고 수정할 수 있습니다.
1. **확장성**:
- 새로운 기능이나 도구를 추가하기 쉬워, 시스템을 지속적으로 개선하고 확장할 수 있습니다.
- 이는 빠르게 변화하는 AI 기술 환경에 대응하기 위해 중요한 특성입니다.

## 랭그래프 실제 적용 사례: 나스닥 지수 분석 및 포트폴리오 최적화

랭그래프를 사용한 실제 예제를 살펴보겠습니다. 이 예제는 나스닥 지수를 조회하고 포트폴리오 최적화를 위한 시그널을 생성하는 과정을 보여줍니다:

1. **초기 설정**:
- 금융 데이터 API 키 설정 (예: Yahoo Finance, Alpha Vantage)
- 필요한 라이브러리 임포트 (pandas, numpy, matplotlib, yfinance 등)
1. **에이전트 생성**:
- 데이터 수집 에이전트: 나스닥 지수 및 관련 주식 데이터 수집 담당
- 분석 에이전트: 수집된 데이터 분석 및 기술적 지표 계산 담당
- 시그널 생성 에이전트: 분석 결과를 바탕으로 매매 시그널 생성 담당
- 포트폴리오 최적화 에이전트: 시그널을 바탕으로 포트폴리오 구성 최적화 담당
1. **도구 정의**:
- 금융 데이터 API 호출기: 실시간 주가 및 지수 데이터 조회
- 파이썬 코드 실행기: 데이터 처리, 기술적 분석, 시각화 수행
- 머신러닝 모델: 시계열 예측 및 패턴 인식에 활용
1. **워크플로우 정의**:
- 그래프 구조로 에이전트들의 작업 순서와 조건 정의
- 조건부 엣지를 사용하여 시장 상황에 따른 다양한 분석 흐름 설계
- 주기적인 데이터 업데이트 및 재분석 루프 구현
1. **실행 및 결과**:
- 사용자 입력: "나스닥 지수 분석 및 포트폴리오 최적화 시그널 생성"
- 데이터 수집 에이전트가 최근 나스닥 지수 및 주요 구성 주식 데이터 수집
- 분석 에이전트가 기술적 지표 (예: 이동평균, RSI, MACD) 계산
- 시그널 생성 에이전트가 분석 결과를 바탕으로 매매 시그널 생성
- 포트폴리오 최적화 에이전트가 현재 포트폴리오 구성 조정 제안
- 최종 결과로 시각화된 차트, 매매 시그널, 포트폴리오 조정 제안 출력

이 예제는 랭그래프가 어떻게 복잡한 금융 분석 작업을 여러 단계로 나누고, 각 단계를 효율적으로 관리하는지 보여줍니다. 또한 실시간 데이터 처리, 복잡한 분석 로직, 그리고 결과에 따른 의사결정 과정을 유연하게 구현할 수 있음을 보여줍니다.

## 결론: LLM 개발의 미래

랭체인과 랭그래프는 각각의 장점을 가진 LLM 개발 프레임워크입니다. 랭체인은 모듈식 접근으로 다양한 애플리케이션 개발에 유연성을 제공하며, 랭그래프는 복잡한 워크플로우를 효과적으로 관리할 수 있게 해줍니다.

AutoGPT와의 유사성을 고려하면, 랭그래프는 마치 '프로그래머블한 AutoGPT'를 만드는 도구라고 볼 수 있습니다. 개발자가 직접 AI 시스템의 '두뇌'를 설계하고, 각 단계에서 어떤 판단과 행동을 할지 정의할 수 있게 해줍니다.

프로젝트의 특성과 복잡도에 따라 적절한 프레임워크를 선택하거나, 두 프레임워크를 함께 사용하여 LLM 기반의 강력한 애플리케이션을 개발할 수 있습니다. 앞으로 이러한 프레임워크들이 더욱 발전하여 AI 애플리케이션 개발을 더욱 쉽고 효율적으로 만들어줄 것으로 기대됩니다.

랭체인과 랭그래프는 AI 개발의 새로운 지평을 열고 있습니다. 이러한 도구들을 통해 개발자들은 더욱 복잡하고 강력한 AI 시스템을 구축할 수 있게 되었고, 이는 곧 우리의 일상생활과 산업 전반에 혁신적인 변화를 가져올 것입니다. AI 기술에 관심 있는 개발자라면 이 두 프레임워크에 대해 깊이 있게 학습하고 실제 프로젝트에 적용해 보는 것을 강력히 추천합니다.

