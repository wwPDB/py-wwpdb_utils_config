##
#
# File:    ConfigInfoFileTests.py
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

from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class ConfigInfoFileTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetSiteId(self):
        self.assertEqual(getSiteId(), "WWPDB_DEPLOY_TEST")

    def testCache(self):
        cI = ConfigInfo()
        self.assertEqual(cI.get("VARTEST"), "Hello")
        self.assertEqual(cI.get("TESTVAR1"), "1")
        self.assertEqual(cI.get("TESTVAR2"), "2")

    def testMock(self):
        cI = ConfigInfo()
        self.assertEqual(cI.get("DEPLOY_PATH"), os.path.join(rwMockTopPath, "da_top"))
