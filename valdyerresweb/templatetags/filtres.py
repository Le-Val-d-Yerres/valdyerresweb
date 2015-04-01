# -*- coding: utf-8 -*-
from django.utils import http
from django import template
from evenements.models import Saison
from menu.models import MenuItem
from aide.models import  Aide
import re , os.path
from pytz import timezone
from django.conf import settings
from PIL import Image, ImageOps, ImageFilter, ImageChops
from django.templatetags.static import static

import datetime
import valdyerresweb

register = template.Library()

jours = [u'dimanche',u'lundi',u'mardi',u'mercredi', u'jeudi' , u'vendredi',u'samedi']
mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
mois_courts = [u'jan', u'fév', u'mars', u'avril', u'mai', u'juin', u'juil', u'août', u'sept', u'oct', u'nov' ,u'déc']
    

@register.filter(is_safe=True)
def deuxchiffres(nombre):
    if nombre < 10:
        return "0"+str(nombre)
    else:
        return nombre

@register.filter(is_safe=True)
def monnaie(nombre):
    if nombre == 0.0:
        return "Gratuit"
    else:
        nombre = "{0:10.2f}".format(nombre)
        nombre = str(nombre)+"€"
        nombre = nombre.replace(".", ",") 
        return nombre
    
@register.filter(is_safe=True)
def dateCustom(debutUTC, finUTC):
    
    TZone = timezone(settings.TIME_ZONE)
    debut = debutUTC.astimezone(TZone)
    fin = finUTC.astimezone(TZone)
    now = datetime.datetime.now(TZone)
    delta = fin-debut
    if delta.days >= 1:
        text = u"du "+jours[int(debut.strftime("%w"))]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+u" au "+jours[int(fin.strftime(u"%w"))]+u" "+fin.strftime(u"%d")+u" "+mois[int(fin.strftime(u"%m"))-1]
    else:
        deltanow = debut.date()-now.date()
        if deltanow.days == 0:
            text = u"aujourd'hui à "+debut.strftime(u"%H:%M")
        elif  deltanow.days == 1:
            text = u"demain à "+debut.strftime(u"%H:%M")
        else :    
            text = jours[int(debut.strftime(u"%w"))]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+u" à "+debut.strftime(u"%H:%M")
    return text


@register.filter(is_safe=True)
def dateSimple(mydate):
    
    TZone = timezone(settings.TIME_ZONE)
    thedate = mydate.astimezone(TZone)
    text = jours[int(thedate.strftime(u"%w"))]+u" "+thedate.strftime(u"%d")+u" "+mois[int(thedate.strftime(u"%m"))-1]+" "+thedate.strftime(u"%Y")+u" à "+thedate.strftime(u"%H:%M")
    return text


@register.filter(is_safe=True)
def festivalInfo(evenement_id, champ):
    festival = Saison.objects.filter(pk=evenement_id)
    if champ == "slug":
        return festival.slug
    elif champ == "nom":
        return festival.nom
    
@register.filter(is_safe=True)
def resume(text, longeur):
    compile_obj = re.compile(r"""(<(/?[^\>]+\>))""")
    text = compile_obj.sub('',text)
    
    if len(text) > longeur:
        if text[longeur] == " " or text[longeur+1] == " ":
            textResult = text[0:longeur]+" [...]"
        else:
            i = longeur
            while (text[i] != " " and i > 1):
                i = i-1
            textResult = text[0:i]+" [...]"
    else:
        textResult = text
    return textResult

@register.filter(is_safe=True)
def toFloatjs(num):
        return str(num).replace(',','.')

@register.filter(is_safe=True)
def grouperToString(monthYear):
    month,year = monthYear.split('-')
    text = mois[int(month)-1]+u" "+str(year)
    return text.capitalize()

@register.filter(is_safe=True)
def moisannee(date):
    month = date.month
    year = date.year
    
    text = mois[int(month)-1]+u" "+str(year)
    return text.capitalize()

@register.filter(is_safe=True)
def annee(date):
    
    year = date.year
    
    text = str(year)
    return text.capitalize()
 
@register.filter(is_safe=True)    
def dateFormat(dateUTC):
    TZone = timezone(settings.TIME_ZONE)
    date = dateUTC.astimezone(TZone)
    return date.strftime("%Y")+date.strftime("%m")+date.strftime("%d")+"T"+date.strftime("%H")+date.strftime("%M")+date.strftime("%S")

@register.filter(is_safe=True)   
def dateSEO(dateUTC):
    TZone = timezone(settings.TIME_ZONE)
    date = dateUTC.astimezone(TZone)
    return date.strftime("%Y")+"-"+date.strftime("%m")+"-"+date.strftime("%d")+"T"+date.strftime("%H")+":"+date.strftime("%M")

#

