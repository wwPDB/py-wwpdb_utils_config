##
#
# File:    ConfigInfoDataSetTests.py
# Author:  J. Westbrook
# Date:    17-Mar-2016
# Version: 0.001
#
# Updates:
#
##
"""
Test cases for mapping data sets ids to server sites ids.
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

from wwpdb.utils.config.ConfigInfoDataSet import ConfigInfoDataSet  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigInfoDataSetTests(unittest.TestCase):
    """
    Test cases for mapping data sets ids to server sites ids.
    """

    def setUp(self):
        self.__startTime = time.time()
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__testIdList = ["D_1", "D_1000200000", "D_1000200001", "1001200000", 1000200000, 8000200001, 8000200002, 8000200003, 100, 10002000000]
        self.__testIdLoc = {
            "D_1": None,
            "D_1000200000": "WWPDB_DEPLOY_PRODUCTION_RU",
            "D_1000200001": "WWPDB_DEPLOY_PRODUCTION_RU",
            "1001200000": "WWPDB_DEPLOY_PRODUCTION_RU",
            1000200000: "WWPDB_DEPLOY_PRODUCTION_RU",
            8000200001: None,
            8000200002: None,
            8000200003: None,
            100: None,
            10002000000: None,
        }
        self.__siteIdList = [
            "WWPDB_DEPLOY_PRODUCTION_RU",
            "WWPDB_DEPLOY_NEXT_RU",
            "WWPDB_DEPLOY_PRODUCTION_UCSD",
            "WWPDB_DEPLOY_BETA_RU",
            "PDBE_PROD",
            "WWPDB_DEPLOY_PRODUCTION_PDBJ",
            "BMRB",
            "WWPDB_DEPLOY_TEST_RU",
            "UNASSIGNED",
            "SILLYSITE",
        ]
        self.__siteIdRanges = {
            "WWPDB_DEPLOY_PRODUCTION_RU": (1000200000, 1001200000),
            "WWPDB_DEPLOY_NEXT_RU": (800000, 999999),
            "WWPDB_DEPLOY_PRODUCTION_UCSD": (1001200001, 1001300000),
            "WWPDB_DEPLOY_BETA_RU": (8000240000, 8000250000),
            "PDBE_PROD": (1200000001, 1300000000),
            "WWPDB_DEPLOY_PRODUCTION_PDBJ": (1300000001, 1400000000),
            "BMRB": (800000, 999999),
            "WWPDB_DEPLOY_TEST_RU": (8000210000, 8000215000),
            "UNASSIGNED": (800000, 999999),
            "SILLYSITE": (800000, 999999),
        }
        self.__siteIdTestRanges = {"WWPDB_DEPLOY_LCLTEST_RU": (8000231000, 8000232000), "SILLYSITE": (-1, -1), "WWPDB_DEPLOY_PRODUCTION_RU": (-1, -1)}

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGetSiteIdRange(self):
        """Test case -  return default id ranges selected sites.
        """
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            for siteId in self.__siteIdList:
                (lId, uId) = cfds.getDefaultIdRange(siteId=siteId)
                logger.info(" siteId %-30s lower %-12d upper %-12d", siteId, lId, uId)
                (refLid, refUid) = self.__siteIdRanges[siteId]
                if siteId in self.__siteIdRanges:
                    self.assertEqual(lId, refLid)
                    self.assertEqual(uId, refUid)
        except Exception as e:
            logger.exception("Failure in getting id range %s", str(e))
            self.fail()

    def testGetSiteId(self):
        """Test case -  translate data set id to site id.
        """
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            for testId in self.__testIdList:
                siteId = cfds.getSiteId(depSetId=testId)
                logger.info(" testId %-12s siteId %20s", testId, siteId)
                self.assertEqual(siteId, self.__testIdLoc[testId])
        except Exception as e:
            logger.exception("Update to get site id for dataset %s", str(e))
            self.fail()

    def testGetSiteIdTestRange(self):
        """Test case -  return default id ranges selected sites.
        """
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            for siteId in self.__siteIdTestRanges:
                (lId, uId) = cfds.getTestIdRange(siteId=siteId)
                logger.info(" siteId %-30s lower %-12d upper %-12d", siteId, lId, uId)
                (refLid, refUid) = self.__siteIdTestRanges[siteId]
                if siteId in self.__siteIdTestRanges:
                    self.assertEqual(lId, refLid)
                    self.assertEqual(uId, refUid)
        except Exception as e:
            logger.exception("Failre to get SiteIdTestRange %s", str(e))
            self.fail()


def suiteGetSiteId():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoDataSetTests("testGetSiteId"))
    return suiteSelect


def suiteGetIdTestRange():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoDataSetTests("testGetSiteIdTestRange"))
    return suiteSelect


def suiteGetIdRange():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoDataSetTests("testGetSiteIdRange"))
    return suiteSelect


if __name__ == "__main__":
    #
    mySuite = suiteGetSiteId()
    siteRes = unittest.TextTestRunner(verbosity=2).run(mySuite).wasSuccessful()

    mySuite = suiteGetIdRange()
    idRes = unittest.TextTestRunner(verbosity=2).run(mySuite).wasSuccessful()

    mySuite = suiteGetIdTestRange()
    testidRes = unittest.TextTestRunner(verbosity=2).run(mySuite).wasSuccessful()

    sys.exit(not siteRes or not idRes or not testidRes)
