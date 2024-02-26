import os
import glob
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pandas as pd
from datetime import datetime


pic_list = []
pic_name_list = []
take_info_list = []

print("이미지 메타데이터를 추출하는 프로그램입니다")
print("아래에 폴더 경로를 입력해주세요")
upper_path = input().replace("'", "").replace('"', "")

# 지정한 폴더 내의 jpg, jpeg, png 파일을 모두 찾습니다.
for filetype in ['*.jpg', '*.jpeg', '*.png']:
    pic_list.extend(glob.glob(os.path.join(upper_path, filetype)))

length_list = len(pic_list)

i = 0
for pic in pic_list:
    i = i + 1
    print(str(length_list) + "중 " + str(i) + "번째 항목 작업중")
    pic_name = os.path.basename(pic)
    image = Image.open(pic)
    exifdata = image._getexif()
    take_date = None
    if exifdata is not None:
        # 사진 찍은 날짜는 'DateTimeOriginal' 태그에 저장되어 있습니다.
        for tag, value in exifdata.items():
            if TAGS.get(tag) == 'DateTimeOriginal':
                take_date = value
    # 찍은 날짜가 없는 경우에는 'None'을 append 합니다.
    if take_date is None:
        take_date = "데이터 없음"
    take_info_list.append(take_date)
    pic_name_list.append(pic_name)

# pic_list 와 take_info 를 dataframe 에 넣습니다.
df = pd.DataFrame({'파일명': pic_name_list, '촬영일': take_info_list})

# 데이터프레임을 엑셀 파일로 변환하여 저장합니다.
user = os.getlogin()
now = datetime.now()
datetime_str = str(now.strftime("%y%m%d%H%M"))
final_path = "C:\\Users\\" + user + "\\Desktop\\exif추출_" + datetime_str + ".xlsx"
print(final_path, "에 저장됩니다")
df.to_excel(final_path, index=False)

a = input("엔터 입력 시 종료됩니다")
