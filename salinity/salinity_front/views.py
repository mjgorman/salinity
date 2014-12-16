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
    template = get_template('index.html')
    roles = ['web', 'lb', 'php', 'app', 'uti', 'queue', 'solr', 'es', 'node', 'nfs', 'sftp', 'rsyslog', 'mmonit']
    envs = ['qa', 'stg', 'prd']
    context_dict = {}
    salted = 0
    for role in roles:
        context_dict[role] = server_con.check_failed_role(role, "qa")
        if server_con.check_failed_role(role, "qa") == "GREEN":
            salted += 1

    try:
        saltyness = len(roles) / salted
    except:
        saltyness = 0

    html = template.render(Context({'context_dict' : context_dict, 'saltyness' : saltyness}))
    return HttpResponse(html)
