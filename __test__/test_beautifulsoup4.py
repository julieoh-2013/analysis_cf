from bs4 import BeautifulSoup
html ='<td class ="title"><div class ="tit3"> '\
      '<a href = "/movie/bi/mi/basic.nhn?code=159892" title = "탐정: 리턴즈"> 탐정: 리턴즈 </a>'\
      '</div> </td> '

# 1 태그조회
def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    print('bs : ', bs)
    tag = bs.td
    print(tag.div)

    print(tag)

    tab = bs.a
    print(tag)
    print(tag.name)

def ex2():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.td
    print(tag['class'])

    tag = bs.div
    # print(tag['id'])  #없으면 에러

    print(tag.attrs)
    #attr 값

    #3.attribute 조회

def ex3():
    bs = BeautifulSoup(html, 'html.parser')
    tag= bs.find('td', attrs={'class':'title'})
    print(tag)

    tag = bs.find( attrs={'class': 'tit3'})
    print(tag)

if __name__=='__main__':
    ex1()