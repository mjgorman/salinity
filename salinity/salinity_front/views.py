"""
Web views are setup here. Will display a templated page populated with
results from checking the redis server
"""
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import logging
from salinity_front.models import CheckRedis

def index(request):
    """
    The main page, will end up being a timeline like page
    """
    logging.info(request)
    server_con = CheckRedis("localhost")
    test_role = server_con.check_failed_role("php", "qa")
    template = get_template('index.html')
    saltyness = 50
    roles = ['web', 'lb', 'php', 'app', 'uti', 'queue', 'solr', 'es', 'node', 'nfs', 'sftp', 'rsyslog', 'mmonit']
    not_stg = ['rsyslog', 'mmonit']
    envs = ['qa', 'stg', 'prd']

    html = template.render(Context({'test_role': test_role, 'saltyness': saltyness, 'roles' : roles, 'not_stg' : not_stg, 'envs' : envs}))
    return HttpResponse(html)
