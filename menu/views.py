# -*- coding: utf-8 -*-
# Create your views here.

from menu.models import MenuItem
from collections import defaultdict

def getChilds(items , subitems, menutxt ="" , sub = False):
    if sub:
        menutxt = "<ul class=\"dropdown-menu\" aria-labelledby=\"drop1\" role=\"menu\">\n"
    else :
        menutxt = "<ul role=menubar  class=\"nav\">\n"
    for item in items:
        menutxt += "<li role=menuitem #item-"+str(item.id)+" ><a #item-link"+str(item.id)+" href=\""+item.chemin+"\">"+item.nom+"#caret-"+str(item.id)+" </a>\n"
        try:
            sublist = subitems[item.id]
            if len(sublist) ==0:
                menutxt = menutxt.replace("#caret-"+str(item.id), "")
                menutxt = menutxt.replace("#item-"+str(item.id), "")
                menutxt = menutxt.replace("#item-link"+str(item.id), "")
                menutxt += "</li>"
                continue
            if sub :
                menutxt = menutxt.replace("#caret-"+str(item.id), "")
                menutxt = menutxt.replace("#item-"+str(item.id), "class=\"dropdown-submenu\"")  
            else:
                menutxt = menutxt.replace("#caret-"+str(item.id), "<b class=\"caret\"></b>")
                menutxt = menutxt.replace("#item-"+str(item.id), "class=\"dropdown\"")
                
            menutxt = menutxt.replace("#item-link"+str(item.id), "id=\"drop"+str(item.id)+"\" class=\"dropdown-toggle\" data-toggle=\"dropdown\" role=\"button\"")
            menutxt += getChilds(sublist, subitems, menutxt , sub = True)
            menutxt += "</li>"
        except:
            menutxt += "</li>"
            pass
    return menutxt + "</ul>\n"
            
            
            

def TopMenu():
    
    items = MenuItem.objects.all().select_related('parent').order_by('index')
    toplistItems = [item for item in items if item.parent == None]
    flatSubItems = [item for item in items if item.parent != None]
    subitems = defaultdict(list)
    for each in flatSubItems: 
        subitems[each.parent.id].append(each)   
        
    return getChilds(toplistItems, subitems)
        
