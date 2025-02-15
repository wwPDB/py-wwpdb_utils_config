##
#
# File:    ConfigInfoShellExecTests.py
# Author:  E. Peisach
# Date:    24-Dec-2019
# Version: 0.001
##
"""
Test cases for ConfigInfoShellExec

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

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(HERE)
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)  # pragma: no cover
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

from wwpdb.utils.config.ConfigInfoShellExec import ConfigInfoShellExec  # noqa: E402


class ConfigDataSetExecTests(unittest.TestCase):
    def setUp(self):
        self.__cise = ConfigInfoShellExec(siteId="WWPDB_DEPLOY_TEST", siteLoc="rcsb-east", verbose=True, log=sys.stdout)

    def tearDown(self):
        pass

    def testPrintConfig(self):
        """Tests printing configuration"""
        self.__cise.printConfig()
        # Returns nothing useful

    def testGetConfig(self):
        """Iterates through all get functions"""
        self.__cise.shellConfig()
        self.__cise.shellConfig("tcsh")
        self.__cise.httpdConfig("tcsh")
        self.__cise.installConfig()
        self.__cise.validationConfig()
        self.__cise.databaseConfig()

    def testBrokenConfig(self):
        """Tests error handling"""
        ConfigInfoShellExec(
            topConfigPath="/tmp/ab12s", siteId="WWPDB_DEPLOY_TEST", siteLoc="rcsb-east", verbose=True, log=sys.stdout
        )  # noqa: S108

    def testHostnameLookup(self):
        """Tests locating by host name - no cache"""
        tcise = ConfigInfoShellExec(
            siteId="WWPDB_DEPLOY_TEST", hostName="testhost.test.com", verbose=True, cacheFlag=False, log=sys.stdout
        )
        tcise.shellConfig()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
