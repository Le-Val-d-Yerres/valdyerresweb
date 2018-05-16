# -*- coding: utf-8 -*-
from django import template
register = template.Library()
import datetime

mois = [u'janvier', u'février', u'mars', u'avril', u'mai', u'juin', u'juillet', u'août', u'septembre', u'octobre', u'novembre' ,u'décembre']
WeekDay = ['lundi','mardi','mercredi', 'jeudi' , 'vendredi','samedi','dimanche']
SchemaDay = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
SchemaDayLD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#une journée en général
@register.filter(is_safe=True) 
def horaires_journee(numjour,horaire):
    txthours = ""
    numjour= int(numjour)
    myday = horaire.GetDay(numjour)
    if myday.matin_ferme and myday.am_ferme:
        return "fermé toute la journée"
    
    if myday.journee_continue:
        return "journée continue de "+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_am_fin.strftime("%H:%M")+"."
    if myday.matin_ferme:
        txthours += "fermé la matinée, "
    else:
        txthours += "matin de "+myday.heure_matin_debut.strftime("%H:%M")+" à "+myday.heure_matin_fin.strftime("%H:%M")+", "
        
    if myday.am_ferme:
        txthours += "fermé l'après-midi"
    else:
        txthours += "après-midi de "+myday.heure_am_debut.strftime("%H:%M")+" à "+myday.heure_am_fin.strftime("%H:%M")
    return txthours+"."


@register.filter(is_safe=True)
def schema_horaires_journee(numjour, horaire):
    txthours = ""
    numjour = int(numjour)
    myday = horaire.GetDay(numjour)
    numjour = numjour -1 # pour l'index du tableau
    balise = "<span itemprop=\"openingHours\" content=\"{{hours}}\"/>"
    if myday.matin_ferme and myday.am_ferme:
        return ""

    if myday.journee_continue:
        return balise.replace("{{hours}}", SchemaDay[numjour] +" "+ myday.heure_matin_debut.strftime("%H:%M") + " - " + myday.heure_am_fin.strftime(
            "%H:%M"))
    if myday.matin_ferme:
        txthours +=""
    else:
        txthours += balise.replace("{{hours}}", SchemaDay[numjour] +" "+ myday.heure_matin_debut.strftime("%H:%M") + " - " + myday.heure_matin_fin.strftime(
            "%H:%M"))

    if myday.am_ferme:
        txthours += ""
    else:
        txthours += balise.replace("{{hours}}", SchemaDay[numjour] +" "+ myday.heure_am_debut.strftime("%H:%M") + " - " + myday.heure_am_fin.strftime(
            "%H:%M"))
    return txthours


#un jour précis
def horaires_jour(day,horaire):
    return horaires_journee(day.isoweekday(), horaire)  


@register.filter(is_safe=True)
def horaire_journee_timedelta(delta,horaire):
    day = datetime.date.today() + datetime.timedelta(days=delta)
    return horaires_jour(day, horaire)

@register.filter(is_safe=True)
def schema_horaire_journee_timedelta(delta,horaire):
    day = datetime.date.today() + datetime.timedelta(days=delta)
    return schema_horaires_journee(day.isoweekday(), horaire)


@register.filter(is_safe=True)
def horaires_semaine(horaire, periode):
    txthoraires = ""
    
    nbreJour = (periode.date_fin-periode.date_debut).days
    
    if nbreJour >= 6:
        listeJour = range(1, 8)
    else:
        listeJour = []
        prochainJour = periode.date_debut
        while (periode.date_fin-prochainJour).days >= 0:
            listeJour.append(prochainJour.weekday()+1)
            
            prochainJour += datetime.timedelta(days=1)
    try:
        for day in listeJour:
            txthoraires += "<li>"+WeekDay[day-1].capitalize()+" : "+horaires_journee(day, horaire)+"</li>"
        return txthoraires
    except:
        return u"Erreur"


@register.filter(is_safe=True)
def horaires_semaine_schema(horaire, periode):
    txthoraires = ""

    nbreJour = (periode.date_fin - periode.date_debut).days

    if nbreJour >= 6:
        listeJour = range(1, 8)
    else:
        listeJour = []
        prochainJour = periode.date_debut
        while (periode.date_fin - prochainJour).days >= 0:
            listeJour.append(prochainJour.weekday() + 1)

            prochainJour += datetime.timedelta(days=1)
    try:
        txthoraires = "\"openingHoursSpecification\":[\n"
        for day in listeJour:
            txthoraires += horaires_journee_schema(day, horaire)
            if listeJour.index(day) == len(listeJour)-1:
                txthoraires += "\n"
            else:
                txthoraires += ",\n"
        txthoraires += "]"
        return txthoraires
    except:
        return u"Erreur"

