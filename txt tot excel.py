####000000000000__PERFECT____

import openpyxl

# example.txt 파일 열기
with open('sample.txt', 'r') as f:
    lines = f.readlines()

# 태그-열 인덱스 매핑 정보
tag_mapping = {
    '[메모]': 1,
    '[대발문]': 2,
    '[대발문코드]': 3,
    '[문항수]': 4,
    '[지문]': 5,
    '[소문제문항수]': 6,
    '[문제]': 7,
    '[문항코드]': 8,
    '[선택지]': 9,
    '[정답]': 10,
    '[채점수식]': 11,
    '[해설]': 12,
    '[OMR뷰어]': 13
}

# 결과 엑셀 파일 작성
wb = openpyxl.Workbook()
ws = wb.active

# 헤더 추가
header = ['PK']
for tag in tag_mapping:
    header.append(tag[1:-1])
ws.append(header)

# 각 행에 데이터 추가x
row_data = [0]
current_row = 1
for line in lines:
    line = line.strip()
    if line.startswith('[메모]'):
        # Start of a new record
        row_data[0] = current_row
        ws.append(row_data)
        row_data = [current_row + 1] + [''] * len(tag_mapping)
        current_row += 1
    if line in tag_mapping:
        # Update tag data
        current_tag = line
    else:
        # Add text data to tag
        tag_index = tag_mapping.get(current_tag)
        if tag_index is not None:
            row_data[tag_index] += line + ' '

# Add the last row of data
row_data[0] = current_row
ws.append(row_data)

# 결과 저장
wb.save('123result.xlsx')
