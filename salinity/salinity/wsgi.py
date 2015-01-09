"""
WSGI config for salinity project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import sys
import os
import site

#path addition
site.addsitedir('/opt/salinity/lib/python2.7/site-packages')
sys.path.append('/opt/salinity/git/salinity/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salinity.settings")

# Activate your virtual env
activate_env=os.path.expanduser("/opt/salinity/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
