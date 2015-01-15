"""
This is the models module. This is where I will put all the relevant classes.
"""
#from django.db import models
import redis

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
    def check_failed_role(self, role, env):
        """
        Check for failed highstates
        """
        server_list = self.get_server_list("*" + role + "*" + env)
        try:
            for server in (server for server in server_list if server):
                if self.check_failed_highstate(server, self.find_last_highstate(server)):
                    return "RED"
            if server_list:
                return "GREEN"
        except TypeError:
            return "None"
    def get_server_list(self, glob):
        """
        Using the server glob, find a matching list of servers in
        redis returns so that they can be checked individually.
        """
        server_list = []
        for result in self.con.keys(glob + "*:state.highstate"):
            server_list.append(result.split(":")[0])
        return server_list
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
        highstate = self.con.get(server + ":" + last_highstate)
        if '"result": false' in highstate.lower():
            return True
        return False
