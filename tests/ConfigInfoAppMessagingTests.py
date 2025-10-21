#
#
# File:    ConfigInfoAppCommunicationTests.py
# Author:  E. Peisach
# Date:    18-Oct-2020
# Version: 0.001
##
"""
Test cases for messaging setting
"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import platform
import sys
import unittest

try:
    from unittest.mock import patch
except ImportError:  # pragma: no cover
    from unittest.mock import patch

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(HERE)
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):  # pragma: no cover
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.CreateRWTree import CreateRWTree  # noqa: E402
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402

# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(["site-config", "depuiresources", "webapps"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.utils.config.ConfigInfo import ConfigInfo  # noqa: E402
from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppMessaging  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(HERE)


class MyConfigInfo(ConfigInfo):
    """A class to setup tests for Messaging Communication"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        self._msgdbname = None
        super(MyConfigInfo, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get(self, keyWord, default=None):
        if keyWord == "SITE_MESSAGE_DB_NAME":
            val = self._msgdbname
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
        self._msgdbname = "WWPDB_MESSAGING"


class ConfigInfoAppMessagingTests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation works"""
        ConfigInfoAppMessaging()

    def testDefaultValues(self):
        """Test default values"""
        with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=StandardConfig) as _mock_method:  # noqa: F841
            cim = ConfigInfoAppMessaging()
            self.assertFalse(cim.get_msgdb_support())

    def testAlteredValues(self):
        """Test override values"""
        with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=TestConfig) as _mock_method:  # noqa: F841
            cim = ConfigInfoAppMessaging()
            self.assertTrue(cim.get_msgdb_support())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
