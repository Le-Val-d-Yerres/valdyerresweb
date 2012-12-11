import requests,lxml,unicodedata
import time,hashlib
from lxml import etree
from datetime import date, datetime, timedelta


class alcScreening:
    def __init__(self):
        self.id_allocine_film =""
        self.date_debut = ""
        self.date_fin = ""
        self.format = ""
        self.vo = False
        

class alcMovie:
    def __init__(self):
        self.id_allocine_film =""
        self.urlallocine = ""
        self.title = ""
        self.urlimage =""
        self.duration = ""


tabmovies = {}
tabseances = list()

urlparadiso = "http://api.allocine.fr/rest/v3/showtimelist?partner=YW5kcm9pZC12M3M&format=xml&theaters=B0203"
response =  requests.get(urlparadiso)
data = response.text.encode('utf-8')


hash_cine = hashlib.sha1()
hash_cine.update(data)
print hash_cine.hexdigest()

tree = etree.fromstring(data)
tree = etree.ElementTree(tree)
movies = tree.findall("//{http://www.allocine.net/v6/ns/}movieShowtimes")

for movie in movies:
    mynsmap = {}
    mynsmap['bob'] = movie.nsmap[None]
    mymovie = alcMovie()
    movieid = movie.xpath("./bob:onShow/bob:movie",namespaces = mynsmap)
    movieid = movieid[0].attrib['code']
   
    if not movieid in tabmovies:
        mymovie.id_allocine_film = movieid
        title  = movie.xpath("./bob:onShow/bob:movie/bob:title",namespaces = mynsmap)
        urlimage = movie.xpath("./bob:onShow/bob:movie/bob:poster",namespaces = mynsmap)
        duration = movie.xpath("./bob:onShow/bob:movie/bob:runtime",namespaces = mynsmap)
        mymovie.title = title[0].text
        mymovie.urlimage = urlimage[0].attrib['href']
        mymovie.duration = duration[0].text
        tabmovies[mymovie.id_allocine_film] = mymovie

    movieformat = movie.xpath("./bob:screenFormat",namespaces = mynsmap)[0].text
    version_lang = movie.xpath("./bob:version",namespaces = mynsmap)[0].text
    version_vo = movie.xpath("./bob:version",namespaces = mynsmap)[0].attrib['original']
    screenings = movie.xpath("./bob:screenings",namespaces = mynsmap)

    for scrdate in screenings[0]:
        thedate = scrdate.attrib['d']
        for thetime in scrdate:
            thescreening = alcScreening()
            thescreening.id_allocine_film = movieid
            thescreening.format = movieformat
            thescreening.version_lang = version_lang
            if version_vo == "true":
                thescreening.version_vo = True
            else:
                thescreening.version_vo = False
            thescreening.date_debut = datetime.strptime(thedate+" "+thetime.text,"%Y-%m-%d %H:%M")
            delta = timedelta(seconds = int(tabmovies[movieid].duration))
            thescreening.date_fin = thescreening.date_debut + delta
            tabseances.append(thescreening)