def resizeandcrop(img, box, fit):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
    @param out: file-like-object - save the image into the output stream
    '''
    

    #calculate the cropping box and get the cropped part
    if fit:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2/box[0]
        hRatio = 1.0 * y2/box[1]
        if hRatio > wRatio:
            y1 = int(y2/2-box[1]*wRatio/2)
            y2 = int(y2/2+box[1]*wRatio/2)
        else:
            x1 = int(x2/2-box[0]*hRatio/2)
            x2 = int(x2/2+box[0]*hRatio/2)
        img = img.crop((x1,y1,x2,y2))

    #Resize the image with best quality algorithm ANTI-ALIAS
    img.thumbnail(box, Image.ANTIALIAS)

    #save it into a file-like object
    return img
#resize

@register.filter(is_safe=True)   
def resize(myfile, size='100x100x1'):
    print('resize')
    try:
        logo = False 
        try:
            path = myfile.path.replace(settings.MEDIA_ROOT,"") #TODO: trouver pkoi Image et Filebrowsefield renvoient des chemins différents
            path = settings.MEDIA_ROOT+path
        except AttributeError:
            path = settings.LOGO_ORGANISATION
            logo = True
    
        x, y, ratio = [int(x) for x in size.split('x')]
    
    
        filehead, filetail = os.path.split(path)
        basename, format = os.path.splitext(filetail)
        
        if format == ".png":
            format = ".jpg"
            
        miniature = basename + '_' + size + format
        filename = path
        filehead = os.path.join(filehead,'mini')
        if not os.path.exists(filehead):
            os.makedirs(filehead)
        miniature_filename = os.path.join(filehead, miniature)
        miniature_url = filehead + '/' + miniature
        
        if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
    
        if not os.path.exists(miniature_filename):
           
            image = ImageOps.fit(Image.open(filename), (x,y), Image.ANTIALIAS)
              
            try:
                image.save(miniature_filename, "JPEG", quality=90, optimize=True, progressive=True)
            except:
                image.save(miniature_filename, "JPEG", quality=90)
        
        if logo is True:
            return miniature_url.replace(settings.STATIC_ROOT,settings.STATIC_URL)
            
        return miniature_url.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)
    
    except:
        return "fileerror.jpg"



@register.filter(is_safe=True)   
def expand(myfile, size='100x100x1'):
    try:   
        logo = False 
        try:
            path = myfile.path.replace(settings.MEDIA_ROOT,"")
            path = settings.MEDIA_ROOT+path
        except AttributeError:
            path = settings.STATIC_ROOT+settings.LOGO_ORGANISATION
            logo = True
    
        x, y, ratio = [int(x) for x in size.split('x')]
    
    
        filehead, filetail = os.path.split(path)
        basename, format = os.path.splitext(filetail)
        
        if format == ".png":
            format = ".jpg"
            
        miniature = basename + '_' + size + format
        filename = path
        filehead = os.path.join(filehead,'mini')
        if not os.path.exists(filehead):
            os.makedirs(filehead)
        miniature_filename = os.path.join(filehead, miniature)
        miniature_url = filehead + '/' + miniature
        
        if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
            os.unlink(miniature_filename)
    
        if not os.path.exists(miniature_filename):
           
            image = Image.open(filename)
            for i in range(0,15):
                image = image.filter(ImageFilter.BLUR)
                
            x2, y2 = image.size
            x3 = (x2*2)/100
            
            image = image.crop((x3,0,x2-x3,y2))  
            image = ImageOps.fit(image, (x,y), Image.ANTIALIAS)
            #image = ImageChops.offset(image, x,y)
            #image = resizeandcrop(image, (x,y), True)
           
            try:
                image.save(miniature_filename, "JPEG", quality=90, optimize=True, progressive=True)
            except:
                image.save(miniature_filename, "JPEG", quality=90)
        
        if logo is True:
            return miniature_url.replace(settings.STATIC_ROOT,settings.STATIC_URL)
                
        return miniature_url.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)
    except:
        return "fileerror.jpg"

# evenements
@register.filter(is_safe=True) 
def lieuMarker(lieu):
    try:
        picto = lieu.fonction.picto
    except:
        picto = settings.PICTO_LIEU
    return picto

@register.filter(is_safe=True) 
def aide(aideSlug):
    aide = Aide.objects.get(slug=aideSlug)
    return aide


@register.filter()
def generateMenu():
    menu=''
    return menu
        
@register.filter(is_safe=True) 
def twitter(url,txt):
    lien = "<a href=\"https://www.twitter.com/share?text="+http.urlquote_plus(txt)+"&amp;url="+valdyerresweb.settings.NOM_DOMAINE+url+"\"><img alt=\"twitter\" src=\""+static("valdyerresweb/img/reseaux-sociaux/twitter-share.png")+"\"> Partager sur Twitter</a>"
    return lien
        
@register.filter(is_safe=True) 
def facebook(url,txt):
    lien = "<a href=\"https://www.facebook.com/sharer.php?t="+http.urlquote_plus(txt)+"&amp;u="+valdyerresweb.settings.NOM_DOMAINE+url+"\"><img alt=\"facebook\" src=\""+static("valdyerresweb/img/reseaux-sociaux/facebook-share.png")+"\"> Partager sur Facebook</a>"
    return lien

