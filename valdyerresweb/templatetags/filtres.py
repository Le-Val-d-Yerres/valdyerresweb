# -*- coding: utf-8 -*-

from django import template
from datetime import timedelta
from time import strftime
from evenements.models import Saison
from aide.models import Aide
import re
from pytz import timezone
import pytz
from django.conf import settings
import os
import os.path
import re
import Image

register = template.Library()

jours = ['dimanche','lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi']
mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre' ,'décembre']
mois_courts = ['jan', 'fév', 'mars', 'avril', 'mai', 'juin', 'juil', 'août', 'sept', 'oct', 'nov' ,'déc']
    
    
@register.filter(is_safe=True)
def dateCustom(debutUTC, finUTC):
    TZone = timezone(settings.TIME_ZONE)
    debut = debutUTC.astimezone(TZone)
    fin = finUTC.astimezone(TZone)
    delta = fin-debut
    if delta.days >= 1:
        text = "du "+jours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" "+mois[int(debut.strftime("%m"))-1]+" au "+jours[int(fin.strftime("%w"))]+" "+fin.strftime("%d")+" "+mois[int(fin.strftime("%m"))-1]
    else:
        text = "le "+jours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" "+mois[int(debut.strftime("%m"))-1]+" "+debut.strftime("à %H:%M")
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
def dateFormat(dateUTC):
    TZone = timezone(settings.TIME_ZONE)
    date = dateUTC.astimezone(TZone)
    return date.strftime("%Y")+date.strftime("%m")+date.strftime("%d")+"T"+date.strftime("%H")+date.strftime("%M")+date.strftime("%S")

@register.filter(is_safe=True)   
def dateSEO(dateUTC):
    TZone = timezone(settings.TIME_ZONE)
    date = dateUTC.astimezone(TZone)
    return date.strftime("%Y")+"-"+date.strftime("%m")+"-"+date.strftime("%d")+"T"+date.strftime("%H")+":"+date.strftime("%M")

# trouvé sur http://united-coders.com/christian-harms/image-resizing-tips-every-coder-should-know/
def resizeandcrop(img, box, fit):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
     apuça @param out: file-like-object - save the image into the output stream
    '''
    #preresize image with factor 2, 4, 8 and fast algorithm
    factor = 1
    while img.size[0]/factor > 2*box[0] and img.size[1]*2/factor > 2*box[1]:
        factor *=2
    if factor > 1:
        img.thumbnail((img.size[0]/factor, img.size[1]/factor), Image.NEAREST)

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
    #img.save(out, "JPEG", quality=90)
    return img
#resize

@register.filter(is_safe=True)   
def resize(file, size='100x100x1'):
    file.path = settings.MEDIA_ROOT+file.path
    print file.path+'\n'
    # defining the size
    x, y, ratio = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(file.path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = file.path
    miniature_filename = os.path.join(filehead, miniature)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)
    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
        image = resizeandcrop(Image.open(filename), (x,y), True)
        
#        if ratio == 0:
#            image = image.resize([x, y], Image.ANTIALIAS)
#        else:
#            image.thumbnail([x, y], Image.ANTIALIAS)        
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)

    return miniature_url.replace(settings.MEDIA_ROOT,settings.MEDIA_URL)




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
