#
#
# File:    ConfigInfoAppCommunicationTests.py
# Author:  E. Peisach
# Date:    18-Oct-2020
# Version: 0.001
##
"""
Test cases for communication settings
"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import platform
import unittest
import sys

try:
    from unittest.mock import patch
except ImportError:  # pragma: no cover
    from mock import patch

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):  # pragma: no cover
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402
from wwpdb.utils.testing.CreateRWTree import CreateRWTree  # noqa: E402

# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(["site-config", "depuiresources", "webapps"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppCommunication  # noqa: E402
from wwpdb.utils.config.ConfigInfo import ConfigInfo  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class MyConfigInfo(ConfigInfo):
    """A class to setup tests for DepUI config"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        self._noreply = "noreply@mail.wwpdb.org"
        self._server = "localhost"
        self._err_email = "notification@mail.wwpdb.org"
        super(MyConfigInfo, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get(self, keyWord, default=None):
        if keyWord == "SITE_NOREPLY_EMAIL":
            val = self._noreply
        elif keyWord == "SITE_MAILSERVER_NAME":
            val = self._server
        elif keyWord == "SITE_ERROR_EMAIL":
            val = self._err_email
        else:  # pragma: no cover
            # sys.stderr.write("XXXXX Unknown site config fetching %s\n" % keyWord)
            val = super(MyConfigInfo, self).get(keyWord=keyWord, default=default)

        return val


class StandardConfig(MyConfigInfo):
    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(StandardConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)


class TestConfig(MyConfigInfo):
    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(TestConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self._noreply = "noreply@test.com"
        self._server = "relayhost.test.com"
        self._err_email = "error@mail.wwpdb.org"


class ConfigInfoAppCommunicationTests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation of EM class works"""
        ConfigInfoAppCommunication()

    def testDefaultValues(self):
        """Test default values"""
        with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=StandardConfig) as _mock_method:  # noqa: F841
            ciac = ConfigInfoAppCommunication()
            nr = ciac.get_noreply_address()
            self.assertEqual(nr, "noreply@mail.wwpdb.org")

            msa = ciac.get_mailserver_name()
            self.assertEqual(msa, "localhost")

            err_email = ciac.get_system_notification_address()
            self.assertEqual(err_email, "notification@mail.wwpdb.org")

    def testAlteredValues(self):
        """Test override values"""
        with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=TestConfig) as _mock_method:  # noqa: F841
            ciac = ConfigInfoAppCommunication()
            nr = ciac.get_noreply_address()
            self.assertEqual(nr, "noreply@test.com")

            msa = ciac.get_mailserver_name()
            self.assertEqual(msa, "relayhost.test.com")

            err_email = ciac.get_system_notification_address()
            self.assertEqual(err_email, "error@mail.wwpdb.org")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
