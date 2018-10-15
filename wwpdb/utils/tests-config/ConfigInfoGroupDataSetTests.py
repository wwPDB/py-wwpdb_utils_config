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
import traceback
import time
import os
import platform

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TESTOUTPUT = os.path.join(HERE, 'test-output', platform.python_version())
if not os.path.exists(TESTOUTPUT):
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, 'wwpdb', 'mock-data')

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.SiteConfigSetup  import SiteConfigSetup
SiteConfigSetup().setupEnvironment(TESTOUTPUT, mockTopPath)

from wwpdb.utils.config.ConfigInfoGroupDataSet import ConfigInfoGroupDataSet
from wwpdb.utils.config.ConfigInfo import ConfigInfo


class ConfigInfoGroupDataSetTests(unittest.TestCase):
    """
    Test cases for mapping group data sets ids to server sites ids.
    """

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__groupIdList = ['G_1', 'G_1002001', 'G_1002003', 'G_1002005', 'G_1002007', 'G_1002009', 'G_1002011', 'G_1002013']
        self.__siteIdList = ['WWPDB_DEPLOY_DEPGRP1_RU', 'WWPDB_DEPLOY_DEPGRP1_RU', 'WWPDB_DEPLOY_TEST_RU',
                             'UNASSIGNED', 'SILLYSITE']

    def tearDown(self):
        pass

    def testGetSiteLocation(self):
        """Test case -  return site location
        """
        startTime = time.time()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            for siteId in self.__siteIdList:
                ci = ConfigInfo(siteId=siteId, verbose=self.__verbose, log=self.__lfh)
                siteName = ci.get("SITE_NAME", default=None)
                siteLoc = ci.get("WWPDB_SITE_LOC", default=None)
                self.__lfh.write(" siteId %-30s siteName %s siteLoc %s\n" % (siteId, siteName, siteLoc))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.time()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testGetSiteGroupIdRange(self):
        """Test case -  return default id ranges selected sites.
        """
        startTime = time.time()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            cfds = ConfigInfoGroupDataSet(self.__verbose, self.__lfh)
            for siteId in self.__siteIdList:
                (lId, uId) = cfds.getDefaultGroupIdRange(siteId=siteId)
                self.__lfh.write(" siteId %-30s lower %-12d upper %-12d \n" % (siteId, lId, uId))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.time()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testGetSiteId(self):
        """Test case -  translate data set id to site id.
        """
        startTime = time.time()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            cfds = ConfigInfoGroupDataSet(self.__verbose, self.__lfh)
            for testId in self.__groupIdList:
                siteId = cfds.getDefaultSiteId(groupId=testId)
                self.__lfh.write(" testId %-12s siteId %20s\n" % (testId, siteId))

        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.time()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))


def suiteGetSiteLocation():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoGroupDataSetTests("testGetSiteLocation"))
    return suiteSelect


def suiteGetSiteId():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoGroupDataSetTests("testGetSiteId"))
    return suiteSelect


def suiteGetGroupIdRange():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoGroupDataSetTests("testGetSiteGroupIdRange"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteGetSiteId()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteGetGroupIdRange()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteGetSiteLocation()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    #
    #
