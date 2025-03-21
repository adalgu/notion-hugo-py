from typing import Dict, List, Any, Callable, TypeVar, Generator, Iterator, Optional
import os

T = TypeVar('T')

def iterate_paginated_api(api_method: Callable, args: Dict[str, Any]) -> Generator[Any, None, None]:
    """
    페이지네이션이 있는 Notion API 메서드를 반복하는 제너레이터 함수입니다.
    
    Args:
        api_method: 호출할 Notion API 메서드
        args: API 메서드에 전달할 인자
    
    Yields:
        API 응답의 각 결과 항목
    """
    has_more = True
    start_cursor = None
    
    while has_more:
        if start_cursor:
            args['start_cursor'] = start_cursor
        
        response = api_method(**args)
        
        for result in response.get('results', []):
            yield result
        
        has_more = response.get('has_more', False)
        start_cursor = response.get('next_cursor')

def is_full_page(page: Dict[str, Any]) -> bool:
    """
    주어진 객체가 완전한 Notion 페이지인지 확인합니다.
    
    Args:
        page: 확인할 Notion 페이지 객체
    
    Returns:
        완전한 페이지인 경우 True, 그렇지 않은 경우 False
    """
    return (
        isinstance(page, dict) and
        page.get('object') == 'page' and
        'id' in page and
        'properties' in page
    )

def is_full_block(block: Dict[str, Any]) -> bool:
    """
    주어진 객체가 완전한 Notion 블록인지 확인합니다.
    
    Args:
        block: 확인할 Notion 블록 객체
    
    Returns:
        완전한 블록인 경우 True, 그렇지 않은 경우 False
    """
    return (
        isinstance(block, dict) and
        block.get('object') == 'block' and
        'id' in block and
        'type' in block and
        block['type'] in block
    )

def ensure_directory(directory_path: str) -> None:
    """
    디렉토리가 존재하는지 확인하고, 없으면 생성합니다.
    
    Args:
        directory_path: 확인할 디렉토리 경로
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
