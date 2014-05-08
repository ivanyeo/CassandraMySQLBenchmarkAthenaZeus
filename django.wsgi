import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/ivan/site/venv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/ivan/site/tagteam')
sys.path.append('/home/ivan/site/tagteam/tagteam')

os.environ['DJANGO_SETTINGS_MODULE'] = 'tagteam.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/ivan/site/venv/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
