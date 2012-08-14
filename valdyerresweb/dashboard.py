"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'levaldyerres.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # liste de tout les modules par defaut 
        """self.children.append(modules.Group(
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    _('Administration'),
                    column=1,
                    collapsible=False,
                    models=('django.contrib.*',),
                ),
            ]
        ))"""
        
        # Remplace la liste des modules d'administration par defaut
        self.children.append(modules.AppList(
            _('Administration'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            models=('django.contrib.*',),
        ))
                
        # Liste des gestionnaires de media
        self.children.append(modules.LinkList(
            _('Media Management'),
            column=1,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))
        
        # Liste des applications
        self.children.append(modules.AppList(
            _('Applications'),
            collapsible=True,
            column=1,
            css_classes=('collapse closed',),
            exclude=('django.contrib.*',),
        ))
        
        # Liste des modules d'administration par defaut
        """self.children.append(modules.ModelList(
            _('ModelList: Administration'),
            column=1,
            collapsible=False,
            models=('django.contrib.*',),
        ))"""
        
        # Lien vers la doc django et grapppelli
        """self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://packages.python.org/django-grappelli/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Google-Code'),
                    'url': 'http://code.google.com/p/django-grappelli/',
                    'external': True,
                },
            ]
        ))"""
        
        # affichage des news django
        """self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))"""
        
        # affichage des dernieres actions
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))


