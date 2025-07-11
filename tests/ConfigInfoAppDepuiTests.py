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
from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppDepUI  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


class MyConfigInfo(ConfigInfo):
    """A class to setup tests for DepUI config"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        self._resources_ro = "/tmp/resources"  # noqa: S108
        self._resources_rw = None
        self._ds_loc_path = None
        self._archive_ui_path = None
        super(MyConfigInfo, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get(self, keyWord, default=None):
        if keyWord == "SITE_DATASET_SITELOC_FILE_PATH":
            val = self._ds_loc_path
        elif keyWord == "RO_RESOURCE_PATH":
            val = self._resources_ro
        elif keyWord == "RW_RESOURCE_PATH":
            val = self._resources_rw
        elif keyWord == "SITE_ARCHIVE_UI_STORAGE_PATH":
            val = self._archive_ui_path
        else:
            # sys.stderr.write("XXXXX Unknown site config fetching %s\n" % keyWord)
            val = super(MyConfigInfo, self).get(keyWord=keyWord, default=default)

        return val


class LegacyConfig(MyConfigInfo):
    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(LegacyConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self._ds_loc_path = "/tmp/res/path"  # noqa: S108


class RoConfig(MyConfigInfo):
    """R/O path - as R/W not set"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(RoConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)


class RwConfig(MyConfigInfo):
    """R/W path - as R/W not set"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(RwConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self._resources_rw = os.path.join(TESTOUTPUT, "depuirw")


class SplitDepositUIConfig(MyConfigInfo):
    """deposit-ui configuration"""

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        super(SplitDepositUIConfig, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self._archive_ui_path = "/tmp/pathsomewhere"  # noqa: S108


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
                self.assertEqual(slPath, "/tmp/res/path")  # noqa: S108
            with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=RoConfig) as _mock_method:  # noqa: F841
                cia = ConfigInfoAppDepUI()
                slPath = cia.get_site_dataset_siteloc_file_path()
                self.assertEqual(slPath, "/tmp/resources/depui/site_dataset_siteloc_info.json")  # noqa: S108

            # RW path to avoid fallbacks tests for destination file
            rwpath = os.path.join(TESTOUTPUT, "depuirw", "depui")
            if not os.path.exists(rwpath):  # pragma: no cover
                os.makedirs(rwpath)
            testOutPath = os.path.join(rwpath, "site_dataset_siteloc_info.json")
            if not os.path.exists(testOutPath):  # pragma: no cover
                with open(testOutPath, "w") as _fout:  # noqa: F841
                    pass

            with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=RwConfig) as _mock_method:  # noqa: F841
                cia = ConfigInfoAppDepUI()
                slPath = cia.get_site_dataset_siteloc_file_path()
                self.assertEqual(slPath, testOutPath)

    def testMessageSubjects(self):
        """Tests the dataset location options"""
        ci = ConfigInfo()
        subj = ci.get("MESSAGE_SUBJECTS")
        self.assertTrue(len(subj) > 5)

        appmess = ci.get("COMMUNICATION_APPROVAL_WITHOUT_CHANGES_MESSAGE_SUBJECTS")
        self.assertTrue(len(appmess) == 1, appmess)
        self.assertTrue(appmess == ["Approval without corrections"])

    def testDepositUiSupport(self):
        """Tests the deposit-ui support"""
        cia = ConfigInfoAppDepUI()
        self.assertFalse(cia.get_deposit_ui_support())

        with patch("wwpdb.utils.config.ConfigInfoApp.ConfigInfo", side_effect=SplitDepositUIConfig) as _mock_method:  # noqa: F841
            cia = ConfigInfoAppDepUI()
            self.assertTrue(cia.get_deposit_ui_support())


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
