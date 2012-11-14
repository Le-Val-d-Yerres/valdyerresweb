# -*- coding: utf-8 -*-

from django import template
from evenements.models import Saison
from menu.models import MenuItem
from aide.models import  Aide
import re , os.path , Image
from pytz import timezone
from django.conf import settings

register = template.Library()

jours = [u'dimanche',u'lundi',u'mardi',u'mercredi', u'jeudi' , u'vendredi',u'samedi']
mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
mois_courts = [u'jan', u'fév', u'mars', u'avril', u'mai', u'juin', u'juil', u'août', u'sept', u'oct', u'nov' ,u'déc']
    
    
@register.filter(is_safe=True)
def dateCustom(debutUTC, finUTC):
    TZone = timezone(settings.TIME_ZONE)
    debut = debutUTC.astimezone(TZone)
    fin = finUTC.astimezone(TZone)
    delta = fin-debut
    if delta.days >= 1:
        text = u"du "+jours[int(debut.strftime("%w"))]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+u" au "+jours[int(fin.strftime(u"%w"))]+u" "+fin.strftime(u"%d")+u" "+mois[int(fin.strftime(u"%m"))-1]
    else:
        text = u"le "+jours[int(debut.strftime(u"%w"))]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+u" à "+debut.strftime(u"%H:%M")
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
# un peu modifié aussi
def resizeandcrop(img, box, fit):
    '''Downsample the image.
    @param img: Image -  an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fix: boolean - crop the image to fill the box
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
    return img


@register.filter(is_safe=True)   
def resize(myfile, size='100x100x1'):
    logo = False 
    try:
        path = settings.MEDIA_ROOT+myfile.path
    except AttributeError:
        path = settings.STATIC_ROOT+settings.LOGO_ORGANISATION
        logo = True
    # defining the size
    x, y, ratio = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    filehead, filetail = os.path.split(path)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    filename = path
    miniature_filename = os.path.join(filehead, miniature)
    miniature_url = filehead + '/' + miniature
    if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
        os.unlink(miniature_filename)

    if not os.path.exists(miniature_filename):
        image = resizeandcrop(Image.open(filename), (x,y), True)
          
        try:
            image.save(miniature_filename, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_filename, image.format, quality=90)
    
    if logo is True:
        return miniature_url.replace(settings.STATIC_ROOT,settings.STATIC_URL)
            
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


@register.filter()
def generateMenu():
    menu=''
    return menu
        
        
        

    
    
    
    
    