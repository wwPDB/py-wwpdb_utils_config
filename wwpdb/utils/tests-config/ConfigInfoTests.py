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

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402

SiteConfigSetup().setupEnvironment(TESTOUTPUT, mockTopPath)

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
        expMockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
        cI = ConfigInfo()
        self.assertEqual(cI.get("DEPLOY_PATH"), os.path.join(expMockTopPath, "da_top"))
