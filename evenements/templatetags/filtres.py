# -*- coding: utf-8 -*-

from django import template
from datetime import timedelta
from time import strftime
from evenements.models import Saison
import re

register = template.Library()

jours = ['dimanche','lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi']
mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre' ,'décembre']
mois_courts = ['jan', 'fév', 'mars', 'avril', 'mai', 'juin', 'juil', 'août', 'sept', 'oct', 'nov' ,'déc']
    
    
@register.filter(is_safe=True)
def dateCustom(debut, fin):
    delta = fin-debut
    if delta.days >= 1:
        text = "Du "+jours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" "+mois[int(debut.strftime("%m"))-1]+" "+debut.strftime("à %H:%M")+" au "+jours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" "+mois[int(debut.strftime("%m"))-1]+" "+debut.strftime("à %H:%M")
    else:
        text = "Le "+jours[int(debut.strftime("%w"))]+" "+debut.strftime("%d")+" "+mois[int(debut.strftime("%m"))-1]+" "+debut.strftime("à %H:%M")
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