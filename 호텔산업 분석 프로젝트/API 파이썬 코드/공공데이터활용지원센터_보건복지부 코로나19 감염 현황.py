# http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson
# 보건복지부 코로나19 감염 현황

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
base_url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
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
# <accDefRate>2.1424778525</accDefRate>
# <accExamCnt>503051</accExamCnt>
# <accExamCompCnt>487753</accExamCompCnt>
# <careCnt>3246</careCnt>
# <clearCnt>7117</clearCnt>
# <createDt>2020-04-10 10:15:54.54</createDt>
# <deathCnt>208</deathCnt>
# <decideCnt>10450</decideCnt>
# <examCnt>15298</examCnt>
# <resutlNegCnt>477303</resutlNegCnt>
# <seq>102</seq>
# <stateDt>20200410</stateDt>
# <stateTime>00:00</stateTime>
# <updateDt>2020-04-10 10:15:54.54</updateDt>
# _____________________________

# i = 0

# areanm = soup.findAll('areanm')
# comment_print('areanm')     # 아래 내용 제목 출력 //
# print(areanm)
# <areanm>기타</areanm>, <areanm>기타</areanm>, <areanm>기타</areanm>

# ____________ 항목별 데이터 저장 _________________

accdefrate = soup.findAll('accdefrate')  # 누적 확진률
accexamcnt = soup.findAll('accexamcnt') # 누적 검사 수
accexamcompcnt = soup.findAll('accexamcompcnt') # 누적 검사 완료 수
carecnt = soup.findAll('carecnt') # 치료중 호나자 수
clearcnt = soup.findAll('clearcnt') # 격리해제 수
deathcnt = soup.findAll('deathcnt') # 사망자 수
decidecnt = soup.findAll('decidecnt') # 확진자 수
examcnt = soup.findAll('examcnt') # 검사진행 수
resutlnegcnt = soup.findAll('resutlnegcnt')  # 결과 음성 수
statedt = soup.findAll('statedt') # 기준일




# _________ 저장용 배열 선언 ____________________
statedt_list       = []  # 배열 선언
decidecnt_list       = []  # 배열 선언
clearcnt_list       = []  # 배열 선언
examcnt_list    = []  # 배열 선언
deathcnt_list   = []  # 배열 선언
carecnt_list      = []  # 배열 선언
resutlnegcnt_list       = []  # 배열 선언
accexamcnt_list     = []  # 배열 선언
accexamcompcnt_list            = []  # 배열 선언
accdefrate_list         = []  # 배열 선언


# ___________ 배열에 데이터 저장 __________
for code in statedt:       statedt_list.append(code.text)
for code in decidecnt:       decidecnt_list.append(code.text)
for code in clearcnt:       clearcnt_list.append(code.text)

for code in examcnt:    examcnt_list.append(code.text)
for code in deathcnt:   deathcnt_list.append(code.text)
for code in carecnt:      carecnt_list.append(code.text)

for code in resutlnegcnt:       resutlnegcnt_list.append(code.text)
for code in accexamcnt:     accexamcnt_list.append(code.text)
for code in accexamcompcnt:            accexamcompcnt_list.append(code.text)
for code in accdefrate:         accdefrate_list.append(code.text)


# ___  배열별 건수 인쇄 ____________
print('statedt_list: ',          len(statedt_list))
print('decidecnt_list: ',        len(decidecnt))
print('clearcnt_list: ',        len(clearcnt_list))

print('examcnt_list: ',     len(examcnt_list))
print('deathcnt_list: ',    len(deathcnt_list))
print('carecnt_list: ',       len(carecnt_list))

print('resutlnegcnt_list: ',        len(resutlnegcnt_list))
print('accexamcnt_list: ',      len(accexamcnt_list))
print('accexamcompcnt_list: ',             len(accexamcompcnt_list))
print('accdefrate_list: ',          len(accdefrate_list))


# _______  data frame 항목에 데이터 배정 __________________________

commerce_infor = {}
commerce_infor['statedt']        = statedt_list
commerce_infor['decide_cnt']          = decidecnt_list
commerce_infor['clear_cnt']      = clearcnt_list

commerce_infor['exam_cnt']   = examcnt_list
commerce_infor['death_cnt']  = deathcnt_list
commerce_infor['care_cnt']     = carecnt_list

commerce_infor['resutlnegcnt']      = resutlnegcnt_list
commerce_infor['accexamcnt']    = accexamcnt_list
commerce_infor['accexamcompcnt']           = accexamcompcnt_list
commerce_infor['accdefrate']        = accdefrate_list


# _______  data frame 정의 __________________________

df = pandas.DataFrame(commerce_infor)
comment_print('df')
print(df.head(10))


# _______  파일로 저장 __________________________

comment_print('write to csv:ministry of health and welware covid19 infection dashboard')
df.to_csv('ministry of health and welware covid19 infection dashboard' + st_date + '_' + en_date + '.csv')

comment_print('write to excel:ministry of health and welware covid19 infection dashboard')
df.to_excel('ministry of health and welware covid19 infection dashboard' + st_date + '_' + en_date + '.xlsx')


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