@register.filter(is_safe=True)
def horaires_journee_schema(numjour, horaire):
    txthours = ""
    numjour = int(numjour)
    myday = horaire.GetDay(numjour)
    numjour = numjour -1 # pour l'index du tableau
    txthoraires = "{\n"
    txthoraires += "\"@type\": \"OpeningHoursSpecification\",\n"
    txthoraires += "\"dayOfWeek\": \"" + SchemaDayLD[numjour] + "\",\n"
    txthoraires += "\"opens\": \"{{opens}}\",\n"
    txthoraires += "\"closes\":\"{{closes}}\"\n"
    txthoraires += "}"

    if myday.matin_ferme and myday.am_ferme:
        tmpopens = "00:00:00"
        txthoraires = txthoraires.replace("{{opens}}", tmpopens)
        txthoraires = txthoraires.replace("{{closes}}", tmpopens)
        return txthoraires

    if myday.journee_continue:
        tmpopens = myday.heure_matin_debut.strftime("%H:%M:%S")
        tmpcloses = myday.heure_am_fin.strftime("%H:%M:%S")
        txthoraires = txthoraires.replace("{{opens}}", tmpopens)
        txthoraires = txthoraires.replace("{{closes}}", tmpcloses)
        return txthoraires


    if not myday.matin_ferme:
        tmpopens = myday.heure_matin_debut.strftime("%H:%M:%S")
        tmpcloses = myday.heure_matin_fin.strftime("%H:%M:%S")
        txthoraires1 = txthoraires.replace("{{opens}}", tmpopens)
        txthoraires1 = txthoraires1.replace("{{closes}}", tmpcloses)

    if not myday.am_ferme:
        tmpopens = myday.heure_am_debut.strftime("%H:%M:%S")
        tmpcloses = myday.heure_am_fin.strftime("%H:%M:%S")
        txthoraires2 = txthoraires.replace("{{opens}}", tmpopens)
        txthoraires2 = txthoraires2.replace("{{closes}}", tmpcloses)
        if not myday.matin_ferme:
            txthoraires1 = txthoraires1 + ",\n"
            txthoraires = txthoraires1 + txthoraires2
            return txthoraires
        else:
            txthoraires = txthoraires2


    return txthoraires


@register.filter(is_safe=True)
def horaires_aujourdhui(horaire):
    today = datetime.datetime.today()
    return horaires_jour(today,horaire)

@register.filter(is_safe=True)
def schema_horaires_aujourdhui(horaire):
    today = datetime.datetime.today()
    return schema_horaires_journee(today.isoweekday(), horaire)

@register.filter(is_safe=True)
def horaires_demain(horaire):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return horaires_jour(tomorrow,horaire)

@register.simple_tag()
def nom_jour_aujourdhui():
    day = datetime.datetime.today()
    return WeekDay[day.weekday()] +" "+day.strftime(u"%d")+u" "+mois[int(day.strftime(u"%m"))-1]

@register.simple_tag()
def schema_day_aujourdhui():
    day = datetime.datetime.today()
    return SchemaDay[day.weekday()]

@register.simple_tag()
def nom_jour_demain():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    return WeekDay[tomorrow.weekday()]

@register.filter(is_safe=True)
def nom_jour_index(index):
    day = datetime.date.today() + datetime.timedelta(days=index)
    return WeekDay[day.weekday()] +" "+day.strftime(u"%d")+u" "+mois[int(day.strftime(u"%m"))-1]

@register.filter(is_safe=True)
def schema_day_index(index):
    day = datetime.date.today() + datetime.timedelta(days=index)
    return WeekDay[day.weekday()]

@register.filter(is_safe=True)
def dates_periode(debut, fin):
    if debut.strftime(u"%d") != fin.strftime(u"%d") or debut.strftime(u"%m") != fin.strftime(u"%m") or debut.strftime(u"%Y") != fin.strftime(u"%Y"):
        text = u"du "+WeekDay[debut.weekday()]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+" "+debut.strftime(u"%Y")+" au "+WeekDay[fin.weekday()]+u" "+fin.strftime(u"%d")+u" "+mois[int(fin.strftime(u"%m"))-1]+" "+fin.strftime(u"%Y")
    else:
        text = u""+WeekDay[debut.weekday()]+u" "+debut.strftime(u"%d")+u" "+mois[int(debut.strftime(u"%m"))-1]+" "+debut.strftime(u"%Y")
    return text






