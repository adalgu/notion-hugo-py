import os
import yaml
from typing import Dict, List, Any, Optional, TypedDict
from fs import open_fs

class ContentFile(TypedDict):
    filepath: str
    metadata: Dict[str, Any]
    content: str

def get_all_content_files(content_dir: str) -> List[ContentFile]:
    """
    지정된 콘텐츠 디렉토리에서 모든 마크다운 파일을 찾아 반환합니다.
    
    Args:
        content_dir: 콘텐츠 디렉토리 경로
    
    Returns:
        ContentFile 객체 목록
    """
    content_files = []
    
    # 콘텐츠 디렉토리가 존재하는지 확인
    if not os.path.exists(content_dir):
        return content_files
    
    # 파일 시스템 열기
    fs = open_fs(f"osfs://{content_dir}")
    
    # 모든 마크다운 파일 찾기
    for path in fs.walk.files(filter=["*.md"]):
        try:
            # 파일 읽기
            with fs.open(path, 'r') as file:
                content = file.read()
            
            # 프론트매터와 콘텐츠 분리
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    content = parts[2]
                else:
                    frontmatter = {}
            else:
                frontmatter = {}
            
            # ContentFile 객체 생성
            content_file = {
                'filepath': os.path.join(content_dir, path),
                'metadata': frontmatter,
                'content': content
            }
            
            content_files.append(content_file)
        except Exception as e:
            print(f"[Error] 파일 {path} 처리 중 오류 발생: {e}")
    
    return content_files

def save_content_file(filepath: str, metadata: Dict[str, Any], content: str) -> None:
    """
    마크다운 파일을 저장합니다.
    
    Args:
        filepath: 저장할 파일 경로
        metadata: 프론트매터 메타데이터
        content: 파일 내용
    """
    # 디렉토리가 존재하는지 확인하고 없으면 생성
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # 프론트매터와 콘텐츠 결합
    frontmatter = yaml.dump(metadata, default_flow_style=False)
    file_content = f"---\n{frontmatter}---\n{content}"
    
    # 파일 저장
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(file_content)
