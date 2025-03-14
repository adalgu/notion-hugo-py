#!/usr/bin/env python3
"""
Hugo Runner with Preprocessing

이 스크립트는 Hugo 빌드를 실행하기 전에 전처리 과정을 수행하여
빌드 오류가 발생하는 파일을 자동으로 제외합니다.

실행 방법:
    python run_hugo.py [hugo 명령어 인자]

예:
    python run_hugo.py server
    python run_hugo.py --minify
"""

import os
import sys
import signal
import subprocess
from importlib.util import spec_from_file_location, module_from_spec
from typing import List, Optional

# 전역 변수로 전처리기 인스턴스를 저장하기 위한 변수
PROCESSOR = None

def load_preprocessor():
    """
    hugo_preprocess.py 모듈을 동적으로 로드합니다.
    """
    try:
        # 현재 디렉토리에서 hugo_preprocess.py 파일 경로 가져오기
        preprocessor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hugo_preprocess.py')
        
        # 모듈 로드
        spec = spec_from_file_location("hugo_preprocessor", preprocessor_path)
        preprocessor_module = module_from_spec(spec)
        spec.loader.exec_module(preprocessor_module)
        
        return preprocessor_module
    except Exception as e:
        print(f"전처리기 모듈 로드 실패: {str(e)}")
        sys.exit(1)

def ensure_preprocessor_executable():
    """
    전처리기 스크립트가 실행 가능한지 확인하고, 필요한 경우 권한을 설정합니다.
    """
    preprocessor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hugo_preprocess.py')
    
    # 실행 권한 확인 및 설정
    if not os.access(preprocessor_path, os.X_OK):
        try:
            # 실행 권한 추가
            current_mode = os.stat(preprocessor_path).st_mode
            os.chmod(preprocessor_path, current_mode | 0o111)  # 모든 사용자에게 실행 권한 추가
            print(f"전처리기 스크립트에 실행 권한을 추가했습니다: {preprocessor_path}")
        except Exception as e:
            print(f"권한 설정 실패: {str(e)}")
            # 실패해도 계속 진행 (모듈 로드 방식으로 동작 가능)

def signal_handler(sig, frame):
    """
    인터럽트 시그널(Ctrl+C) 처리 핸들러
    """
    print("\n인터럽트 시그널을 받았습니다. 정리 작업 수행 중...")
    
    # 전역 변수로 저장된 전처리기가 있다면 파일 복원 수행
    global PROCESSOR
    if PROCESSOR is not None:
        try:
            PROCESSOR._restore_files()
        except Exception as e:
            print(f"파일 복원 중 오류 발생: {str(e)}")
    
    # 종료
    sys.exit(130)  # 130은 SIGINT에 의한 종료를 나타내는 표준 종료 코드

def run_with_args(args: List[str]) -> int:
    """
    주어진 인수로 전처리기를 실행합니다.
    
    Args:
        args: 전달할 명령줄 인수
        
    Returns:
        종료 코드
    """
    # 전처리기 모듈 로드
    preprocessor = load_preprocessor()
    
    # 전처리기 인스턴스 생성 및 글로벌 변수에 저장
    global PROCESSOR
    PROCESSOR = preprocessor.HugoPreprocessor(args)
    
    # 시그널 핸들러 설정
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # 전처리기 실행
        return PROCESSOR.run()
    except KeyboardInterrupt:
        print("\n인터럽트 시그널을 받았습니다. 정리 작업 수행 중...")
        PROCESSOR._restore_files()
        return 130  # SIGINT에 의한 종료
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        PROCESSOR._restore_files()  # 오류 발생 시에도 파일 복원 시도
        return 1

def main():
    """메인 함수"""
    # 전처리기 스크립트 실행 권한 확인
    ensure_preprocessor_executable()
    
    # 명령줄 인수 처리 (첫 번째 인수는 스크립트 이름이므로 제외)
    hugo_args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 전처리기 실행
    result = run_with_args(hugo_args)
    
    # 종료 코드로 프로세스 종료
    sys.exit(result)

if __name__ == "__main__":
    main()
