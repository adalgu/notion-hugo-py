import os
from dotenv import load_dotenv
from notion_client import Client

def create_notion_client():
    """
    Notion API 클라이언트를 생성합니다.
    
    Returns:
        Notion API 클라이언트 객체
    
    Raises:
        ValueError: NOTION_TOKEN 환경 변수가 설정되지 않은 경우
    """
    # 환경 변수 로드
    load_dotenv()
    
    # NOTION_TOKEN 환경 변수 확인
    notion_token = os.environ.get('NOTION_TOKEN')
    if not notion_token:
        raise ValueError("NOTION_TOKEN 환경 변수가 설정되지 않았습니다.")
    
    # Notion 클라이언트 생성
    return Client(auth=notion_token)

def get_database_pages(notion_client, database_id):
    """
    Notion 데이터베이스의 모든 페이지를 가져옵니다.
    
    Args:
        notion_client: Notion API 클라이언트
        database_id: 데이터베이스 ID
    
    Returns:
        데이터베이스의 페이지 목록
    """
    pages = []
    
    # 데이터베이스 쿼리
    response = notion_client.databases.query(database_id=database_id)
    
    # 모든 페이지 수집
    pages.extend(response['results'])
    
    # 페이지네이션 처리
    while response.get('has_more', False):
        response = notion_client.databases.query(
            database_id=database_id,
            start_cursor=response['next_cursor']
        )
        pages.extend(response['results'])
    
    return pages

def get_page_content(notion_client, page_id):
    """
    Notion 페이지의 내용을 가져옵니다.
    
    Args:
        notion_client: Notion API 클라이언트
        page_id: 페이지 ID
    
    Returns:
        페이지 내용 블록 목록
    """
    blocks = []
    
    # 페이지 블록 가져오기
    response = notion_client.blocks.children.list(block_id=page_id)
    
    # 모든 블록 수집
    blocks.extend(response['results'])
    
    # 페이지네이션 처리
    while response.get('has_more', False):
        response = notion_client.blocks.children.list(
            block_id=page_id,
            start_cursor=response['next_cursor']
        )
        blocks.extend(response['results'])
    
    # 중첩된 블록 처리
    for i, block in enumerate(blocks.copy()):
        if block.get('has_children', False):
            child_blocks = get_page_content(notion_client, block['id'])
            # 원래 블록에 자식 블록 정보 추가
            blocks[i]['children'] = child_blocks
    
    return blocks

def get_database_schema(notion_client, database_id):
    """
    Notion 데이터베이스의 스키마 정보를 가져옵니다.
    
    Args:
        notion_client: Notion API 클라이언트
        database_id: 데이터베이스 ID
    
    Returns:
        데이터베이스 스키마 정보
    """
    # 데이터베이스 정보 가져오기
    database = notion_client.databases.retrieve(database_id=database_id)
    
    # 속성 정보 추출
    properties = database.get('properties', {})
    
    schema = {}
    for name, prop in properties.items():
        schema[name] = prop['type']
    
    return schema
