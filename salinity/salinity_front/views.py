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
    saltyness = 0
    #roles = ['web', 'lb', 'php', 'app', 'uti', 'queue', 'solr', 'es', 'node', 'nfs', 'sftp', 'rsyslog', 'mmonit']
    roles = ['php']
    not_stg = ['rsyslog', 'mmonit']
    envs = ['qa', 'stg', 'prd']
    context_dict = {}
    for role in roles:
        context_dict[role] = server_con.check_failed_role("php", "qa")

    html = template.render(Context({'context_dict' : context_dict, 'saltyness' : saltyness}))
    return HttpResponse(html)
