import collection.crawler as cw

def my_error(e):
    print("myerror:",e)
'''
result = cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nh',
         encoding='cp949',
         err=my_error  #자기함수넣으면 자기거 실행 안넣으면 람다디폴트실행
         )
'''
result = cw.crawling(url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
         encoding='cp949'
         )
print(result)


