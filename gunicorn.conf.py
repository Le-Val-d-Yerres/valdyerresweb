#from os.path import dirname,join,abspath
#PATH_PROJECT = dirname(abspath(__file__))
#import sys
#sys.path.append(PATH_PROJECT)

backlog = 2048
bind = "127.0.0.1:8000"
#pidfile = "/var/run/gunicorn/valdyerresweb.pid"
daemon = False
debug = False
workers = 3
logfile = "/home/web/www/gunicorn.log"
loglevel = "info"
