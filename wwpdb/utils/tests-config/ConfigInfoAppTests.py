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
import unittest
import warnings
import sys

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

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
crw.createtree(["site-config", "depuiresources", "webapps"])
# Use populate r/w site-config using top mock site-config
SiteConfigSetup().setupEnvironment(rwMockTopPath, rwMockTopPath)

from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppEm  # noqa: E402
from wwpdb.utils.config.ConfigInfo import ConfigInfo  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class MyConfigInfo(ConfigInfo):
    """A class to set SITE_EXT_DICT_MAP_EMD_FILE_PATH"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(MyConfigInfo, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get(self, keyWord, default=None):
        if keyWord == "SITE_EXT_DICT_MAP_EMD_FILE_PATH":
            val = "/tmp/emd/emd_map_v2.cif"
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
    def testWarningMessage(self, mock1):  # pylint: disable=unused-argument
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
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "but is deprecated" in str(w[-1].message)

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
            assert len(w) == 0


if __name__ == "__main__":
    unittest.main()
