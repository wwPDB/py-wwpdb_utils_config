##
#
# File:    ConfigInfoDataTests.py
# Author:  J. Westbrook
# Date:    06-Apr-2016
# Version: 0.001
#
# Updates:
#     1-Jun-2016  jdw add test for configuration object dictionary 'ANNOTATOR_USER_NAME_DICT'
##
"""
Test cases for configuration option management.
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
import os
import unittest
import traceback
import time


from wwpdb.api.facade.ConfigInfoData import ConfigInfoData


class ConfigInfoDataTests(unittest.TestCase):
    """
    Test accessors for configuration options -
    """

    def setUp(self):
        self.__lfh = sys.stdout
        self.__verbose = True
        #
        self.__siteIdList = ['WWPDB_DEPLOY_PRODUCTION_RU',
                             'WWPDB_DEPLOY_PRODUCTION_UCSD',
                             'PDBE_PROD',
                             'WWPDB_DEPLOY_PRODUCTION_PDBJ',
                             'WWPDB_DEPLOY_MACOSX']

    def tearDown(self):
        pass

    def testGetConfigDictionary(self):
        """Test case -  verify default configuration - with unspecified siteId.
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            cid = ConfigInfoData(verbose=self.__verbose, log=self.__lfh, useCache=True)
            cD = cid.getConfigDictionary()
            self.__lfh.write("%s.%s site %s option dictionary length %d\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, cD['SITE_PREFIX'], len(cD)))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("Completed %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime - startTime))

    def testGetMultipleConfigs(self):
        """Test case -  test cache and fallback resources for production sites.
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            useCache = True
            for siteId in self.__siteIdList:
                self.__lfh.write("\n\n%s.%s importing configuration for site %s useCache %r\n" %
                                 (self.__class__.__name__, sys._getframe().f_code.co_name, siteId, useCache))
                cid = ConfigInfoData(siteId=siteId, verbose=self.__verbose, log=self.__lfh, useCache=useCache)
                cD = cid.getConfigDictionary()
                self.__lfh.write("%s.%s site %s option dictionary length %d\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, cD['SITE_PREFIX'], len(cD)))
            #
            useCache = False
            for siteId in self.__siteIdList:
                self.__lfh.write("\n\n%s.%s importing configuration for site %s useCache %r\n" %
                                 (self.__class__.__name__, sys._getframe().f_code.co_name, siteId, useCache))
                cid = ConfigInfoData(siteId=siteId, verbose=self.__verbose, log=self.__lfh, useCache=useCache)
                cD = cid.getConfigDictionary()
                self.__lfh.write("%s.%s site %s option dictionary length %d\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, cD['SITE_PREFIX'], len(cD)))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("Completed %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime - startTime))

    def testSelectedConfiguration(self):
        """Test case -  selected configuration required for e-mail handler and data exchange apps.

                        test will fail if there are missing configuration options -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            siteId = 'WWPDB_DEPLOY_PRODUCTION_RU'
            siteInfo = ConfigInfoData(siteId=siteId, useCache=True)
            siteDict = siteInfo.getConfigDictionary()
            self.__lfh.write("%s.%s site %s option dictionary length %d\n" % (self.__class__.__name__, sys._getframe().f_code.co_name, siteDict['SITE_PREFIX'], len(siteDict)))
            #
            daArchiveDir = os.path.join(siteDict['SITE_ARCHIVE_STORAGE_PATH'], 'archive')
            daDepositDir = os.path.join(siteDict['SITE_DEPOSIT_STORAGE_PATH'], 'deposit')

            # internal database -
            daInternalDbHostName = siteDict['SITE_DA_INTERNAL_DB_HOST_NAME']
            daInternalDbName = siteDict['SITE_DA_INTERNAL_DB_NAME']
            daInternalDbPort = siteDict['SITE_DA_INTERNAL_DB_PORT_NUMBER']
            #
            # New options -
            daInternalDbUserName = siteDict['SITE_DA_INTERNAL_DB_USER_NAME']
            daInternalDbPassword = siteDict['SITE_DA_INTERNAL_DB_PASSWORD']

            # status db -
            daStatusHostName = siteDict['SITE_DB_HOST_NAME']
            daStatusPortNumber = siteDict['SITE_DB_PORT_NUMBER']
            daStatusDbName = siteDict['SITE_DB_DATABASE_NAME']
            daStatusDbUserName = siteDict['SITE_DB_USER_NAME']
            daStatusDBPassword = siteDict['SITE_DB_PASSWORD']
            #
            # instance db
            daInstanceDbHostName = siteDict['SITE_INSTANCE_DB_HOST_NAME']
            daInstanceDbName = siteDict['SITE_INSTANCE_DB_NAME']
            daInstanceDbUserName = siteDict['SITE_INSTANCE_DB_USER_NAME']
            daInstanceDbPassword = siteDict['SITE_INSTANCE_DB_PASSWORD']
            daInstanceDbSocket = siteDict['SITE_INSTANCE_DB_SOCKET']
            daInstanceDbPortNumber = siteDict['SITE_INSTANCE_DB_PORT_NUMBER']
            #
            daRefdataDbName = siteDict['SITE_REFDATA_PRD_DB_NAME']
            daRefdataDbName = siteDict['SITE_REFDATA_CC_DB_NAME']
            daRefdataDbHostName = siteDict['SITE_REFDATA_DB_HOST_NAME']
            daRefdataDbPortNumber = siteDict['SITE_REFDATA_DB_PORT_NUMBER']
            daRefdataDbSocket = siteDict['SITE_REFDATA_DB_SOCKET']
            #     New options -
            daRefdatadbUserName = siteDict['SITE_REFDATA_DB_USER_NAME']
            daRefdataDbPassword = siteDict['SITE_REFDATA_DB_PASSWORD']

            #
            #     New options -
            daSiteMessageHost = siteDict['SITE_MESSAGE_SERVER_HOST_NAME']
            daMessageArchiveUrl = siteDict['SITE_MESSAGE_ARCHIVE_URL']
            daMessageForwardUrl = siteDict['SITE_MESSAGE_FORWARD_URL']
            myUrl1 = 'http://' + daSiteMessageHost + daMessageArchiveUrl
            myUrl2 = 'http://' + daSiteMessageHost + daMessageForwardUrl
            #
            aD = siteDict['ANNOTATOR_USER_NAME_DICT']
            self.__lfh.write("\nANNOTATOR_USER_NAME_DICT: %r \n" %  aD)
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("Completed %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                     sys._getframe().f_code.co_name,
                                                                     time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                     endTime - startTime))


def suiteGetConfigDictionary():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoDataTests("testGetConfigDictionary"))
    suiteSelect.addTest(ConfigInfoDataTests("testGetMultipleConfigs"))
    return suiteSelect


def suiteSelected():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoDataTests("testSelectedConfiguration"))
    return suiteSelect

if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteGetConfigDictionary()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

        mySuite = suiteSelected()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    #
    #
