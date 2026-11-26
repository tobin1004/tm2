import os
import sys
import shutil
import subprocess
import importlib.util

# 1. icrawler 설치 확인 (Pillow도 함께 설치됨)
if importlib.util.find_spec("icrawler") is None:
    print("icrawler 설치 중...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "icrawler"])

from icrawler.builtin import BingImageCrawler
from PIL import Image

# 2. 저장 위치: 스크립트 파일이 있는 폴더 안의 tm2_data (없으면 생성)
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:                      # 노트북 등 __file__이 없는 환경
    BASE_DIR = os.getcwd()

OUTPUT_DIR = os.path.join(BASE_DIR, "tm2_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)          # tm2_data 폴더가 없으면 생성
print("저장 위치:", OUTPUT_DIR)

# 3. 설정
LIMIT = 50                  # 클래스당 다운로드 시도 수
MIN_SIZE = (200, 200)       # 이보다 작은 이미지는 제외
CONVERT_TO_JPG = False      # True: png도 jpg로 변환 (모든 파일이 .jpg)

# 4. 클래스 이름(폴더명) : 검색어
targets = {
    "Dog":    "dog face close up",
    "Fox":    "fox face close up",
    "Rabbit": "rabbit face close up",

    "박보영": "박보영 얼굴 사진 단독",
    "한지민": "한지민 얼굴 사진 단독",
    "박보검": "박보검 얼굴 사진 단독",
    "송중기": "송중기 얼굴 사진 단독",
    "이주빈": "이주빈 얼굴 사진 단독",
    "전종서": "전종서 얼굴 사진 단독",
    "이준기": "이준기 얼굴 사진 단독",
    "서인국": "서인국 얼굴 사진 단독",
    "박은빈": "박은빈 얼굴 사진 단독",
    "장원영": "장원영 얼굴 사진 단독",
    "임시완": "임시완 얼굴 사진 단독",
    "최우식": "최우식 얼굴 사진 단독",
}


def organize(raw_dir, save_dir):
    """raw_dir의 이미지 중 jpg/png만 골라 000001.jpg 형태로 save_dir에 저장"""
    count = 0
    for name in sorted(os.listdir(raw_dir)):
        path = os.path.join(raw_dir, name)
        ext = None

        try:
            with Image.open(path) as img:
                fmt = img.format
                size = img.size
                if fmt not in ("JPEG", "PNG"):
                    continue
                if size[0] < MIN_SIZE[0] or size[1] < MIN_SIZE[1]:
                    continue

                count += 1
                if CONVERT_TO_JPG:
                    dst = os.path.join(save_dir, f"{count:06d}.jpg")
                    img.convert("RGB").save(dst, "JPEG", quality=95)
                else:
                    ext = "jpg" if fmt == "JPEG" else "png"
        except Exception:
            continue                    # 깨진 파일은 건너뜀

        # 파일이 닫힌 뒤 이동 (Windows 필수)
        if ext:
            dst = os.path.join(save_dir, f"{count:06d}.{ext}")
            shutil.move(path, dst)

    return count


# 5. 클래스별 다운로드 + 정리
for folder, keyword in targets.items():
    save_dir = os.path.join(OUTPUT_DIR, folder)
    raw_dir = os.path.join(save_dir, "_raw")

    # 다시 실행해도 번호가 꼬이지 않도록 해당 클래스 폴더만 비우고 시작
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.makedirs(raw_dir, exist_ok=True)         # tm2_data/클래스명/_raw 생성

    print(f"\n[{folder}] 다운로드 중: {keyword}")
    crawler = BingImageCrawler(storage={"root_dir": raw_dir})
    crawler.crawl(keyword=keyword, max_num=LIMIT, min_size=MIN_SIZE)

    saved = organize(raw_dir, save_dir)
    shutil.rmtree(raw_dir, ignore_errors=True)  # 임시 폴더 삭제
    print(f"  → [{folder}] 저장: {saved}장")

print("\n이미지 다운로드 완료:", OUTPUT_DIR)