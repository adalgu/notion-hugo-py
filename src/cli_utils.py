"""
CLI 유틸리티 모듈

이 모듈은 대화형 CLI 인터페이스를 위한 유틸리티 함수를 제공합니다.
사용자 입력, 메뉴 표시, ID 검증 등의 기능을 담당합니다.
"""

import re
import sys
import json
from typing import Dict, Any, List, Optional, Union, Tuple, Callable

def clear_screen() -> None:
    """터미널 화면을 지웁니다."""
    print("\033c", end="")

def print_header(title: str, width: int = 60) -> None:
    """
    강조된 헤더를 출력합니다.
    
    Args:
        title: 표시할 제목
        width: 헤더 전체 너비
    """
    print("\n" + "=" * width)
    padding = (width - len(title)) // 2
    print(" " * padding + title)
    print("=" * width + "\n")

def print_step(step: str, description: str) -> None:
    """
    단계 정보를 출력합니다.
    
    Args:
        step: 단계 번호나 제목
        description: 단계 설명
    """
    print(f"\n[{step}] {description}")
    print("-" * 60)

def print_info(message: str) -> None:
    """
    정보 메시지를 출력합니다.
    
    Args:
        message: 표시할 메시지
    """
    print(f"ℹ️  {message}")

def print_success(message: str) -> None:
    """
    성공 메시지를 출력합니다.
    
    Args:
        message: 표시할 메시지
    """
    print(f"✅ {message}")

def print_warning(message: str) -> None:
    """
    경고 메시지를 출력합니다.
    
    Args:
        message: 표시할 메시지
    """
    print(f"⚠️  {message}")

def print_error(message: str) -> None:
    """
    오류 메시지를 출력합니다.
    
    Args:
        message: 표시할 메시지
    """
    print(f"❌ {message}")

def ask_yes_no(question: str, default: bool = True) -> bool:
    """
    예/아니오 질문을 표시하고 응답을 받습니다.
    
    Args:
        question: 질문 내용
        default: 기본값 (True: 예, False: 아니오)
        
    Returns:
        사용자 선택 결과 (True: 예, False: 아니오)
    """
    default_text = "[Y/n]" if default else "[y/N]"
    while True:
        response = input(f"{question} {default_text}: ").strip().lower()
        
        if not response:
            return default
        
        if response in ["y", "yes", "예"]:
            return True
        elif response in ["n", "no", "아니오"]:
            return False
            
        print_warning("'y' 또는 'n'으로 응답해주세요.")

def ask_input(prompt: str, default: Optional[str] = None, validator: Optional[Callable[[str], bool]] = None) -> str:
    """
    사용자 입력을 받습니다.
    
    Args:
        prompt: 입력 프롬프트
        default: 기본값 (선택 사항)
        validator: 입력값 검증 함수 (선택 사항)
        
    Returns:
        사용자 입력 문자열
    """
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        response = input(prompt).strip()
        
        if not response and default:
            response = default
        
        if not response:
            print_warning("값을 입력해주세요.")
            continue
            
        if validator and not validator(response):
            print_warning("유효하지 않은 입력입니다. 다시 시도해주세요.")
            continue
            
        return response

def show_menu(title: str, options: List[str]) -> int:
    """
    번호가 있는 메뉴를 표시하고 선택을 받습니다.
    
    Args:
        title: 메뉴 제목
        options: 메뉴 옵션 목록
        
    Returns:
        선택한 옵션의 인덱스 (0부터 시작)
    """
    print(f"\n{title}")
    print("-" * 60)
    
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    
    print()
    
    while True:
        try:
            choice = int(input("번호를 선택하세요: "))
            if 1 <= choice <= len(options):
                return choice - 1
            print_warning(f"1부터 {len(options)} 사이의 번호를 입력해주세요.")
        except ValueError:
            print_warning("유효한 번호를 입력해주세요.")

def is_notion_page_id(id_str: str) -> bool:
    """
    문자열이 노션 페이지 ID 형식인지 확인합니다.
    
    Args:
        id_str: 확인할 ID 문자열
        
    Returns:
        유효한 페이지 ID 여부
    """
    # 노션 페이지 ID 패턴: 32글자의 16진수, 선택적으로 하이픈으로 구분
    # 예: 8a021de72bda434db255d7cc94ebb567 또는 8a021de7-2bda-434d-b255-d7cc94ebb567
    pattern = r'^[a-f0-9]{8}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{4}-?[a-f0-9]{12}$'
    return bool(re.match(pattern, id_str.lower()))

def is_notion_database_id(id_str: str) -> bool:
    """
    현재 구현에서는 페이지 ID와 데이터베이스 ID의 형식이 동일합니다.
    추후 차별화가 필요할 경우 실제 API 호출로 검증하는 로직 추가 필요.
    
    Args:
        id_str: 확인할 ID 문자열
        
    Returns:
        유효한 데이터베이스 ID 여부
    """
    return is_notion_page_id(id_str)

def extract_notion_id_from_url(url: str) -> Optional[str]:
    """
    노션 URL에서 ID를 추출합니다.
    
    Args:
        url: 노션 URL
        
    Returns:
        추출된 ID 또는 None
    """
    # 노션 URL 패턴들
    patterns = [
        r'https?://(?:www\.)?notion\.so/(?:[^/]+/)?([a-f0-9]{32})',
        r'https?://(?:www\.)?notion\.so/(?:[^/]+/)?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def format_notion_id(id_str: str) -> str:
    """
    노션 ID를 표준 형식(하이픈 포함)으로 변환합니다.
    
    Args:
        id_str: 정규화할 ID 문자열
        
    Returns:
        정규화된 ID 문자열
    """
    # 하이픈 제거
    clean_id = re.sub(r'[^a-f0-9]', '', id_str.lower())
    
    # UUID 형식으로 변환
    if len(clean_id) == 32:
        return f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
    
    # 형식이 맞지 않으면 원래 문자열 반환
    return id_str

def print_id_info(id_type: str, id_value: str, url: Optional[str] = None) -> None:
    """
    ID 정보를 출력합니다.
    
    Args:
        id_type: ID 유형 (예: "데이터베이스", "페이지")
        id_value: ID 값
        url: 연결 URL (선택 사항)
    """
    formatted_id = format_notion_id(id_value)
    print(f"\n{id_type} ID: {formatted_id}")
    if url:
        print(f"{id_type} URL: {url}")
