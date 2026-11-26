# 1. 필요한 라이브러리 가져오기
import sys
import subprocess
import importlib.util

# 2. google_images_download 설치 여부 확인
if importlib.util.find_spec("google_images_download") is None:

    print("google_images_download 라이브러리가 없습니다.")
    print("라이브러리 설치를 시작합니다.")

    # 현재 실행 중인 Python 환경에 라이브러리 설치
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "google_images_download"
    ])

    print("라이브러리 설치가 완료되었습니다.")

else:
    print("google_images_download 라이브러리가 이미 설치되어 있습니다.")


# 3. Google 이미지 다운로드 라이브러리 가져오기
from google_images_download import google_images_download

# 4. Google 이미지 다운로드 객체 생성
response = google_images_download.googleimagesdownload()

# 5. 이미지 다운로드 옵션 설정
arguments = {

    # 검색할 이미지 키워드
    "keywords": "이효리, 장원영",
    
    # 다운로드할 이미지 최대 개수
    "limit": 20,

    # 이미지 URL 출력 여부
    "print_urls": True,

    # 이미지 파일 형식
    "format": "jpg"
}

# 6. 이미지 검색 및 다운로드 실행
paths = response.download(arguments)

# 7. 다운로드 결과 출력
print("\n이미지 다운로드 결과:")
print(paths)




