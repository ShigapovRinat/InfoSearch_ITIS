from urllib.request import urlopen
from bs4 import BeautifulSoup


def save(url):
    try:
        bs = BeautifulSoup(urlopen(url).read(), 'lxml')
        file = open('data/' + str(i) + ".html", 'a', encoding="utf-8")
        file.write(str(bs))
        file.flush()
        index.write(str(i) + ' ' + url + '\n')
        index.flush()
    except Exception:
        print('Exception in url: ' + url)


if __name__ == '__main__':
    mainUrl = 'https://www.litmir.me/br/?b=217310&p='
    index = open("data/index.txt", 'a')

    for i in range(1, 110):
        save(mainUrl + str(i))
