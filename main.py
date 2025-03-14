import os
import sys
from dotenv import load_dotenv

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.notion_api import create_notion_client
from src.config import load_config
from src.helpers import iterate_paginated_api, ensure_directory
from src.markdown_converter import convert_blocks_to_markdown, create_hugo_frontmatter, sanitize_filename
from src.hugo_integration import ensure_hugo_structure

def main():
    """
    메인 함수 - Notion에서 Hugo로 콘텐츠를 변환합니다.
    """
    try:
        # 환경 변수 로드
        load_dotenv()
        
        # NOTION_TOKEN 환경 변수 확인
        if not os.environ.get('NOTION_TOKEN'):
            print("[Error] NOTION_TOKEN 환경 변수가 설정되지 않았습니다.")
            print("환경 변수 파일(.env)을 생성하고 NOTION_TOKEN=your_token을 추가하세요.")
            sys.exit(1)
        
        print("[Info] Notion에서 Hugo로 변환 시작")
        
        # 설정 로드
        config = load_config()
        print("[Info] 설정 로드 완료")
        
        # Notion 클라이언트 생성
        notion = create_notion_client()
        
        # Hugo 구조 확인
        ensure_hugo_structure()
        
        # 데이터베이스 처리
        process_databases(notion, config)
        
        # 페이지 처리
        process_pages(notion, config)
        
        print("[Info] 변환 완료")
        
    except Exception as e:
        print(f"[Error] {str(e)}")
        sys.exit(1)

def process_databases(notion, config):
    """
    설정된 Notion 데이터베이스의 페이지를 처리합니다.
    """
    print("[Info] 마운트된 데이터베이스 처리 시작")
    
    for mount in config['mount']['databases']:
        ensure_directory(f"content/{mount['target_folder']}")
        pages = []
        
        print(f"[Info] 데이터베이스 {mount['database_id']} 처리 중")
        
        # 데이터베이스의 모든 페이지 조회
        for page in iterate_paginated_api(notion.databases.query, {
            "database_id": mount['database_id']
        }):
            if page.get('object') != 'page':
                continue
                
            pages.append(page)
        
        if pages:
            print(f"[Info] 데이터베이스 {mount['database_id']}에서 {len(pages)}개 페이지 처리 중")
            for page in pages:
                process_page(notion, page, mount['target_folder'])

def process_pages(notion, config):
    """
    설정된 Notion 페이지를 처리합니다.
    """
    print("[Info] 마운트된 페이지 처리 시작")
    
    for mount in config['mount']['pages']:
        print(f"[Info] 페이지 {mount['page_id']} 처리 중")
        
        # 페이지 조회
        page = notion.pages.retrieve(page_id=mount['page_id'])
        
        if page.get('object') != 'page':
            print(f"[Warn] {mount['page_id']}는 유효한 페이지가 아닙니다.")
            continue
            
        process_page(notion, page, mount['target_folder'])

def process_page(notion, page, target_folder):
    """
    단일 Notion 페이지를 처리하고 Hugo 마크다운으로 변환합니다.
    """
    try:
        # 페이지가 보관 처리되었는지 확인
        if page.get('archived', False):
            print(f"[Info] 페이지 {page['id']}는 보관 처리되어 건너뜁니다.")
            return
        
        # 페이지 속성 추출
        properties = extract_page_properties(page)
        
        # 제목이 없으면 기본값 사용
        title = properties.get('title', 'Untitled')
        
        # 파일명 생성
        filename = sanitize_filename(title)
        
        # 대상 디렉토리 및 파일 경로 설정
        target_dir = f"content/{target_folder}"
        ensure_directory(target_dir)
        
        filepath = f"{target_dir}/{filename}.md"
        
        # 페이지 내용 가져오기
        blocks = list(iterate_paginated_api(notion.blocks.children.list, {'block_id': page['id']}))
        
        # 중첩된 블록 처리
        process_nested_blocks(notion, blocks)
        
        # 마크다운으로 변환
        markdown_content = convert_blocks_to_markdown(blocks)
        
        # 프론트매터 생성
        frontmatter = create_hugo_frontmatter(properties)
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"{frontmatter}\n\n{markdown_content}")
        
        print(f"[Info] 페이지 저장 완료: {filepath}")
        
    except Exception as e:
        print(f"[Error] 페이지 {page['id']} 처리 중 오류 발생: {str(e)}")

def process_nested_blocks(notion, blocks):
    """
    중첩된 블록을 재귀적으로 처리합니다.
    """
    for i, block in enumerate(blocks):
        if block.get('has_children', False):
            # 자식 블록 가져오기
            children = list(iterate_paginated_api(notion.blocks.children.list, {'block_id': block['id']}))
            
            # 자식 블록 처리
            process_nested_blocks(notion, children)
            
            # 원래 블록에 자식 블록 정보 추가
            blocks[i]['children'] = children

def extract_page_properties(page):
    """
    Notion 페이지의 속성을 추출합니다.
    """
    properties = {}
    page_properties = page.get('properties', {})
    
    for key, prop in page_properties.items():
        prop_type = prop.get('type')
        
        if prop_type == 'title':
            title_text = extract_rich_text(prop.get('title', []))
            properties['title'] = title_text
        
        elif prop_type == 'rich_text':
            text = extract_rich_text(prop.get('rich_text', []))
            properties[key.lower()] = text
        
        elif prop_type == 'date':
            date_obj = prop.get('date', {})
            if date_obj:
                start_date = date_obj.get('start')
                end_date = date_obj.get('end')
                
                if start_date:
                    properties[key.lower()] = start_date
                    if end_date:
                        properties[f"{key.lower()}_end"] = end_date
        
        elif prop_type == 'select':
            select_obj = prop.get('select', {})
            if select_obj and 'name' in select_obj:
                properties[key.lower()] = select_obj['name']
        
        elif prop_type == 'multi_select':
            multi_select = prop.get('multi_select', [])
            if multi_select:
                properties[key.lower()] = [item.get('name') for item in multi_select if 'name' in item]
        
        elif prop_type == 'checkbox':
            properties[key.lower()] = prop.get('checkbox', False)
        
        elif prop_type == 'url':
            properties[key.lower()] = prop.get('url', '')
        
        elif prop_type == 'email':
            properties[key.lower()] = prop.get('email', '')
        
        elif prop_type == 'phone_number':
            properties[key.lower()] = prop.get('phone_number', '')
        
        elif prop_type == 'number':
            properties[key.lower()] = prop.get('number')
    
    # 기본 메타데이터 추가
    properties['id'] = page.get('id')
    properties['created_time'] = page.get('created_time')
    properties['last_edited_time'] = page.get('last_edited_time')
    
    return properties

def extract_rich_text(rich_text):
    """
    Notion의 rich_text 배열에서 텍스트를 추출합니다.
    """
    result = ""
    
    for text_item in rich_text:
        result += text_item.get('plain_text', '')
    
    return result

if __name__ == "__main__":
    main()
