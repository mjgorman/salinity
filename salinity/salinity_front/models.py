"""
This is the models module. This is where I will put all the relevant classes.
"""
#from django.db import models
import redis
import jsonpickle
from time import time
import subprocess
import ast

class CheckRedis(object):
    """
    This class is where the redis connection and work happens.
    """
    def __init__(self, server):
        """
        Setup the server address and redis connection string
        """
        self.server = server
        self.con = redis.Redis(self.server)
    def check_failed_role(self, role, env, server_list=['aw1-web30-qa']):
        """
        Check for failed highstates
        """
        try:
            server_list = self.get_server_list(role,env)
        except Exception as e:
            print "There was a problem, {}, using default server_list".format(e)
        try:
            for server in (server for server in server_list if server):
                if self.check_failed_highstate(server, self.find_last_highstate(server)):
                    return "RED"
            if server_list:
                return "GREEN"
        except TypeError:
            return "None"
    def get_server_list(self, role, env):
        """
        Using the server glob, find a matching list of servers in
        redis returns so that they can be checked individually.
        """
        serverList = ast.literal_eval(subprocess.check_output(["/usr/bin/sudo", "/opt/salinity/git/salinity/salinity_front/salt_client.py"]))
        return [server for server,ip in serverList.iteritems() if role in server and env in server]
    def find_last_highstate(self, server):
        """
        Check the server:state.highstate list entry for
        the most recent highstat value. We will use this
        to parse json and look for bad states.
        """
        return self.con.lindex(server + ":state.highstate", 0)
    def check_failed_highstate(self, server, last_highstate):
        """
        Spit back the actual json from the highstate
        """
        highstate = jsonpickle.decode(self.con.get(server + ":" + last_highstate))
        try:
            for state, info in highstate['return'].iteritems():
                if not info['result']:
                    return True
        except Exception as e:
            print "Problem with highstate return: {}".format(e)
        return False
    def get_highstate(self, server, jid):
        return jsonpickle.decode(self.con.get(server + ":" + jid))
    def get_context(self):
        return self.con.get("saved_context_dict")
    def get_context(self, context={"No": { "Valid": "Json"}}):
        try:
            context = jsonpickle.decode(self.con.get("saved_context_dict"))
        except:
            pass
        return context
    def write_context(self, context):
        self.con.set("saved_context_dict", context)
    def update_redis_context(self, envs, roles, timestamp=0.0):
        try:
            timestamp = float(self.con.get("saved_context_timestamp"))
        except:
            pass
        now = time()
        if abs(timestamp - now) > 1200:
            self.con.set("saved_context_timestamp", time()) 
            context_dict = {}
            for env_type, env_list in envs.iteritems():
                for env in env_list:
                    for role in roles[env_type]:
                        context_dict[role + "_" + env] = {'status':self.check_failed_role(role, env), 'role':role, 'env':env}
                        print context_dict[role + "_" + env]
            redis_context = jsonpickle.encode(context_dict)
            self.write_context(redis_context)
