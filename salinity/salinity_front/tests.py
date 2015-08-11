"""
Test will go here, hopefully in the first iteration
"""
from django.test import TestCase
from salinity_front.models import CheckRedis
from mock import MagicMock
import salt.wheel
import subprocess

class CheckRedisTests(TestCase):
    """
    Test checkredis functionality
    """
    def setUp(self):
        self.checkredis = CheckRedis("localhost")
        self.setup_checkredis_mocks()
    def setup_checkredis_mocks(self):
        """
        Build the mock of checkredis, allows testing without real redis data
        """
        self.checkredis.con.lindex = MagicMock(name="method")
        self.checkredis.con.lindex.return_value = "01"
        self.checkredis.con.get = MagicMock(name="method")
        self.checkredis.con.get.return_value = "{\"jid\": \"01\", \"return\": {\"service_|-sshd_|-sshd_|-running\": {\"comment\": \"Service sshd is already enabled, and is in the desired state\", \"__run_num__\": 98, \"changes\": {}, \"name\": \"sshd\", \"result\": true}}}"
        salt.wheel.Wheel.call_func = MagicMock(name="method")
        salt.wheel.Wheel.call_func.return_value = {"minions": ['aw1-php70-qa', 'aw1-php80-qa']} 
        subprocess.check_output = MagicMock(name="method")
        subprocess.check_output.return_value = "{'aw1-php70-qa': ['10.26.40.112'], 'aw1-php80-qa': ['10.26.40.123'] }"

    def test_get_server_list(self):
        """
        Find the list of servers (Mocked)
        """
        self.assertEqual(sorted(self.checkredis.get_server_list("php","qa")), sorted(['aw1-php70-qa', 'aw1-php80-qa']))
    def test_find_last_highstate(self):
        """
        Find the last highstate (Mocked)
        """
        self.assertEqual(self.checkredis.find_last_highstate("aw1-php70-qa"), "01")
    def test_check_failed_highstate(self):
        """
        Test the failed highstate (Mocked)
        """
        self.assertEqual(self.checkredis.check_failed_highstate("aw1-php70-qa", "01"), False)
    def test_check_failed_role(self):
        """
        Test failed role, which walks through all the other items as well (Mocked results provided from all the above)
        """
        self.assertEqual(self.checkredis.check_failed_role("php", "qa"), "GREEN")
