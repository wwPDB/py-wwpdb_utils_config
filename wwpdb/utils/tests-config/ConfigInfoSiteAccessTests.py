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
TESTOUTPUT = os.path.join(HERE, 'test-output', platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, 'wwpdb', 'mock-data')

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402
SiteConfigSetup().setupEnvironment(TESTOUTPUT, mockTopPath)

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
        self.__siteIdList = ['WWPDB_DEPLOY_PRODUCTION_RU',
                             'WWPDB_DEPLOY_PRODUCTION_UCSD',
                             'PDBE_PROD',
                             'WWPDB_DEPLOY_PRODUCTION_PDBJ',
                             'BMRB',
                             'WWPDB_DEPLOY_TEST_RU',
                             'SILLYSITE']

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
                if siteId in ['WWPDB_DEPLOY_PRODUCTION_UCSD']:
                    should = False
                else:
                    should = True

                logger.info(" siteId %-30s status %r", siteId, status)
                self.assertEqual(status, should, "Status mismatch for %s" % siteId)
        except Exception as e:
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
        except Exception as e:
            logger.exception("Determining if site is reachable %s", str(e))
            self.fail()


def suiteTestSiteAccess():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoSiteAccessTests("testSiteAvailable"))
    suiteSelect.addTest(ConfigInfoSiteAccessTests("testSiteReachable"))
    return suiteSelect


if __name__ == '__main__':
    mySuite = suiteTestSiteAccess()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
