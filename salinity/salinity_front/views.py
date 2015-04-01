"""
Web views are setup here. Will display a templated page populated with
results from checking the redis server
"""
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import logging
import collections
from salinity_front.models import CheckRedis
import jsonpickle
from time import time
import threading

server_con = CheckRedis("localhost")
roles = {'app':['web', 'lb', 'php', 'app', 'util', 'queue', 'solr', 'es', 'node', 'nfs', 'sftp', 'rsyslog', 'mmonit'], 'ci': ['slave', 'ci', 'tarantula', 'awsutils']}
no_stg = ['rsyslog', 'mmonit']
envs = {'app':['qa', 'stg', 'prd'], 'ci':['ci']}

def update_redis():
    while(True):
        server_con.update_redis_context(envs, roles)

update_redis = threading.Thread(target=update_redis)

def index(request):
    """
    The main page, will end up being a timeline like page
    """
    logging.info(request)
    template = get_template('index.html')
    salted = 0
    context_dict = jsonpickle.decode(server_con.get_context())

    for env_type, env_list in envs.iteritems():
        for env in env_list:
            for role in roles[env_type]:
                if context_dict[role + "_" + env]['status'] == "GREEN":
                    salted += 1
    
    sorted_dict = collections.OrderedDict(sorted(context_dict.items()))
    try:
        saltyness = salted*100/((len(roles['app'])*3 + len(roles['ci']))-len(no_stg))
    except ZeroDivisionError:
        saltyness = 0

    html = template.render(Context({'context_dict' : sorted_dict, 'saltyness' : saltyness}))

    if not update_redis.is_alive():
        update_redis.start()

    return HttpResponse(html)

def job(request, role="none", env="none"):
    """
    The job ID information page
    """
    logging.info(request)
    template = get_template('job.html')
    # Get these from URL parameters
    params = request.GET.get('role')
    role = params.split('_')[0]
    env = params.split('_')[1]
    server = server_con.get_server_list("*" + role + "*" + env)[0]

    jid = server_con.find_last_highstate(server)
    highstate = server_con.get_highstate(server, jid) 
    html = template.render(Context({'jid': jid, 'role' : role, 'env' : env, 'highstate' : highstate}))
    return HttpResponse(html)
