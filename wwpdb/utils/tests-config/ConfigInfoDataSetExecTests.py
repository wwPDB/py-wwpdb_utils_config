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
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402
from wwpdb.utils.testing.CreateRWTree import CreateRWTree  # noqa: E402

# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(["site-config", "depuiresources"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.utils.config.ConfigInfoDataSetExec import ConfigInfoDataSetExec  # noqa: E402
from wwpdb.utils.config.ConfigInfoDataSet import ConfigInfoDataSet  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class ConfigDataSetExecTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckConfig(self):
        cidse = ConfigInfoDataSetExec()
        cidse.checkConfig()
        # Nothing to check here

    def testPrintConfig(self):
        cidse = ConfigInfoDataSetExec()
        cidse.printConfig("WWPDB_DEPLOY_PRODUCTION_RU")
        # Nothing to check here

    def testSetRemoveLocations(self):
        cidse = ConfigInfoDataSetExec()
        tset = ["D_800002", "D_800003"]
        status = cidse.setLocations("WWPDB_DEPLOY_DUMMY_RU", tset)
        self.assertTrue(status)

        # Check response
        cids = ConfigInfoDataSet()
        for d in tset:
            self.assertEqual(cids.getSiteId(d), "WWPDB_DEPLOY_DUMMY_RU")
        self.assertIsNone(cids.getSiteId("D_9999"))
        self.assertEqual(cids.getSiteId("D_1000200001"), "WWPDB_DEPLOY_PRODUCTION_RU")

        # Removal
        status = cidse.removeDataSets([tset[0]])
        self.assertTrue(status)
        # Reinstantiate to load list again
        cids = ConfigInfoDataSet()
        self.assertEqual(cids.getSiteId(tset[0]), "UNASSIGNED", "Removal failed")


if __name__ == "__main__":
    unittest.main()
