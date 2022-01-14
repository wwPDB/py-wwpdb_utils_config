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

from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppDepUI  # noqa: E402
from wwpdb.utils.config.ConfigInfo import ConfigInfo  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class MyConfigInfo(ConfigInfo):
    """A class to setup tests for DepUI config"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        self._resources_ro = "/tmp/resources"
        self._resources_rw = None
        self._ds_loc_path = None
        super(MyConfigInfo, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get(self, keyWord, default=None):
        if keyWord == "SITE_DATASET_SITELOC_FILE_PATH":
            val = self._ds_loc_path
        elif keyWord == "RO_RESOURCE_PATH":
            val = self._resources_ro
        elif keyWord == "RW_RESOURCE_PATH":
            val = self._resources_rw
        else:
            # sys.stderr.write("XXXXX Unknown site config fetching %s\n" % keyWord)
            val = super(MyConfigInfo, self).get(keyWord=keyWord, default=default)

        return val


class LegacyConfig(MyConfigInfo):
    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(LegacyConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self._ds_loc_path = "/tmp/res/path"


class RoConfig(MyConfigInfo):
    """R/O path - as R/W not set"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(RoConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)


class RwConfig(MyConfigInfo):
    """R/W path - as R/W not set"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(RwConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self._resources_rw = os.path.join(TESTOUTPUT, "depuirw")


class ConfigInfoAppDepUITests(unittest.TestCase):
    @staticmethod
    def testInstantiate():
        """Test if instantiation of EM class works"""
        ConfigInfoAppDepUI()

    def testDatasetSiteLoc(self):
        """Tests the dataset location options"""

        # Disable warnings
        with warnings.catch_warnings(record=True) as _w:  # noqa: F841
            with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=LegacyConfig) as _mock_method:  # noqa: F841
                cia = ConfigInfoAppDepUI()
                slPath = cia.get_site_dataset_siteloc_file_path()
                self.assertEqual(slPath, "/tmp/res/path")
            with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=RoConfig) as _mock_method:  # noqa: F841
                cia = ConfigInfoAppDepUI()
                slPath = cia.get_site_dataset_siteloc_file_path()
                self.assertEqual(slPath, "/tmp/resources/depui/site_dataset_siteloc_info.json")

            # RW path to avoid fallbacks tests for destination file
            rwpath = os.path.join(TESTOUTPUT, "depuirw", "depui")
            if not os.path.exists(rwpath):
                os.makedirs(rwpath)
            testOutPath = os.path.join(rwpath, "site_dataset_siteloc_info.json")
            if not os.path.exists(testOutPath):
                with open(testOutPath, "w") as _fout:  # noqa: F841
                    pass

            with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=RwConfig) as _mock_method:  # noqa: F841
                cia = ConfigInfoAppDepUI()
                slPath = cia.get_site_dataset_siteloc_file_path()
                self.assertEqual(slPath, testOutPath)


if __name__ == "__main__":
    unittest.main()
