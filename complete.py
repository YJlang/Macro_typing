import os
from PIL import ImageGrab
import keyboard
from google.cloud import vision
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
# OCR.json 파일의 경로 설정
ocr_json_path = os.path.join(script_dir, 'OCR.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ocr_json_path

# OCR을 수행할 이미지 파일 경로
image_file = "my_region.png"

# 스크린샷 찍을 영역의 좌상단과 우하단 좌표 설정
x1, y1, x2, y2 = 658, 722, 1261, 769
screenshot_region = (x1, y1, x2, y2)

def perform_ocr_and_typing(image_file):
    # 스크린샷 찍기
    screenshot = ImageGrab.grab(bbox=screenshot_region)
    screenshot.save(image_file)

    # Google Cloud Vision API에 이미지 전송하여 텍스트 추출
    client = vision.ImageAnnotatorClient()
    with open(image_file, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    extracted_text = texts[0].description if texts else "레슬링이여 영원하라 Made - by 강은율,정민우"
    if not texts:
        print("Made-by 강은율,정민우 A.K.A 알고리즘 shot out to 레슬링")

    # 추출된 텍스트를 자동으로 타이핑 (글자 간의 간격을 위해 시간 지연 추가)
    for char in extracted_text:
        keyboard.write(char)
        #time.sleep(0.000001)

# 모든 키 입력을 감지하여 'insert' 키가 입력되면 OCR 및 타이핑 함수 호출
def on_key_press(event):
    if event.name == 'insert':
        perform_ocr_and_typing(image_file)

# 키보드 이벤트 핸들러 등록
keyboard.on_press_key('insert', on_key_press)

# 프로그램 실행 중단을 방지하기 위해 무한루프
keyboard.wait("esc")  # esc 키가 눌릴 때까지 대기