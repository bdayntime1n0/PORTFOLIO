# http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson
# 보건복지부 코로나19 연령별·성별감염 현황

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
base_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19GenAgeCaseInfJson'
service_key = '?' + 'serviceKey=CoFlabV4zDnMX82ZFxmARJcUcZ2ostZA4PPRBQVG28PSJSipJWs%2FE5taPSm8tek1SuvgC00Zeochd0jisLseaQ%3D%3D&'

st_date = '20200401'
en_date = '20200410'

queryParams = urlencode(
    {
        quote_plus('pageNo') : '1',
        quote_plus('numOfRows') : '10',
        quote_plus('startCreateDt') : st_date,
        quote_plus('endCreateDt') : en_date
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
# <confCase>132</confCase>
# <confCaseRate>1.25</confCaseRate>
# <createDt>2020-04-14 10:24:23.23</createDt>
# <criticalRate>0</criticalRate>
# <death>0</death>
# <deathRate>0.00</deathRate>
# <gubun>0-9</gubun>
# <seq>145</seq>
# <updateDt>null</updateDt>
# _____________________________

# i = 0

# areanm = soup.findAll('areanm')
# comment_print('areanm')     # 아래 내용 제목 출력 //
# print(areanm)
# <areanm>기타</areanm>, <areanm>기타</areanm>, <areanm>기타</areanm>

# ____________ 항목별 데이터 저장 _________________

createdt = soup.findAll('createdt') # 날짜
gubun = soup.findAll('gubun') # 연령, 성별
confcase = soup.findAll('confcase') # 확진자 수
confcaserate = soup.findAll('confcaserate') # 확진율
death = soup.findAll('death') # 사망자 수
deathrate = soup.findAll('deathrate') #사망률
criticalrate = soup.findAll('criticalrate') #치명률



# _________ 저장용 배열 선언 ____________________
createdt_list       = []  # 배열 선언
gubun_list       = []  # 배열 선언
confcase_list       = []  # 배열 선언
confcaserate_list    = []  # 배열 선언
death_list   = []  # 배열 선언
deathrate_list      = []  # 배열 선언
criticalrate_list       = []  # 배열 선언


# ___________ 배열에 데이터 저장 __________
for code in createdt:       createdt_list.append(code.text)
for code in gubun:       gubun_list.append(code.text)
for code in confcase:       confcase_list.append(code.text)

for code in confcaserate:    confcaserate_list.append(code.text)
for code in death:   death_list.append(code.text)
for code in deathrate:      deathrate_list.append(code.text)

for code in criticalrate:       criticalrate_list.append(code.text)


# ___  배열별 건수 인쇄 ____________
print('createdt_list: ',          len(createdt_list))
print('gubun_list: ',        len(gubun_list))
print('confcase_list: ',        len(confcase_list))

print('confcaserate_list: ',     len(confcaserate_list))
print('death_list: ',    len(death_list))
print('deathrate_list: ',       len(deathrate_list))

print('criticalrate_list: ',        len(criticalrate_list))


# _______  data frame 항목에 데이터 배정 __________________________

commerce_infor = {}
commerce_infor['createdt']        = createdt_list
commerce_infor['gubun']          = gubun_list
commerce_infor['confcase']      = confcase_list

commerce_infor['confcaserate']   = confcaserate_list
commerce_infor['death']  = death_list
commerce_infor['deathrate']     = deathrate_list

commerce_infor['criticalrate']      = criticalrate_list


# _______  data frame 정의 __________________________

df = pandas.DataFrame(commerce_infor)
comment_print('df')
print(df.head(10))


# _______  파일로 저장 __________________________

comment_print('write to csv:보건복지부 코로나19 연령별, 성별 감염 현황')
df.to_csv('보건복지부 코로나19 연령별, 성별 감염 현황' + st_date + '_' + en_date + '.csv')

comment_print('write to excel:보건복지부 코로나19 연령별, 성별 감염 현황')
df.to_excel('보건복지부 코로나19 연령별, 성별 감염 현황' + st_date + '_' + en_date + '.xlsx')


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