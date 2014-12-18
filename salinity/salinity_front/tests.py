"""
Test will go here, hopefully in the first iteration
"""
from django.test import TestCase
from salinity_front.models import CheckRedis
from mock import MagicMock

class CheckRedisTests(TestCase):
    def setUp(self):
        self.checkredis = CheckRedis("localhost")
    def setUpCheckRedisMocks(self, expected_return):
        self.checkredis.check_failed_role = MagicMock(name="method")
        self.checkredis.check_failed_role.return_value = expected_return
        self.checkredis.get_server_list = MagicMock(name="method")
        self.checkredis.get_server_list.return_value = expected_return
        self.checkredis.find_last_highstate = MagicMock(name="method")
        self.checkredis.find_last_highstate.return_value = expected_return
        self.checkredis.check_failed_highstate = MagicMock(name="method")
        self.checkredis.check_failed_highstate.return_value = expected_return

    def test_get_server_list(self):
        self.setUpCheckRedisMocks(['aw1-php70-qa', 'aw1-php80-qa'])
        self.assertEqual(sorted(self.checkredis.get_server_list("*php*qa")), sorted(['aw1-php70-qa', 'aw1-php80-qa'])) 
    def test_find_last_highstate(self):
        self.setUpCheckRedisMocks("225")
        self.assertEqual(self.checkredis.find_last_highstate("aw1-php70-qa"), "225")
    def test_check_failed_highstate(self):
        self.setUpCheckRedisMocks(False)
        self.assertEqual(self.checkredis.check_failed_highstate("aw1-php121-qa", "225"), False)
    def test_check_failed_role(self):
        self.setUpCheckRedisMocks("GREEN")
        self.assertEqual(self.checkredis.check_failed_role("php", "qa"), "GREEN")
