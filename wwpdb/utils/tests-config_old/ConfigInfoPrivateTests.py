##
#
# File:    ConfigInfoSpecialTests.py
# Author:  J. Westbrook
# Date:    12-Apr-2017
# Version:
#
# Updates:
#
##
"""
Test cases for special/private configuration data sections.
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

from wwpdb.api.facade.ConfigInfo import ConfigInfo


class ConfigInfoSpecialTests(unittest.TestCase):
    """
    Test cases for special/private configuration data sections.
    """

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__siteIdList = ['WWPDB_DEPLOY_PRODUCTION_RU', 'WWPDB_DEPLOY_DEPGRP1_RU', 'WWPDB_DEPLOY_DEPGRP1_RU', 'WWPDB_DEPLOY_TEST_RU',
                             'UNASSIGNED', 'SILLYSITE']

    def tearDown(self):
        pass

    def testGetSiteLocation(self):
        """Test case -  return site location
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            for siteId in self.__siteIdList:
                ci = ConfigInfo(siteId=siteId, verbose=self.__verbose, log=self.__lfh)
                hsD = ci.get("HOST_SITE_DEFAULTS", default={})
                self.__lfh.write("SiteId %s HSD %r\n" % (siteId, hsD))
                d = {}
                for _, v in hsD.items():
                    vL = v.split(',')
                    d[vL[1]] = vL[0]
                for siteId in self.__siteIdList:
                    if siteId in d:
                        self.__lfh.write(" siteId %-30s location %s\n" % (siteId, d[siteId]))
                    else:
                        self.__lfh.write(" siteId %-30s location UNKNOWN\n" % siteId)
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))


def suiteGetSiteLocation():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoSpecialTests("testGetSiteLocation"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteGetSiteLocation()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    #
    #
