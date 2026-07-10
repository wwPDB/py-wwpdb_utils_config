##
#
# File:    ConfigInfoFileTests.py
# Author:  E. Peisach
# Date:    5-Oct-2018
# Version: 0.001
##
"""
Test cases for generation of configuration and use

"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import io
import os
import platform
import unittest

# from unittest import mock
from datetime import datetime

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

from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId  # noqa: E402

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(HERE)


class ConfigInfoFileTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testGetSiteId(self) -> None:
        self.assertEqual(getSiteId(), "WWPDB_DEPLOY_TEST")
        # # Test fallback - with no environment set
        # with mock.patch.dict(os.environ):
        #     # Remove WWPDB_SITE_ID if exists
        #     os.environ.pop("WWPDB_SITE_ID", None)
        #     self.assertEqual(getSiteId(), "WWPDB_DEPLOY")

    def testCache(self) -> None:
        cI = ConfigInfo()
        self.assertEqual(cI.get("VARTEST"), "Hello")
        self.assertEqual(cI.get("TESTVAR1"), "1")
        self.assertEqual(cI.get("TESTVAR2"), "2")

    def testDump(self) -> None:
        cI = ConfigInfo()
        stream = io.StringIO()
        cI.dump(stream)
        stream.seek(0)
        data = stream.readlines()
        self.assertTrue(len(data) > 50, "Dump ConfigInfo too small")
        stream.close()

    def testMock(self) -> None:
        cI = ConfigInfo()
        self.assertEqual(cI.get("DEPLOY_PATH"), os.path.join(rwMockTopPath, "da_top"))

    def testBuiltin(self) -> None:
        """Tests if common built in definitions are set"""
        cI = ConfigInfo()
        self.assertIsNotNone(cI.get("PROJECT_VAL_REL_CUTOFF"))
        self.assertIsNone(cI.get("PROJECT_RANDOM"))

    def _parseTime(self, timestr: str) -> datetime:
        weeknum = datetime.today().strftime("%U")  # noqa: DTZ002
        this_year = datetime.today().strftime("%G")  # noqa: DTZ002
        mytime = f"{this_year}:{weeknum}:{timestr}"
        time_t = datetime.strptime(mytime, "%Y:%U:%a:%H:%M:%S")  # noqa: DTZ007
        return time_t

    def testParseCutoff(self) -> None:
        """Tests if common built in definitions are set"""
        cI = ConfigInfo()
        val = cI.get("PROJECT_VAL_REL_CUTOFF")

        self.assertEqual(len(val), 2)

        time_t = self._parseTime(val["start"])
        self.assertEqual(time_t.hour, 9)
        self.assertEqual(time_t.minute, 0)
        self.assertEqual(time_t.second, 0)
        self.assertEqual(time_t.isoweekday(), 5)

        time_t = self._parseTime(val["end"])
        self.assertEqual(time_t.hour, 23)
        self.assertEqual(time_t.minute, 59)
        self.assertEqual(time_t.second, 59)
        self.assertEqual(time_t.isoweekday(), 5)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
