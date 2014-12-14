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
    def return_from_glob(self, glob):
        """
        Do some glob magic to find highstate
        """
        return_list = []
        for match in self.con.keys(glob):
            return_list.append(self.con.hget(match, 'highstate'))
        return return_list
    def check_failed(self, role):
        """
        Check for failed highstates
        """
        for redis_return in self.return_from_glob("*" + role + "*"):
            if "false" in redis_return.lower():
                print redis_return
