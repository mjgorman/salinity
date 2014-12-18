"""
Test will go here, hopefully in the first iteration
"""
from django.test import TestCase
from salinity_front.models import CheckRedis
from mock import MagicMock

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
        self.checkredis.con.keys = MagicMock(name="method")
        self.checkredis.con.keys.return_value = ['aw1-php70-qa', 'aw1-php80-qa']
        self.checkredis.con.lindex = MagicMock(name="method")
        self.checkredis.con.lindex.return_value = "01"
        self.checkredis.con.get = MagicMock(name="method")
        self.checkredis.con.get.return_value = "This Highstate went well"
    def test_get_server_list(self):
        """
        Find the list of servers (Mocked)
        """
        self.assertEqual(sorted(self.checkredis.get_server_list("*php*qa")), sorted(['aw1-php70-qa', 'aw1-php80-qa']))
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
