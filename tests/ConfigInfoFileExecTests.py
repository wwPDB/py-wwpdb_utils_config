##
#
# File:    ConfigInfoFileExecTests.py
# Author:  E. Peisach
# Date:    5-Oct-2018
# Version: 0.001
##
"""
Test cases for generation of configuration and use

"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import platform
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

from wwpdb.utils.config.ConfigInfoFileExec import ConfigInfoFileExec  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(HERE)


class ConfigInfoFileExecTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConfigPath(self):
        cif = ConfigInfoFileExec(mockTopPath=mockTopPath)

        status = cif.testConfigPath()
        self.assertTrue(status, "testconfig read access")
        status = cif.testConfigPath("write")
        self.assertTrue(status, "testconfig write access")

    def testPrintConfig(self):
        cif = ConfigInfoFileExec(mockTopPath=mockTopPath)
        # Test coverage
        cif.printConfig("rcsb-east", "WWPDB_DEPLOY_TEST")

    def testWriteConfig(self):
        """Test writing config file"""
        subtestdir = os.path.join(TESTOUTPUT, "testconfig")
        testout = os.path.join(subtestdir, "site-config", "rcsb-east", "wwpdb_deploy_test", "ConfigInfoFileCache.json")
        if os.path.exists(testout):
            os.remove(testout)
        cr = CreateRWTree(mockTopPath, subtestdir)
        cr.createtree(["site-config"])
        saveconf = os.environ["TOP_WWPDB_SITE_CONFIG_DIR"]
        try:
            os.environ["TOP_WWPDB_SITE_CONFIG_DIR"] = os.path.join(subtestdir, "site-config")
            cif = ConfigInfoFileExec(mockTopPath=subtestdir)
            cif.writeConfigCache(siteLoc="rcsb-east", siteId="WWPDB_DEPLOY_TEST")
        except Exception as e:  # noqa: BLE001 pragma: no cover
            self.fail("Error testing writing config %s" % str(e))

        os.environ["TOP_WWPDB_SITE_CONFIG_DIR"] = saveconf

        self.assertTrue(os.path.exists(testout))

    def testWriteLocationConfig(self):
        """Test writing config file"""
        subtestdir = os.path.join(TESTOUTPUT, "testconfig")
        testout = os.path.join(subtestdir, "site-config", "rcsb-east", "wwpdb_deploy_test", "ConfigInfoFileCache.json")
        if os.path.exists(testout):
            os.remove(testout)
        cr = CreateRWTree(mockTopPath, subtestdir)
        cr.createtree(["site-config"])
        saveconf = os.environ["TOP_WWPDB_SITE_CONFIG_DIR"]
        try:
            os.environ["TOP_WWPDB_SITE_CONFIG_DIR"] = os.path.join(subtestdir, "site-config")
            cif = ConfigInfoFileExec(mockTopPath=subtestdir)
            cif.writeLocationConfigCache(siteLoc="rcsb-east")
        except Exception as e:  # noqa: BLE001 pragma: no cover
            self.fail("Error testing writing config %s" % str(e))

        os.environ["TOP_WWPDB_SITE_CONFIG_DIR"] = saveconf

        self.assertTrue(os.path.exists(testout))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
