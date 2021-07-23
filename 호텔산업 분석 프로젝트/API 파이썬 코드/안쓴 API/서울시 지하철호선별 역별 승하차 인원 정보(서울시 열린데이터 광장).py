# http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19NatInfStateJson
# 서울시 지하철호선별 역별 승하차 인원 정보

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
#

def comment_print(comment):
    print()
    print('-------------- [' + comment + '] --------------')



# Service URL
base_url = 'http://openapi.seoul.go.kr:8088/5650445072716c7435394d63616a64/xml/CardSubwayStatsNew/'
service_key = '?' + 'serviceKey=5650445072716c7435394d63616a64&' #
# vZ0A%2BJSgnpdhs1MeVIkwzFehZ50sIpCj%2BzrEInws%2B%2B%2BCuwkbT4KbestZ3oX%2Bbe9LPQlaGefjdXSaKFOeff9leg%3D%3D

# service_key = '?' + 'serviceKey=K0xA0YEBm8bPUHpfpUMDrYBHOq8707meoRTCtZ2R%2FgDlRXvwH8oUp1jUvfiAIEkAvYJgBICirpKmTnRf5u1NtA%3D%3D&' # 강사님 키

# st_date = '20210501'
# en_date = '20210505'
startindex  = '1'
endindex = '500'
usedt = '20200505'

queryParams = urlencode(
    {
        # quote_plus('pageNo') : '1',
        # quote_plus('numOfRows') : '10',
        # quote_plus('startCreate_dt') : st_date,
        # quote_plus('endCreateDt') : en_date
        quote_plus('pageNo') : '1',
        quote_plus('numOfRows') : '10',
        quote_plus('startindex') : startindex,
        quote_plus('endindex') : endindex,
        quote_plus('usedt') : usedt

    }
)

url = base_url + startindex + '/' + endindex + '/' + usedt

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
# <areaNm>기타</areaNm>
# <areaNmEn>Others</areaNmEn>
# <createDt>2020-04-14 10:43:52.52</createDt>
# <natDeathCnt>0</natDeathCnt>
# <natDeathRate>0.0</natDeathRate>
# <natDefCnt>1</natDefCnt>
# <nationNm>생피에르미클롱</nationNm>
# <nationNmEn>Saint Pierre and Miquelon</nationNmEn>
# <seq>9521</seq>
# <stdDay>2020년 04월 14일 09시</stdDay>
# <updateDt/>
# _____________________________

# i = 0

# areanm = soup.findAll('areanm')
# comment_print('areanm')     # 아래 내용 제목 출력 //
# print(areanm)
# <areanm>기타</areanm>, <areanm>기타</areanm>, <areanm>기타</areanm>

# ____________ 항목별 데이터 저장 _________________ ##########

use_dt = soup.findAll(('use_dt')) # 사용날짜(이용한 날짜)
line_num = soup.findAll('line_num') # 호선명 (ex) 1호선, 2호선)
sub_sta_nm = soup.findAll('sub_sta_nm') # 역명
ride_pasgr_num = soup.findAll('ride_pasgr_num') # 승차 총 승객수
alight_pasgr_num = soup.findAll('alight_pasgr_num') # 하차 총 승객 수
work_dt = soup.findAll('work_dt') # 데이터 올린날짜


# _________ 저장용 배열 선언 ____________________ ###########

use_dt_list         = []  # 배열 선언
line_num_list       = []  # 배열 선언
sub_sta_nm_list       = []  # 배열 선언
ride_pasgr_num_list    = []  # 배열 선언
alight_pasgr_num_list   = []  # 배열 선언
work_dt_list      = []  # 배열 선언



# ___________ 배열에 데이터 저장 __________  ###########

for code in use_dt:         use_dt_list.append(code.text)
for code in line_num:       line_num_list.append(code.text)
for code in sub_sta_nm:       sub_sta_nm_list.append(code.text)

for code in ride_pasgr_num:    ride_pasgr_num_list.append(code.text)
for code in alight_pasgr_num:   alight_pasgr_num_list.append(code.text)
for code in work_dt:      work_dt_list.append(code.text)


# ___  배열별 건수 인쇄 ____________  ###########
print('use_dt_list: ',          len(use_dt_list))
print('line_num_list: ',        len(line_num_list))
print('sub_sta_nm_list: ',        len(sub_sta_nm_list))

print('ride_pasgr_num_list: ',     len(ride_pasgr_num_list))
print('alight_pasgr_num_list: ',    len(alight_pasgr_num_list))
print('work_dt_list: ',       len(work_dt_list))



# _______  data frame 항목에 데이터 배정 __________________________  ###########

commerce_infor = {}
commerce_infor['use_dt']        = use_dt_list
commerce_infor['line_num']          = line_num_list
commerce_infor['sub_sta_nm']      = sub_sta_nm_list

commerce_infor['ride_pasgr_num']   = ride_pasgr_num_list
commerce_infor['alight_pasgr_num']  = alight_pasgr_num_list
commerce_infor['work_dt']     = work_dt_list



# _______  data frame 정의 __________________________

df = pandas.DataFrame(commerce_infor)
comment_print('df')
print(df.head(10))


# _______  파일로 저장 __________________________

comment_print('write to csv:서울시 지하철호선별 역별 승하차 인원 정보')
df.to_csv('서울시 지하철호선별 역별 승하차 인원 정보_.csv')

comment_print('write to excel:서울시 지하철호선별 역별 승하차 인원 정보')
df.to_excel('서울시 지하철호선별 역별 승하차 인원 정보.xlsx')


# __________ 주의 사항 ____________________
# 확진자, 사망자는 누적 수치 임
# 영문명에 결측이 있음
# 기준일시가 03월, 3월 같이 0이 없는 경우도 있음.
# ________________________________________

# 항목명(국문)   항목명(영문)   항목크기   항목구분   샘플데이터   항목설명
# 결과코드       resultCode   2   필수   00   결과코드
# 결과메시지       resultMsg   50   필수   OK   결과메시지
# 한 페이지 결과 수   numOfRows   4   필수   10   한 페이지 결과 수
# 페이지 번호       pageNo   4   필수   1   페이지번호
# 전체 결과 수   totalCount   4   필수   3   전체 결과 수
# 게시글번호(국외발생현황 고유값)   SEQ   30   필수   96   게시글번호(국외발생현황 고유값)
# 기준일시       STD_DAY   30   필수   2020년 3월 09일 00시   기준일시
# 지역명           AREA_NM   30   필수   아프리카   지역명
# 지역명(영문)   AREA_NM_EN   30   필수   null   지역명(영문)
# 지멱명(중문)   AREA_NM_CN   30   필수   null   지멱명(중문)
# 국가명           NATION_NM   30   필수   토고   국가명
# 국가명(영문)   NATION_NM_EN   30   필수   null   국가명(영문)
# 국가명(중문)   NATION_NM_CN   30   필수   null   국가명(중문)
# 국가별 확진자 수   NAT_DEF_CNT   15   필수   0   국가별 확진자 수
# 국가별 사망자 수   NAT_DEATH_CNT   15   필수   0   국가별 사망자 수
# 확진률 대비 사망률   NAT_DEATH_RATE   30   필수   0   확진률 대비 사망률
# 등록일시분초   CREATE_DT   30   필수   2020-03-16 20:51:43.000   등록일시분초
# 수정일시분초   UPDATE_DT   30   필수   null   수정일시분초