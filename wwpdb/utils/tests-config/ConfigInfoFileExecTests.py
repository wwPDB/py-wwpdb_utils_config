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
import shutil

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

from wwpdb.utils.config.ConfigInfoFileExec import ConfigInfoFileExec  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class ConfigInfoFileExecTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConfigPath(self):
        cif = ConfigInfoFileExec()

        status = cif.testConfigPath()
        self.assertTrue(status, "testconfig read access")
        status = cif.testConfigPath("write")
        self.assertTrue(status, "testconfig write access")

    def testPrintConfig(self):
        cif = ConfigInfoFileExec()
        # Test coverage
        cif.printConfig("rcsb-east", "WWPDB_DEPLOY_TEST")

    def testWriteConfigFallBack(self):
        """Create a fake callback tree and instantiates files"""
        outdir = os.path.join(TESTOUTPUT, "mocksite")
        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        cif = ConfigInfoFileExec(mockTopPath=outdir, sourceDirPath=os.path.join(outdir, "site-config"))
        status = cif.writeConfigFallBack("rcsb-west", "WWPDB_DEPLOY_PRODUCTION_UCSD")
        self.assertTrue(status, "Creating fallback")
        testfile = os.path.join(outdir, "site-config", "rcsb-west", "wwpdb_deploy_production_ucsd", "site.cfg")
        self.assertTrue(os.path.exists(testfile), "Created test file missing")

        # Need to set os.environ for what comes next
        savenv = os.getenv("TOP_WWPDB_SITE_CONFIG_DIR", default=None)
        os.environ["TOP_WWPDB_SITE_CONFIG_DIR"] = os.path.join(outdir, "site-config")

        cif = ConfigInfoFileExec(mockTopPath=outdir, sourceDirPath=os.path.join(outdir, "site-config"))
        status = cif.writeConfigCache("rcsb-west", "wwpdb_deploy_production_ucsd")
        self.assertTrue(status, "In creating cache files")
        os.environ["TOP_WWPDB_SITE_CONFIG_DIR"] = savenv


if __name__ == "__main__":
    unittest.main()
