##
#
# File:    ConfigInfoSiteAccessTests.py
# Author:  J. Westbrook
# Date:    07-Apr-2016
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for checking site access status.
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import sys
import unittest
import time
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

from wwpdb.utils.config.ConfigInfoSiteAccess import ConfigInfoSiteAccess  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigInfoSiteAccessTests(unittest.TestCase):
    """
    Test cases for checking site access status information.
    """

    def setUp(self):
        self.__startTime = time.time()
        logger.info("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

        self.__lfh = sys.stdout
        self.__verbose = False
        #
        self.__siteIdList = ["WWPDB_DEPLOY_PRODUCTION_RU", "WWPDB_DEPLOY_PRODUCTION_UCSD", "PDBE_PROD", "WWPDB_DEPLOY_PRODUCTION_PDBJ", "BMRB", "WWPDB_DEPLOY_TEST_RU", "SILLYSITE"]

    def tearDown(self):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testSiteAvailable(self):
        """Test case -  return site access status.
        """
        try:
            cfsa = ConfigInfoSiteAccess(self.__verbose, self.__lfh)
            for siteId in self.__siteIdList:
                status = cfsa.isSiteAvailable(siteId)
                if siteId in ["WWPDB_DEPLOY_PRODUCTION_UCSD"]:
                    should = False
                else:
                    should = True

                logger.info(" siteId %-30s status %r", siteId, status)
                self.assertEqual(status, should, "Status mismatch for %s" % siteId)
        except Exception as e:  # pragma: no cover
            logger.exception("Determining if site is available %s", str(e))
            self.fail()

    def testSiteReachable(self):
        """Test case -  return if the site is reachable.
        """
        try:
            cfsa = ConfigInfoSiteAccess(self.__verbose, self.__lfh)
            for siteId in self.__siteIdList:
                status = cfsa.isServiceReachable(siteId, timeout=5)
                logger.info(" siteId %-30s reachable %r", siteId, status)
        except Exception as e:  # pragma: no cover
            logger.exception("Determining if site is reachable %s", str(e))
            self.fail()

        # Coverage case - site not existand
        cfsa = ConfigInfoSiteAccess(self.__verbose, self.__lfh)
        status = cfsa.isServiceReachable("UNKNOWN SITE", timeout=5)
        self.assertFalse(status, "Received info on nonexistant site")

    def testSiteGetCorrespondence(self):
        """Test case -  return if site correspondence returned
        """
        cfsa = ConfigInfoSiteAccess(self.__verbose, self.__lfh)
        status = cfsa.getCorrespondenceService("WWPDB_DEPLOY_PRODUCTION_RU")
        self.assertIsNotNone(status, "Failed to get correspondece endpoint")
        status = cfsa.getCorrespondenceService("SITE_NO_EXIST")
        self.assertIsNone(status, "Found unexpected correspondece endpoint")

    def testSiteGetForwarding(self):
        """Test case -  return for site forwarding endpoint
        """
        cfsa = ConfigInfoSiteAccess(self.__verbose, self.__lfh)
        status = cfsa.getForwardingService("WWPDB_DEPLOY_PRODUCTION_RU")
        self.assertIsNotNone(status, "Failed to get forwarding endpoint")
        status = cfsa.getForwardingService("SITE_NO_EXIST")
        self.assertIsNone(status, "Found unexpected forwarding endpoint")

    def testSiteGetDownTimeRange(self):
        """Test case -  return for site forwarding endpoint
        """
        cfsa = ConfigInfoSiteAccess(self.__verbose, self.__lfh)
        status = cfsa.getSiteDownTimeRange("WWPDB_DEPLOY_PRODUCTION_RU")
        self.assertEqual(status, (None, None), "Failed to get downtime")
        status = cfsa.getSiteDownTimeRange("PDBE_PROD")
        self.assertEqual(status, ("2016-08-26 06:00:00", "2016-09-02 06:00:00"), "Failed to get downtime")


def suiteTestSiteAccess():  # pragma: no cover
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoSiteAccessTests("testSiteAvailable"))
    suiteSelect.addTest(ConfigInfoSiteAccessTests("testSiteReachable"))
    suiteSelect.addTest(ConfigInfoSiteAccessTests("testSiteGetCorrespondence"))
    return suiteSelect


if __name__ == "__main__":  # pragma: no cover
    mySuite = suiteTestSiteAccess()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
