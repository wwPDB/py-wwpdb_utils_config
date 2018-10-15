##
#
# File:    ConfigInfoFileTests.py
# Author:  J. Westbrook
# Date:    17-Mar-2016
# Version: 0.001
#
# Updates:
#   6-Apr-2016  jdw make config path local to his module -
#
##
"""
Test cases for reading and writing configuration files and file caches.
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
import copy
import os

from wwpdb.api.facade.ConfigInfoData import ConfigInfoData
from wwpdb.api.facade.ConfigInfoFile import ConfigInfoFile
from wwpdb.api.facade.ConfigInfoFallBack import ConfigInfoFallBack


class ConfigInfoFileTests(unittest.TestCase):
    """
    Test cases for reading and writing configuration file data.
    """

    def setUp(self):
        self.__lfh = sys.stderr
        self.__verbose = True
        self.__debug = False
        # local test file names -
        self.__testConfigFilePath = 'default.cfg'
        self.__testCacheFilePath = 'TestCache.py'
        self.__testSpecialFilePath = 'special.cfg'
        self.__testJsonCacheFilePath = 'SpecialCache.json'
        self.__cfb = ConfigInfoFallBack(verbose=self.__verbose, log=self.__lfh)
        #
        self.__testSiteId = 'WWPDB_DEPLOY_TEST_RU'
        # self.__topConfigPath = os.getenv('TOP_WWPDB_SITE_CONFIG_DIR', './test-config')
        self.__topConfigPath = './test-config'
        #
        # self.__configCachePath = os.getenv('WWPDB_SITE_CONFIG_CACHE_DIR',None)
        #
        # This dictionary is used for testing purposes only --  this is only useful in the context of
        #       the current fall-back configuration data provided in the ConfigInfoData class.
        self.__siteD = {'PDBE': ['PDBE_PROD', 'PDBE_DEV', 'PDBE_LOCAL', 'PDBE_HAPPY'],
                        'PDBJ': ['WWPDB_DEPLOY_INTERNAL_PDBJ', 'WWPDB_DEPLOY_PRODUCTION_PDBJ'],
                        'RCSB-WEST': ['WWPDB_DEPLOY_PRODUCTION_UCSD'],
                        'RCSB-EAST': ['WWPDB_DEPLOY_STAGING_RU',
                                      'WWPDB_DEPLOY_C5',
                                      'WWPDB_DEPLOY_DEVEL_RU',
                                      'WWPDB_DEPLOY_DEVEL_ALPHA_RU',
                                      'WWPDB_DEPLOY_DEVEL_PROD_RU',
                                      'WWPDB_DEPLOY_DEVEL2_RU',
                                      'WWPDB_DEPLOY_DEVEL2_ALPHA_RU',
                                      'WWPDB_DEPLOY_DEVEL2_PROD_RU',
                                      'WWPDB_DEPLOY_INTERNAL_RU',
                                      'WWPDB_DEPLOY_PRODUCTION_RU',
                                      'WWPDB_DEPLOY_VALSRV_RU',
                                      'WWPDB_DEPLOY_TEST_RU',
                                      'WWPDB_DEPLOY_ALPHA_RU',
                                      'WWPDB_DEPLOY_BETA_RU',
                                      'WWPDB_DEPLOY_NEXT_RU',
                                      'WWPDB_DEPLOY_INTERNAL_RU',
                                      'WWPDB_DEPLOY',
                                      'WWPDB_DEPLOY_MACOSX']}

    def tearDown(self):
        pass

    def __getTestData(self):
        """ Test fixture to create sample configuration data -
        """
        tD = {}
        oD = {}
        tD['SITE_SITE_DICT'] = copy.deepcopy(self.__siteD)
        tD['SITE_STR_LIST'] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        tD['SITE_INT_LIST'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        tD['SITE_DICT_A'] = {'A': 1, 'B': 2, 'C': (1, 2, 3)}
        tD['SITE_SIMPLE_INT'] = 1
        tD['SITE_SIMPLE_FLOAT'] = 1.00001
        tD['SITE_SIMPLE_NONE'] = None
        tD['SITE_SIMPLE_STRING'] = 'abcdefghijklmnopqrstuvwxyz0123456789'

        tD['SITE_SIMPLE_CSV_STRING'] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '99 99', '100 000 000']
        tD['SITE_SIMPLE_CSV_INT'] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, -1]

        oD['config_as_object'] = 'site_site_dict,site_str_list,site_int_list,site_dict_a,'
        oD['CONFIG_CSV_AS_LIST'] = 'SITE_SIMPLE_CSV_STRING,'
        oD['CONFIG_CSV_AS_INT_LIST'] = 'SITE_simple_csv_INT,'
        oD['config_as_int'] = 'SITE_SIMPLE_INT,'
        oD['config_as_float'] = 'SITE_SIMPLE_FLOAT,'
        if self.__verbose:
            self.__lfh.write("\n\n +++  TEST DATA +++\n")
            for k in sorted(tD.keys()):
                self.__lfh.write(" +++ %-45s  %r\n" % (k, tD[k]))
        #
        return tD, oD

    def testSerializeWrite(self):
        """Test case -  write local configuration data with serialization -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cD = {}
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            tD, oD = self.__getTestData()
            cD[self.__testSiteId] = cf.serializeConfig(tD, optionD=oD)
            ok = cf.writeConfig(self.__testSpecialFilePath, sectionL=[self.__testSiteId], sectionD=cD, requireBackup=False)
            self.__lfh.write("Writing %d data sections %r\n" % (len(cD), ok))
            for sKy in cD:
                self.__lfh.write("Section: %s length %d\n" % (sKy, len(cD[sKy])))
                if self.__verbose:
                    for k in sorted(cD[sKy].keys()):
                        self.__lfh.write(" +++ %-45s  %r\n" % (k, cD[sKy][k]))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testDeserializeRead(self):
        """Test case -  read local configuration file with deserialization -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            cD = cf.readConfig(self.__testSpecialFilePath)
            tD, oD = self.__getTestData()
            self.__lfh.write("Read %d data sections\n" % len(cD))
            for sKy in cD:
                dd = cf.deserializeConfig(cD[sKy], optionD=oD)
                self.__lfh.write("Section: %s length %d\n" % (sKy, len(dd)))
                if self.__verbose:
                    for k in sorted(dd.keys()):
                        if tD[k] != dd[k]:
                            self.__lfh.write(" XXX +++ %-45s  %r %r\n" % (k, dd[k], tD[k]))

        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testSerializeJsonWrite(self):
        """Test case -  write configuration data with serialization to json cache file -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cD = {}
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            tD, oD = self.__getTestData()
            cD[self.__testSiteId] = cf.serializeConfig(tD, optionD=oD)
            ok = cf.writeJsonConfigCache(cD, self.__testJsonCacheFilePath, withBackup=False)
            self.__lfh.write("Writing %d data sections %r\n" % (len(cD), ok))
            for sKy in cD:
                self.__lfh.write("Section: %s length %d\n" % (sKy, len(cD[sKy])))
                if self.__verbose:
                    for k in sorted(cD[sKy].keys()):
                        self.__lfh.write(" +++ %-45s  %r\n" % (k, cD[sKy][k]))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testDeserializeJsonRead(self):
        """Test case -  read local json configuration cache file with deserialization -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            cD = cf.readJsonConfigCache(self.__testJsonCacheFilePath)
            tD, oD = self.__getTestData()
            self.__lfh.write("Read %d data sections\n" % len(cD))
            for sKy in cD:
                dd = cf.deserializeConfig(cD[sKy], optionD=oD)
                self.__lfh.write("Section: %s length %d\n" % (sKy, len(dd)))
                if self.__verbose:
                    for k in sorted(dd.keys()):
                        if tD[k] != dd[k]:
                            self.__lfh.write(" XXX +++ %-45s  %r %r\n" % (k, dd[k], tD[k]))

        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testConfigFileWriter(self):
        """Test case -  write local configuration file containing fallback config options -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cD = {}
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            d = self.__cfb.getSiteFallbackDictionary(siteId=self.__testSiteId)
            cD[self.__testSiteId] = d
            ok = cf.writeConfig(self.__testConfigFilePath, sectionL=[self.__testSiteId], sectionD=cD, requireBackup=False)
            self.__lfh.write("Writing %d data sections %r\n" % (len(cD), ok))
            for sKy in cD:
                self.__lfh.write("Section: %s length %d\n" % (sKy, len(cD[sKy])))
                if self.__debug:
                    for k in sorted(cD[sKy].keys()):
                        self.__lfh.write(" +++ %-45s  %r\n" % (k, cD[sKy][k]))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testConfigFileReader(self):
        """Test case -  read local configuration file -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            cD = cf.readConfig(self.__testConfigFilePath)
            self.__lfh.write("Read %d data sections\n" % len(cD))
            for sKy in cD:
                self.__lfh.write("Section: %s length %d\n" % (sKy, len(cD[sKy])))
                if self.__debug:
                    for k in sorted(cD[sKy].keys()):
                        self.__lfh.write(" +++ %-45s  %r\n" % (k, cD[sKy][k]))
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testCacheFileWriter(self):
        """Test case -  write local cache configuration file -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            cf = ConfigInfoFile(self.__verbose, self.__lfh)
            cD = cf.readConfig(self.__testConfigFilePath)
            cf.writePythonConfigCache(cD, self.__testCacheFilePath)
        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testCacheFileImporter(self):
        """Test case -  explicit import of cache configuration file -
        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            # from self.__testCacheFilePath import ConfigInfoCache
            dir, fn = os.path.split(self.__testCacheFilePath)
            modN, ext = os.path.splitext(fn)
            tMod = __import__(modN, globals(), locals(), [], -1)
            cls = tMod.ConfigInfoFileCache()
            d = cls.getConfigDictionary(siteId=self.__testSiteId)
            self.__lfh.write("Imported configuration dictionary length %d\n" % len(d))
            if self.__debug:
                for k, v in d.items():
                    self.__lfh.write(" +++ %-45s  %r\n" % (k, v))
            d = cls.getConfigDictionary(siteId="SILLYSITE")
            self.__lfh.write("Imported wrong site dictionary length %d\n" % len(d))

        except:
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def __mkdir(self, path):
        if (not os.path.isdir(path)):
            os.makedirs(path, 0o755)

    def testWriteConfigTemplates(self):
        """Test case -  write template configuration files to standard project file system paths using
                        the current fallback configuration data -

        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        try:
            cf = ConfigInfoFile(verbose=self.__verbose, log=self.__lfh)
            locCmD = self.__cfb.getCommonOptions(siteD=self.__siteD)
            for siteLoc in self.__siteD:
                siteIdList = self.__siteD[siteLoc]
                siteCmL, siteKyL = locCmD[siteLoc]
                siteCmD = {}
                for siteId in siteIdList:
                    siteSpD = {}
                    cfDirPath = os.path.join(self.__topConfigPath, siteLoc.lower(), siteId.lower())
                    self.__mkdir(cfDirPath)
                    cfPath = os.path.join(cfDirPath, 'site.cfg')
                    self.__lfh.write("Location %s site %s path %s\n" % (siteLoc, siteId, cfPath))
                    spD, cmD, subList, pD, rD, cD = self.__cfb.getFallBackConfig(siteId=siteId)
                    self.__lfh.write("Location %s site %s length spD %d length cmD %d length siteKL %d\n" % (siteLoc, siteId, len(spD), len(cmD), len(siteKyL)))
                    # fill in the values for the common options dictionary --
                    for k in spD.keys():
                        siteSpD[k] = spD[k]
                    otherL = list(set(siteKyL) - set(siteCmL))
                    for k in otherL:
                        if k in spD:
                            siteSpD[k] = spD[k]
                        elif k in cmD:
                            siteSpD[k] = cmD[k]
                    for k in siteCmL:
                        if k in cmD and k not in siteCmD:
                            siteCmD[k] = cmD[k]
                    self.__lfh.write("Location %s site %s length siteSpD %d\n" % (siteLoc, siteId, len(siteSpD)))
                    cf.writeConfig(configFilePath=cfPath, sectionL=[siteId], sectionD={siteId: siteSpD}, requireBackup=False)
                #
                cfDirPath = os.path.join(self.__topConfigPath, siteLoc.lower(), 'site_common')
                self.__mkdir(cfDirPath)
                cfPath = os.path.join(cfDirPath, 'common.cfg')
                self.__lfh.write("Location %s site %s length siteCmD %d\n" % (siteLoc, siteId, len(siteCmD)))
                cf.writeConfig(configFilePath=cfPath, sectionL=['site_common'], sectionD={'site_common': siteCmD}, requireBackup=False)
        except:
            self.__lfh.write("%s.%s failing\n" % (self.__class__.__name__, sys._getframe().f_code.co_name))
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testReadConfigUpdateCache(self):
        """Test case -  read the hierarchy of current configuration files from standard project file system paths.
                        Update site cache files.

        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))
        #
        # list of options that are not managed in configuration files -
        #
        specialList = ['FILE_FORMAT_EXTENSION_DICTIONARY',
                       'CONTENT_TYPE_DICTIONARY',
                       'CONTENT_MILESTONE_LIST',
                       'CONTENT_TYPE_BASE_DICTIONARY',
                       'SITE_DATASET_ID_ASSIGNMENT_DICTIONARY']
        try:
            allSiteD = {}
            commonSectionName = 'common'
            siteCommonSectionName = 'site_common'
            cfCommonPath = os.path.join(self.__topConfigPath, 'common', 'common.cfg')
            cf = ConfigInfoFile(verbose=self.__verbose, log=self.__lfh)

            for siteLoc in self.__siteD:
                cfSiteCommonDirPath = os.path.join(self.__topConfigPath, siteLoc.lower(), 'site_common')
                cfSiteCommonPath = os.path.join(cfSiteCommonDirPath, 'common.cfg')
                self.__lfh.write("Location %s reading site common path %s\n" % (siteLoc, cfSiteCommonPath))
                #
                siteIdList = self.__siteD[siteLoc]
                for siteId in siteIdList:
                    cfDirPath = os.path.join(self.__topConfigPath, siteLoc.lower(), siteId.lower())
                    cfPath = os.path.join(cfDirPath, 'site.cfg')
                    cfPathSectionList = [(cfPath, siteId.lower()), (cfSiteCommonPath, siteCommonSectionName), (cfCommonPath, commonSectionName)]
                    self.__lfh.write("Location %s site %s reading path %s\n" % (siteLoc, siteId, cfPath))
                    rD = cf.readConfigFileList(configPathSectionList=cfPathSectionList)
                    rD = cf.deserializeConfig(rD, optionD=rD)
                    # -
                    #
                    self.__lfh.write("Location %s site %s read configuration files containing %d options\n" % (siteLoc, siteId, len(rD)))
                    #
                    # -- compare current configuration with current fallback values --
                    #
                    fbD = self.__cfb.getSiteFallbackDictionary(siteId)
                    for k, v in fbD.items():
                        if k in specialList:
                            continue
                        if k in rD and rD[k] == v:
                            continue
                        else:
                            if k not in rD:
                                self.__lfh.write("Location %s site %s key %s missing in option dictionary\n" % (siteLoc, siteId, k))
                            else:
                                self.__lfh.write("Location %s site %s key %s fallback value %r  option value  %r\n" % (siteLoc, siteId, k, v, rD[k]))
                    # --------------------
                    # Write site specific cache files -
                    #
                    cfCachePath = os.path.join(cfDirPath, 'ConfigInfoFileCache.py')
                    cf.writePythonConfigCache(cacheD={siteId: rD}, cacheFilePath=cfCachePath)
                    #
                    cfCachePath = os.path.join(cfDirPath, 'ConfigInfoFileCache.json')
                    cf.writeJsonConfigCache(cacheD={siteId: rD}, cacheFilePath=cfCachePath)
                    #
                    allSiteD[siteId] = rD
                # No longer using location common cache files -
                # cfCachePath = os.path.join(cfSiteCommonDirPath, 'ConfigInfoFileCache.py')
                # cf.writePythonConfigCache(cacheD=allSiteD, cacheFilePath=cfCachePath)

        except:
            self.__lfh.write("%s.%s failing\n" % (self.__class__.__name__, sys._getframe().f_code.co_name))
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))

    def testReadCacheFiles(self):
        """Test case -  read cache files from standard project file system paths.

        """
        startTime = time.clock()
        self.__lfh.write("\nStarting %s %s at %s\n" % (self.__class__.__name__, sys._getframe().f_code.co_name,
                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime())))

        try:
            for siteLoc in self.__siteD:
                siteIdList = self.__siteD[siteLoc]
                for siteId in siteIdList:
                    cI = ConfigInfoData(siteId=siteId, verbose=self.__verbose, log=self.__lfh, useCache=True)
                    cD = cI.getConfigDictionary()
                    self.__lfh.write("Location %s site %s read configuration cache containing %d options\n" % (siteLoc, siteId, len(cD)))
        except:
            self.__lfh.write("%s.%s failing\n" % (self.__class__.__name__, sys._getframe().f_code.co_name))
            traceback.print_exc(file=self.__lfh)
            self.fail()

        endTime = time.clock()
        self.__lfh.write("\nCompleted %s %s at %s (%.2f seconds)\n" % (self.__class__.__name__,
                                                                       sys._getframe().f_code.co_name,
                                                                       time.strftime("%Y %m %d %H:%M:%S", time.localtime()),
                                                                       endTime - startTime))


def suiteSerializeDeserialize():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoFileTests("testSerializeWrite"))
    suiteSelect.addTest(ConfigInfoFileTests("testDeserializeRead"))
    return suiteSelect


def suiteSerializeDeserializeJson():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoFileTests("testSerializeJsonWrite"))
    suiteSelect.addTest(ConfigInfoFileTests("testDeserializeJsonRead"))
    return suiteSelect


def suiteConfigReadWrite():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoFileTests("testConfigFileWriter"))
    suiteSelect.addTest(ConfigInfoFileTests("testConfigFileReader"))
    suiteSelect.addTest(ConfigInfoFileTests("testCacheFileWriter"))
    suiteSelect.addTest(ConfigInfoFileTests("testCacheFileImporter"))
    return suiteSelect


def suiteConfigTemplateWriter():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoFileTests("testWriteConfigTemplates"))
    return suiteSelect


def suiteUpdateCache():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoFileTests("testReadConfigUpdateCache"))
    return suiteSelect


def suiteReadCache():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ConfigInfoFileTests("testReadCacheFiles"))
    return suiteSelect


if __name__ == '__main__':
    #
    if (True):
        mySuite = suiteConfigReadWrite()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    if (True):
        mySuite = suiteConfigTemplateWriter()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    if (True):
        mySuite = suiteUpdateCache()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    if (True):
        mySuite = suiteSerializeDeserialize()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    if (True):
        mySuite = suiteSerializeDeserializeJson()
        unittest.TextTestRunner(verbosity=2).run(mySuite)

    if (True):
        mySuite = suiteReadCache()
        unittest.TextTestRunner(verbosity=2).run(mySuite)
    #
    #
