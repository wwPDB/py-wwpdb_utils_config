##
#
"""
Test cases for retrieving ProjectVersionInfo..
"""
__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import sys
import unittest
import time
import platform
import logging
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

from wwpdb.utils.config.ProjectVersionInfo import ProjectVersionInfo  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ProjectInfoTests(unittest.TestCase):
    """
    Test cases for mapping data sets ids to server sites ids.
    """

    def setUp(self):
        self.__startTime = time.time()
        logger.debug("Starting %s at %s", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

        self.__lfh = sys.stdout
        self.__verbose = True
        #

    def tearDown(self):
        endTime = time.time()
        logger.debug("Completed %s at %s (%.4f seconds)", self.id(), time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTime)

    def testGetVersion(self):
        """Test case -  get project version"""
        pvi = ProjectVersionInfo()
        vers = pvi.getVersion()
        self.assertNotEqual(vers, "unknown")

    def testGetVersionFile(self):
        """Test case -  get project version"""
        pvi = ProjectVersionInfo()
        versfile = pvi.getVersionFile()
        self.assertIsNotNone(versfile)

    @patch.object(ProjectVersionInfo, 'getVersionFile', return_value="/tmp/non-exsitant-file/one-hopes")
    def testGetVersionMissing(self, mock_pvi):
        """Test case -  get project version - missing version"""
        pvi = ProjectVersionInfo()
        vers = pvi.getVersion()
        self.assertEqual(vers, "unknown")
        self.assertTrue(mock_pvi.called)


def suiteProjectVersion():  # pragma: no cover
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ProjectInfoTests("testGetVersion"))
    suiteSelect.addTest(ProjectInfoTests("testGetVersionFile"))
    suiteSelect.addTest(ProjectInfoTests("testGetVersionMissing"))
    return suiteSelect


if __name__ == "__main__":  # pragma: no cover
    #
    mySuite = suiteProjectVersion()
    idRes = unittest.TextTestRunner(verbosity=2).run(mySuite).wasSuccessful()

    sys.exit(not idRes)
