import os
import sys
import argparse
from dotenv import load_dotenv

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import load_config
from src.notion_api import create_notion_client
from src.index import process_databases, process_pages, cleanup_orphaned_files, print_results

def main():
    """
    메인 함수 - 테스트 실행을 위한 진입점
    """
    parser = argparse.ArgumentParser(description='Notion to Hugo 변환 테스트')
    parser.add_argument('--config', type=str, help='설정 파일 경로')
    args = parser.parse_args()
    
    try:
        # 환경 변수 로드
        load_dotenv()
        
        if not os.environ.get('NOTION_TOKEN'):
            raise ValueError("NOTION_TOKEN 환경 변수가 설정되지 않았습니다")
        
        print("[Info] 테스트 시작")
        
        # 설정 로드
        config = load_config()
        print("[Info] 설정 로드 완료")
        
        # Notion 클라이언트 생성
        notion = create_notion_client()
        
        # 데이터베이스와 페이지 처리
        db_results = process_databases(notion, config)
        page_results = process_pages(notion, config)
        
        # 모든 페이지 ID와 결과 결합
        all_page_ids = db_results["page_ids"] + page_results["page_ids"]
        all_results = db_results["results"] + page_results["results"]
        
        # 고아 파일 정리
        cleanup_orphaned_files(all_page_ids)
        
        # 요약 출력
        print_results(all_results)
        
        print("[Info] 테스트 완료")
        
        # 변환 실패 시 오류 코드로 종료
        has_errors = any(len(result["errors"]) > 0 for result in all_results)
        if has_errors:
            sys.exit(1)
            
    except Exception as e:
        print(f"[Error] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
