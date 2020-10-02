##
#
# File:    ConfigInfoGroupDataSetTests.py
# Author:  J. Westbrook
# Date:    23-Oct-2016
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for mapping group data sets ids to server sites ids.
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
import unittest
import time
import os
import platform
import logging

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
crw.createtree(["site-config", "depuiresources"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.utils.config.ConfigInfoGroupDataSet import ConfigInfoGroupDataSet  # noqa: E402
from wwpdb.utils.config.ConfigInfo import ConfigInfo  # noqa: E402


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigInfoGroupDataSetTests(unittest.TestCase):
    """
    Test cases for mapping group data sets ids to server sites ids.
    """

    def setUp(self):
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__groupIdList = ["G_1", "G_1002001", "G_1002003", "G_1002005", "G_1002007", "G_1002009", "G_1002011", "G_1002013"]
        self.__siteIdList = ["WWPDB_DEPLOY_DEPGRP1_RU", "WWPDB_DEPLOY_DEPGRP1_RU", "WWPDB_DEPLOY_TEST_RU", "UNASSIGNED", "SILLYSITE"]

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGetSiteLocation(self):
        """Test case -  return site location"""
        try:
            for siteId in self.__siteIdList:
                ci = ConfigInfo(siteId=siteId, verbose=self.__verbose, log=self.__lfh)
                siteName = ci.get("SITE_NAME", default=None)
                siteLoc = ci.get("WWPDB_SITE_LOC", default=None)
                logger.info(" siteId %-30s siteName %s siteLoc %s", siteId, siteName, siteLoc)
        except Exception as e:  # pragma: no cover
            logger.exception("Unable to get group site location %s", str(e))
            self.fail()

    def testGetSiteGroupIdRange(self):
        """Test case -  return default id ranges selected sites."""
        try:
            cfds = ConfigInfoGroupDataSet(self.__verbose, self.__lfh)
            for siteId in self.__siteIdList:
                (lId, uId) = cfds.getDefaultGroupIdRange(siteId=siteId)
                logger.info(" siteId %-30s lower %-12d upper %-12d", siteId, lId, uId)
        except Exception as e:  # pragma: no cover
            logger.exception("Unable to get group id range %s", str(e))
            self.fail()

    def testGetSiteId(self):
        """Test case -  translate data set id to site id."""
        try:
            cfds = ConfigInfoGroupDataSet(self.__verbose, self.__lfh)
            for testId in self.__groupIdList:
                siteId = cfds.getDefaultSiteId(groupId=testId)
                logger.info(" testId %-12s siteId %20s", testId, siteId)

        except Exception as e:  # pragma: no cover
            logger.exception("Unable to get group site id %s", str(e))
            self.fail()


def suiteGetSiteLocation():  # pragma: no cover
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoGroupDataSetTests("testGetSiteLocation"))
    return suiteSelect


def suiteGetSiteId():  # pragma: no cover
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoGroupDataSetTests("testGetSiteId"))
    return suiteSelect


def suiteGetGroupIdRange():  # pragma: no cover
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoGroupDataSetTests("testGetSiteGroupIdRange"))
    return suiteSelect


if __name__ == "__main__":  # pragma: no cover
    mySuite = suiteGetSiteId()
    unittest.TextTestRunner(verbosity=2).run(mySuite)

    mySuite = suiteGetGroupIdRange()
    unittest.TextTestRunner(verbosity=2).run(mySuite)

    mySuite = suiteGetSiteLocation()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
