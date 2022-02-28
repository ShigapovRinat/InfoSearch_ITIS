from urllib.request import urlopen
from bs4 import BeautifulSoup


def save(url):
    try:
        bs = BeautifulSoup(urlopen(url).read(), 'lxml')
        file = open('data/' + str(i) + ".html", 'a', encoding="utf-8")
        file.write(str(bs))
        file.flush()
        index.write(str(i-8471213) + ' ' + url + '\n')
        index.flush()
    except Exception:
        print('Exception in url: ' + url)


if __name__ == '__main__':
    mainUrl = 'https://www.nhl.com/player/'
    index = open("data/list.txt", 'a')

    for i in range(8471214, 8471350):
        save(mainUrl + str(i))
