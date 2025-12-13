"""
✅ pytest가 tests 폴더에서 실행되어도
프로젝트 루트(C:/project)를 import 경로(sys.path)에 추가해주는 설정 파일
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
