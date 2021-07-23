# openAPI / json 형식 적용
# 한국언론진흥재단_코로나19이후국민의일상변화조사_코로나19 이후 일상 활동 변화
jsonUrl = 'https://api.odcloud.kr/api/15077856/v1/uddi:15149cbe-7389-4a91-8d32-8bb5fb011a01?page=1&perPage=1000&serviceKey=vZ0A%2BJSgnpdhs1MeVIkwzFehZ50sIpCj%2BzrEInws%2B%2B%2BCuwkbT4KbestZ3oX%2Bbe9LPQlaGefjdXSaKFOeff9leg%3D%3D&returnType=JSON&numOfRows=1000&pageNo=1'

import json, urllib.request
import csv

data = urllib.request.urlopen(jsonUrl).read()
print('--------- data --------')
print(data)

output = json.loads(data)
print('--------- output --------')
print(output)

output = output['data']
print('--------- output2 --------')
print(output)

print('--------- type: output2 --------')
print(type(output))

# key 값 확인
print(output[0].keys())

# 출력할 csv 파일 명
output_file = '한국언론진흥재단_코로나19이후국민의일상변화조사_코로나19 이후 일상 활동 변화.csv'

try:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, output[0].keys())
        writer.writeheader()
        for data in output:
            writer.writerow(data)
except:
    print('Error')

# /