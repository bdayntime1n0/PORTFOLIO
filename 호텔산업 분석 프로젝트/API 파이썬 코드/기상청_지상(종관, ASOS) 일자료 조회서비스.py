# http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList
# 기상청_지상(종관, ASOS) 일자료 조회서비스

# import requests
#
# import requests, bs4
# import pandas as pd
# from lxml import html
# from urllib.request import Request, urlopen

from urllib.parse import urlencode, quote_plus, unquote
import pandas
from bs4 import BeautifulSoup
import requests
from openpyxl.workbook import Workbook


def comment_print(comment):
    print()
    print('-------------- [' + comment + '] --------------')



# Service URL
base_url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
service_key = '?' + 'serviceKey=CoFlabV4zDnMX82ZFxmARJcUcZ2ostZA4PPRBQVG28PSJSipJWs%2FE5taPSm8tek1SuvgC00Zeochd0jisLseaQ%3D%3D&'

st_date = '20200401'
en_date = '20200410'

queryParams = urlencode(
    {
        quote_plus('pageNo') : '1',
        quote_plus('numOfRows') : '10',
        quote_plus('dataType') : 'XML',
        quote_plus('dataCd') : 'ASOS',
        quote_plus('dateCd') : 'DAY',
        quote_plus('startDt') : st_date,
        quote_plus('endDt') : en_date,
        quote_plus('stnIds') : 108
    }
)

url = base_url + service_key + queryParams

print(url)

req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')

comment_print('soup length')    # 아래 내용 제목 출력 //
print(len(soup))
# print(soup)


rows = soup.findAll('item')

comment_print('len(rows)')     # 아래 내용 제목 출력 //
print(len(rows))

comment_print('rows')     # 아래 내용 제목 출력 //
# print(rows)

# _________ [sample] ____________________
# <stnId>108</stnId>
# <stnNm>서울</stnNm>
# <tm>2010-01-01</tm>
# <avgTa>-7.6</avgTa>
# <minTa>-12.7</minTa>
# <minTaHrmt>654</minTaHrmt>
# <maxTa>-3.6</maxTa>
# <maxTaHrmt>1501</maxTaHrmt>
# <mi10MaxRn/>
# <mi10MaxRnHrmt/>
# <hr1MaxRn/>
# <hr1MaxRnHrmt/>
# <sumRnDur/>
# <sumRn/>
# <maxInsWs>7.5</maxInsWs>
# <maxInsWsWd>340</maxInsWsWd>
# <maxInsWsHrmt>105</maxInsWsHrmt>
# <maxWs>3.4</maxWs>
# <maxWsWd>70</maxWsWd>
# <maxWsHrmt>2350</maxWsHrmt>
# <avgWs>1.9</avgWs>
# <hr24SumRws>1608</hr24SumRws>
# <maxWd>70</maxWd>
# <avgTd>-16.9</avgTd>
# <minRhm>30</minRhm>

# _____________________________

# i = 0

# areanm = soup.findAll('areanm')
# comment_print('areanm')     # 아래 내용 제목 출력 //
# print(areanm)
# <areanm>기타</areanm>, <areanm>기타</areanm>, <areanm>기타</areanm>

# ____________ 항목별 데이터 저장 _________________

stnid = soup.findAll('stnid') # 지점 번호, 종관기상관측 지점 번호
stnnm = soup.findAll('stnnm') # 지역명
tm = soup.findAll('tm') # 일시
avgta = soup.findAll('avgta') # 평균기온

# _________ 저장용 배열 선언 ____________________
stnid_list       = []  # 배열 선언
stnnm_list          = []  # 배열 선언
tm_list             = []  # 배열 선언
avgta_list          = []  # 배열 선언


# ___________ 배열에 데이터 저장 __________
for code in stnid:       stnid_list.append(code.text)
for code in stnnm:       stnnm_list.append(code.text)
for code in tm:          tm_list.append(code.text)
for code in avgta:       avgta_list.append(code.text)




# ___  배열별 건수 인쇄 ____________
print('stnid_list: ',          len(stnid_list))
print('stnnm_list: ',          len(stnnm_list))
print('tm_list: ',               len(tm_list))
print('avgta_list: ',          len(avgta_list))



# _______  data frame 항목에 데이터 배정 __________________________

commerce_infor = {}
commerce_infor['stnid']        = stnid_list
commerce_infor['stnnm']        = stnnm_list
commerce_infor['tm']           = tm_list
commerce_infor['avgta']        = avgta_list


# _______  data frame 정의 __________________________

df = pandas.DataFrame(commerce_infor)
comment_print('df')
print(df.head(10))


# _______  파일로 저장 __________________________

comment_print('write to csv:기상청 일자료 조회')
df.to_csv('기상청 일자료 조회' + st_date + '_' + en_date + '.csv')

comment_print('write to excel:기상청 일자료 조회')
df.to_excel('기상청 일자료 조회' + st_date + '_' + en_date + '.xlsx')


# __________ 주의 사항 ____________________
# 확진자, 사망자는 누적 수치 임
# 영문명에 결측이 있음
# 기준일시가 03월, 3월 같이 0이 없는 경우도 있음.
# ________________________________________

# 항목명(국문)  항목명(영문)    항목크기   항목구분   샘플데이터  항목설명
# 결과코드     resultCode 2  필수 00 결과코드
# 결과메시지        resultMsg  50 필수 OK 결과메시지
# 한 페이지 결과 수   numOfRows  4  필수 10 한 페이지 결과 수
# 페이지 번호       pageNo 4  필수 1  페이지번호
# 전체 결과 수  totalCount 4  필수 3  전체 결과 수
# 게시글번호(국외발생현황 고유값)    SEQ    30 필수 96 게시글번호(국외발생현황 고유값)
# 기준일시     STD_DAY    30 필수 2020년 3월 09일 00시   기준일시
# 지역명          AREA_NM    30 필수 아프리카   지역명
# 지역명(영문)  AREA_NM_EN 30 필수 null   지역명(영문)
# 지멱명(중문)  AREA_NM_CN 30 필수 null   지멱명(중문)
# 국가명          NATION_NM  30 필수 토고 국가명
# 국가명(영문)  NATION_NM_EN   30 필수 null   국가명(영문)
# 국가명(중문)  NATION_NM_CN   30 필수 null   국가명(중문)
# 국가별 확진자 수    NAT_DEF_CNT    15 필수 0  국가별 확진자 수
# 국가별 사망자 수    NAT_DEATH_CNT  15 필수 0  국가별 사망자 수
# 확진률 대비 사망률   NAT_DEATH_RATE 30 필수 0  확진률 대비 사망률
# 등록일시분초   CREATE_DT  30 필수 2020-03-16 20:51:43.000    등록일시분초
# 수정일시분초   UPDATE_DT  30 필수 null   수정일시분초