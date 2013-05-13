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
import os, glob  , base64, urllib
import json

myTimezone = timezone(settings.TIME_ZONE)
utcTZ = timezone("UTC")
#patch à la noix : http://stackoverflow.com/questions/6788398/how-to-save-progressive-jpeg-using-python-pil-1-1-7
ImageFile.MAXBLOCK = 2**20



class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        
        api_url = "http://api.allocine.fr/rest/v3/showtimelist"
        user_agent = {"User-agent":"Dalvik/1.6.0 (Linux; U; Android 4.0.3; GT-P3100 Build/IML74K)"}
        partner_key = "100043982026"
        secret_key = "29d185d98c984a359e6e6f26a0474269"
        export_format = "json"
        
        
        cinemas = Cinema.objects.all()
        cinemas.order_by('nom')
        
        for cinema in cinemas:
            url_parameters = []
            url_parameters.append(('partner', partner_key))
            url_parameters.append(('format',export_format)) 
            url_parameters.append(('theaters', cinema.id_allocine_cine))
            url_parameters.append(('sed', time.strftime("%Y%m%d")))
            url_parameters.append(( 'sig' ,base64.b64encode(hashlib.sha1(secret_key+urllib.urlencode(url_parameters)).digest()).rstrip("=")+"="))
            response = None
            try :
                response =  requests.get(api_url,params=url_parameters, headers = user_agent )
            except requests.exceptions.Timeout:
                exit()
           
                        
            datatxt = response.text
           
            data = json.loads(datatxt)
            
            hash_cine = hashlib.sha1()
            hash_cine.update(datatxt.encode('utf-8'))
             
            if hash_cine.hexdigest() == cinema.hash_maj:
                continue
            

            seances_to_delete = Seance.objects.select_related().filter(cinema__id = cinema.id)
            films_to_delete = Film.objects.filter(seance__cinema__id = cinema.id)
            films_to_delete.query.group_by = ["id"]
            
            
            
            
            for movie in films_to_delete:
                try:
                    filepath = settings.MEDIA_ROOT+movie.image.name
                    filepath = filepath.replace(".jpg","*")
                    for filename in glob.glob(filepath):
                        os.remove(filename)
                except Exception,e:
                    print e
                movie.delete()
            
            seances_to_delete.delete()
            try:
                movies = [item for item in data["feed"]['theaterShowtimes'][0]['movieShowtimes']]
            except KeyError:
                continue
           
            for movie in movies:
                monfilm = Film()
                movieid = movie['onShow']['movie']['code']
                try:
                    monfilm = Film.objects.get(id_allocine_film=movieid)

                except Film.DoesNotExist:
                    monfilm.id_allocine_film = movieid
                    monfilm.titre  = movie['onShow']['movie']['title']
                    try:
                        monfilm.url_allocine_image = movie['onShow']['movie']['poster']['href']
                    except:
                        monfilm.url_allocine_image = "http://images.allocine.fr/commons/emptymedia/empty_photo.jpg"
                    try:
                        monfilm.duree = movie['onShow']['movie']['runtime']
                    except:
                        monfilm.duree = 3600
                    try:
                        monfilm.note = note = movie['onShow']['movie']['statistics']['userRating']
                    except:
                        monfilm.note = 0

                    
                    monfilm.slug = defaultfilters.slugify(monfilm.titre)
                    monfilm.save()
                    time.sleep(1)
                    response = requests.get(monfilm.url_allocine_image)
                    webimage = Image.open(StringIO(response.content))
                    film_id = str(monfilm.id)
                    filename = monfilm.slug+"-"+film_id+".jpg"
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
                    movieformat =  movie['screenFormat']['$']
                except KeyError:
                    movieformat = None
                version_lang = movie['version']['$']
                version_vo = movie['version']['original']
                screenings = movie['scr']
                
                for scrdate in screenings:
                    thedate = scrdate['d']
                    for thetime in scrdate['t']:
                        maseance = Seance()
                        maseance.id_allocine_film = movieid
                        maseance.format = movieformat
                        maseance.version_lang = version_lang
                        if version_vo == "true":
                            maseance.version_vo = True
                        else:
                            maseance.version_vo = False
                        
                        
                        maseance.date_debut = datetime.strptime(thedate+" "+thetime['$'],"%Y-%m-%d %H:%M")
                        maseance.date_debut = myTimezone.localize(maseance.date_debut)
                        delta = timedelta(seconds = monfilm.duree)
                        maseance.date_fin =  maseance.date_debut + delta 
                        maseance.film = monfilm
                        maseance.cinema = cinema
                        maseance.save()
                    
            cinema.hash_maj = hash_cine.hexdigest()
            cinema.save()
            
                
                
                
