import urllib
from itertools import count
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import collection.crawler as cw
from collection.data_dict import sido_dict, gungu_dict

RESULT_DIRECTORY='__result__/crawling'
def crawling_pelicana():
    results=[]
    for page in count(start=1):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?&gu=&si=&page=%d' % page
        html = cw.crawling(url=url)

        bs = BeautifulSoup(html, 'html.parser')

        tag_table = bs.find('table', attrs={'class':'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')
        #끝 검출
        if len(tags_tr) == 0:
            break
        #print(page,   len(tags_tr), sep=':')

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]

            results.append((name,address) + tuple(sidogu)) # 변경불가
    #store
    table = pd.DataFrame(results, columns=['name','address','sido','gungu'])

    table['sido'] = table.sido.apply(lambda v : sido_dict.get(v,v))  #딕셔너리의 v의 값가져오고 없으면 v리턴
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/pelicana_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True
    )


def proc_nene(xml):
    root = et.fromstring(xml)

    results=[]
    for el in root.findall('item'):
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')
        results.append((name, address, sido, gungu))
    return results


def store_nene(data):
    table = pd.DataFrame(data, columns=['name','address','sido','gungu'])

    table['sido'] = table.sido.apply(lambda v : sido_dict.get(v,v))  #딕셔너리의 v의 값가져오고 없으면 v리턴
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/nene_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True
    )

# kyochon
def crawling_kyochon():

    sido1 = [
            '서울','부산','대구','인천','광주','대전','울산','세종','경기',
            '강원','충북','충남','전북','전남','경북','경남','제주'
            ]
    results=[]
    for sido1 in range(1, 18):
       # for sido2 in count(start=1):
       for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d' %(sido1,sido2)
            html = cw.crawling(url=url)

            if html is None:
                break
            else:
                try:
                    bs = BeautifulSoup(html, 'html.parser')
                    # div-ul-li-<dl><dt><dd>
                    tag_div = bs.find('div', attrs={'class': 'shopSchList'})
                    tag_ul = tag_div.find('ul')
                    tags_li = tag_ul.findAll('li')

                    for tag_li in tags_li:
                        strings = list(tag_li.strings)

                        name = strings[3]
                        address = str(strings[5]).strip()
                        sidogu = address.split()[:2]
                        results.append((name, address) + tuple(sidogu))  # 변경불가
                        table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
                        table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
                        table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

                        # store
                        table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY),
                                     encoding='utf-8',
                                     mode='w',
                                     index='True'
                                     )
                except Exception as e:
                    print(e)
                    pass

# kyochon_table.csv (name, address, sido, gungu)

#파싱 dt, dd tag
#


if __name__== '__main__':
    #페리카나 pelicana
    #crawling_pelicana()

    # nene
    '''
    cw.crawling(
        url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'%(urllib.parse.quote('전체'),urllib.parse.quote('전체')),
        proc=proc_nene,
        store=store_nene
    )
    '''
    crawling_kyochon()

'''
def my_error(e):
    print("myerror:",e)

def proc(html) :
    print("processing :",html)

def store(result):
    pass

cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
         encoding='cp949',
         proc=proc ,     #필터처리함수 만들어 넣음
         store=store

         )
         
         
result = cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nh',
         encoding='cp949',
         err=my_error  #자기함수 넣으면 자기거 실행 안넣으면 람다디폴트실행
         )

result = cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
         encoding='cp949',
         proc=proc      #필터처리함수 만들어 넣음
         )

result = cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
         encoding='cp949',
         proc=proc ,     #필터처리함수 만들어 넣음
         store=store
         )
result = cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
         encoding='cp949'
         )

'''