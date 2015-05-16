import requests as r
from bs4 import BeautifulSoup as bs

def urlworker(url, actor_dic, year):
    year = year.strip('(').strip(')').strip()
    if not int(year) >= inp:
        return

    movie = r.get(url)
    movieSoup = bs(movie.text)
    cast_list = movieSoup.find('table', 'cast_list')
    cast = [ x.text for x in cast_list.find_all('span', class_ = 'itemprop', itemprop = 'name') ]
    for actor in cast:
        if actor in actor_dic:
            actor_dic[actor] += 1
        else:
            actor_dic[actor] = 1
    return actor_dic

def main():
    inp = input('From year:\n')
    inp = int(inp)
    top = input('Top what or type 0 for all:\n')
    top = int(top)
    print('......Working.......')
    actor_dic = {}# key actor name, value = number of movies he was in
    URL = r'http://www.imdb.com'
    urlback = r'chart/top'
    website = r.get(URL + '/' + urlback)
    soup = bs(website.text)
    lis = [ URL + x.a['href'] for x in soup.table('td', class_ = 'titleColumn') ]
    lis2 = [ x.text for x in soup.find_all('span', class_ = 'secondaryInfo') ]
    for a in range(len(lis)):
        year = lis2[a].strip('(').strip(')').strip()
        if not int(year) >= inp:
            continue
        movie = r.get(lis[a])
        movieSoup = bs(movie.text)
        cast_list = movieSoup.find('table', 'cast_list')
        cast = [ x.text for x in cast_list.find_all('span', class_ = 'itemprop', itemprop = 'name') ]
        for actor in cast:
            if actor in actor_dic:
                actor_dic[actor] += 1
            else:
                actor_dic[actor] = 1
    lista = []
    for x,v in actor_dic.items():
        lista.append((x,v))
    ret = sorted(lista, key=lambda x: (-x[1],x[0]))
    if int(top) and int(top) <= len(ret):
        for counter in range(top):
            print(ret[counter][0], 'acted in', ret[counter][1], 'movie/s')
    else:
        for actor in ret:
            print(actor[0], 'acted in', actor[1], 'movies')
    print('done')
main()