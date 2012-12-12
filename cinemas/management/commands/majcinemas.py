# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from cinemas.models import Cinema,Film,Seance
import requests,lxml,unicodedata
import time,hashlib
from lxml import etree
from datetime import date, datetime, timedelta
from pytz import timezone
from valdyerresweb import settings
from PIL import Image, ImageFile
from StringIO import StringIO
from django.template import defaultfilters
import os

myTimezone = timezone(settings.TIME_ZONE)
utcTZ = timezone("UTC")
#patch à la noix : http://stackoverflow.com/questions/6788398/how-to-save-progressive-jpeg-using-python-pil-1-1-7
ImageFile.MAXBLOCK = 2**20


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        cinemas = Cinema.objects.all()
        cinemas.order_by('nom')
        
        for cinema in cinemas:
            url_api_alcn = "http://api.allocine.fr/rest/v3/showtimelist?partner=YW5kcm9pZC12M3M&format=xml&theaters="+cinema.id_allocine_cine
            response = None
            try :
                response =  requests.get(url_api_alcn, timeout= 5 )
            except requests.exceptions.Timeout:
                exit()
            
            data = response.text.encode('utf-8')
            
            hash_cine = hashlib.sha1()
            hash_cine.update(data)
             
            if hash_cine.hexdigest() == cinema.hash_maj:
                continue
            

            seances_to_delete = Seance.objects.select_related().filter(cinema__id = cinema.id)
            films_to_delete = Film.objects.filter(seance__cinema__id = cinema.id)
            films_to_delete.query.group_by = ["id"]
            
            
            
            
            for movie in films_to_delete:
                try:
                    filepath = settings.MEDIA_ROOT+movie.image.name
                    os.remove(filepath)
                except Exception,e:
                    print e
                movie.delete()
            
            seances_to_delete.delete()
            tree = etree.fromstring(data)
            tree = etree.ElementTree(tree)
            movies = tree.findall("//{http://www.allocine.net/v6/ns/}movieShowtimes")
           
            for movie in movies:
                mynsmap = {}
                mynsmap['bob'] = movie.nsmap[None]
                monfilm = Film()
                movieid = movie.xpath("./bob:onShow/bob:movie",namespaces = mynsmap)
                movieid = movieid[0].attrib['code']
                try:
                    monfilm = Film.objects.get(id_allocine_film=movieid)

                except Film.DoesNotExist:
                    monfilm.id_allocine_film = movieid
                    title  = movie.xpath("./bob:onShow/bob:movie/bob:title",namespaces = mynsmap)
                    urlimage = movie.xpath("./bob:onShow/bob:movie/bob:poster",namespaces = mynsmap)
                    duration = movie.xpath("./bob:onShow/bob:movie/bob:runtime",namespaces = mynsmap)
                    monfilm.titre = title[0].text
                    monfilm.url_allocine_image = urlimage[0].attrib['href']
                    monfilm.duree = int(duration[0].text)
                    monfilm.save()
                    time.sleep(1)
                    response = requests.get(monfilm.url_allocine_image)
                    webimage = Image.open(StringIO(response.content))
                    film_id = str(monfilm.id)
                    filename = defaultfilters.slugify(monfilm.titre)+"-"+film_id+".jpg"
                    directory= settings.MEDIA_ROOT+'cinemas/'
                    absfilename = os.path.join(directory,filename)
                    try:
                        webimage.save(absfilename, webimage.format, quality=90, optimize=1, progressive=True)
                    except:
                        webimage.save(absfilename, webimage.format, quality=90)
                    relfilename = 'cinemas/'+filename 
                    monfilm.image = relfilename
                    monfilm.save()


                try:
                    movieformat = movie.xpath("./bob:screenFormat",namespaces = mynsmap)[0].text
                except IndexError:
                    movieformat = None
                version_lang = movie.xpath("./bob:version",namespaces = mynsmap)[0].text
                version_vo = movie.xpath("./bob:version",namespaces = mynsmap)[0].attrib['original']
                screenings = movie.xpath("./bob:screenings",namespaces = mynsmap)
                
                for scrdate in screenings[0]:
                    thedate = scrdate.attrib['d']
                    for thetime in scrdate:
                        maseance = Seance()
                        maseance.id_allocine_film = movieid
                        maseance.format = movieformat
                        maseance.version_lang = version_lang
                        if version_vo == "true":
                            maseance.version_vo = True
                        else:
                            maseance.version_vo = False
                        
                        
                        maseance.date_debut = datetime.strptime(thedate+" "+thetime.text,"%Y-%m-%d %H:%M")
                        maseance.date_debut = myTimezone.localize(maseance.date_debut)
                        delta = timedelta(seconds = monfilm.duree)
                        maseance.date_fin =  maseance.date_debut + delta 
                        maseance.film = monfilm
                        maseance.cinema = cinema
                        maseance.save()
                    
            cinema.hash_maj = hash_cine.hexdigest()
            cinema.save()
            
                
                
                
                