# -*- coding: utf-8 -*-
# Create your views here.

from menu.models import MenuItem
from collections import defaultdict

#def getChilds(menuitem):
    

def TopMenu():
    toplistItems = [item for item in MenuItem.objects.all().filter(parent = None).order_by('index')]
    
    flatSubItems = [item for item in MenuItem.objects.all().filter(parent!=None).order_by('index')]
    subitems = defaultdict(list)
    for each in flatSubItems: 
        subitems[each.parent].append(each)
        
    menu = "<ul>"
    for topItem in toplistItems:
        menu="<li>"+topItem.nom+"<li>"
    return menu
        
