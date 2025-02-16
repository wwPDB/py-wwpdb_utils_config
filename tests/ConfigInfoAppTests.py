#
#
# File:    ConfigInfoAppTests.py
# Author:  E. Peisach
# Date:    18-Oct-2020
# Version: 0.001
##
"""
Test cases for application warnings, etc

"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import platform
import sys
import unittest
import warnings

try:
    from unittest.mock import patch
except ImportError:  # pragma: no cover
    from unittest.mock import patch

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(HERE)
TESTOUTPUT = os.path.join(HERE, "test-output", platform.python_version())
if not os.path.exists(TESTOUTPUT):  # pragma: no cover
    os.makedirs(TESTOUTPUT)
mockTopPath = os.path.join(TOPDIR, "wwpdb", "mock-data")
rwMockTopPath = os.path.join(TESTOUTPUT)

# Must create config file before importing ConfigInfo
from wwpdb.utils.testing.CreateRWTree import CreateRWTree  # noqa: E402
from wwpdb.utils.testing.SiteConfigSetup import SiteConfigSetup  # noqa: E402

# Copy site-config and selected items
crw = CreateRWTree(mockTopPath, TESTOUTPUT)
crw.createtree(["site-config", "depuiresources", "webapps"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.utils.config.ConfigInfo import ConfigInfo  # noqa: E402
from wwpdb.utils.config.ConfigInfoApp import (  # noqa: E402
    ConfigInfoAppCc,
    ConfigInfoAppCommon,
    ConfigInfoAppEm,
    ConfigInfoAppValidation,
)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class MyConfigInfo(ConfigInfo):
    """A class to set SITE_EXT_DICT_MAP_EMD_FILE_PATH"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(MyConfigInfo, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get(self, keyWord, default=None):
        if keyWord == "SITE_EXT_DICT_MAP_EMD_FILE_PATH":
            val = "/tmp/emd/emd_map_v2.cif"  # noqa: S108
        elif keyWord == "EXTENDED_CCD_SUPPORT":
            # val = "True"
            val = "False"
        else:
            # sys.stderr.write("XXXXX Unknown site config fetching %s\n" % keyWord)
            val = super(MyConfigInfo, self).get(keyWord=keyWord, default=default)
        return val


class ConfigInfoAppTests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation of EM class works"""
        ConfigInfoAppEm()

    def testResourceBased(self):
        em = ConfigInfoAppEm()
        mf = em.get_emd_mapping_file_path()
        # print("mapping file: %s" % mf)
        self.assertIn("emd_map_v2.cif", mf)

    @patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=MyConfigInfo)
    def testWarningMessage(self, _mock1):  # pylint: disable=unused-argument
        """Tests warning if legacy used. We patch ConfigInfo to return a value"""
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            em = ConfigInfoAppEm()
            mf = em.get_emd_mapping_file_path()
            # print("testWarning mapping file: %s" % mf)
            self.assertIn("emd_map_v2.cif", mf)
            # Verify some things
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))
            self.assertIn("but is deprecated", str(w[-1].message))

    def testNoWarningMessage(self):
        """Tests warning if legacy used"""
        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            em = ConfigInfoAppEm()
            mf = em.get_emd_mapping_file_path()
            # print("testWarning mapping file: %s" % mf)
            self.assertIn("emd_map_v2.cif", mf)
            # Verify no warning issued
            self.assertEqual(len(w), 0)


class ConfigInfoAppComonTests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation of Common class works"""
        ConfigInfoAppCommon()

    def testDictionaryPaths(self):
        """Tests that next and archive dictionaries are not mixed up"""
        cia = ConfigInfoAppCommon()
        self.assertIn("v5_next.dic", cia.get_mmcif_next_dictionary_file_path())
        self.assertIn("v50.dic", cia.get_mmcif_archive_dictionary_file_path())

    def testinchiPathCorrect(self):
        """Tests if get_site_cc_inchi_dir returns a packages path or not.  Should be tools/bin"""
        cia = ConfigInfoAppCommon()
        ipath = cia.get_site_cc_inchi_dir()
        self.assertNotIn("packages/", ipath)

    def testGetIdCodeDir(self):
        """Backwards AppsCc compatibility test"""
        cia = ConfigInfoAppCommon()
        ipath = cia.get_unused_ccd_file()
        self.assertIsNotNone(ipath)

    def testGetVrptDict(self):
        """Test finding path to vrpt dictionary"""
        cia = ConfigInfoAppCommon()
        ipath = cia.get_mmcif_vrpt_dictionary_file_path()
        self.assertIn("mmcif_pdbx_vrpt", ipath)


class ConfigInfoAppCcTests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation of Common class works"""
        ConfigInfoAppCc()

    def testGetIdCodeDir(self):
        """Get CC id code directory"""
        ciac = ConfigInfoAppCc()
        ipath = ciac.get_unused_ccd_file()
        self.assertIsNotNone(ipath)

    def testGetExtSupport(self):
        """Get CC wide support flag"""
        ciac = ConfigInfoAppCc()
        # Default value
        flag = ciac.get_extended_ccd_supp()
        self.assertTrue(flag)

        # Test when flag set to False in site-config
        with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=MyConfigInfo):
            ciac = ConfigInfoAppCc()
            flag = ciac.get_extended_ccd_supp()
            self.assertFalse(flag)


class ConfigInfoAppValidationTests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation of Common class works"""
        ConfigInfoAppValidation()

    def testGetDensityFitness(self):
        """Get CC id code directory"""
        ciaval = ConfigInfoAppValidation()
        ipath = ciaval.get_density_fitness()
        self.assertIn("/ccp4/", ipath)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
