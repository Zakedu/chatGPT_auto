from PIL import Image, UnidentifiedImageError
from rembg import remove, new_session
from pathlib import Path
import imghdr
import cv2
import os

formats = [".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".ico"]
target_size = (744, 720)
target_dir = '/content/gdrive/My Drive/my_images0'
session = new_session()

for (path, dirs, files) in os.walk(target_dir):
    for file in files:
        if file.endswith(tuple(formats)):
            input_path = os.path.join(path, file)
            output_path = os.path.join(path, os.path.splitext(file)[0] + ".png")

            try:
                #rembg 모델 사용해서 배경 제거
                input = cv2.imread(input_path)
                output = remove(input)
                cv2.imwrite(output_path, output)

                # 이미지 수정 할 수 있도록 컨버팅
                im = Image.open(output_path)
                im = im.convert("RGBA")

                # 배경을 제거한 이미지의 가로세로 측정
                width, height = im.size
                size = max(width, height)

                #투명색 박스를 만들고
                square_img = Image.new("RGBA", (size,size), (255, 255, 255, 0))

                #이미지를 저장할 위치 지정
                left = (size - width) // 2
                right = (size - height) // 2

                #배경 제거한 이미지를 지정된 위치에 넣기
                square_img.paste(im, (left, right))

                #투명색 박스에 이미지를 넣은 결과물을 타겟 사이즈로 정리
                square_img = square_img.resize(target_size)

                # 투명색 박스에 이미지 넣고 저장
                square_img.save(output_path, "PNG")
                print(f"{file} is Re-Painted")

            except UnidentifiedImageError as e:
                print(f"어쩌다 되는 중 {e}")

