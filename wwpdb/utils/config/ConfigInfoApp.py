#
# File:    ConfigInfoApp.py
# Date:    17-Oct-2020
#
# Updates:
#
#
##
"""
Provides common access patterns for application configuration locations to minimize verbose site-config files
"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import logging
import os.path
import sys
import warnings
from typing import Any, Dict, Optional, TextIO, cast

from wwpdb.utils.config.ConfigInfo import ConfigInfo

logger: logging.Logger = logging.getLogger(__name__)


class NoReferenceError(ValueError):
    def __init__(self) -> None:
        msg = "REFERENCE_PATH must be set in site_config"
        super().__init__(msg)


class NoTopWebSessionsError(ValueError):
    def __init__(self) -> None:
        msg = "SITE_WEB_APPS_TOP_SESSIONS_PATH must be set in site_config"
        super().__init__(msg)


class NoResourcesRoError(ValueError):
    def __init__(self) -> None:
        msg = "RO_RESOURCE_PATH must be set in site_config"
        super().__init__(msg)


class NoArchiveError(ValueError):
    def __init__(self) -> None:
        msg = "SITE_ARCHIVE_STORAGE_PATH must be set in site_config"
        super().__init__(msg)


class NoLocalAppsError(ValueError):
    def __init__(self) -> None:
        msg = "SITE_LOCAL_APPS_PATH must be set in site_config"
        super().__init__(msg)


class ConfigInfoAppBase:
    """Base class to provide common application lookups"""

    _cI: ConfigInfo
    _resourcedir: Optional[str]
    _rwresourcedir: Optional[str]
    _referencedir: Optional[str]
    _site_archive_dir: Optional[str]
    _site_local_apps_path: Optional[str]
    _top_webapps_path: Optional[str]
    _top_sessions_path: Optional[str]

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr) -> None:
        self._cI = ConfigInfo(siteId=siteId, verbose=verbose, log=log)
        self._resourcedir = None
        self._rwresourcedir = None
        self._referencedir = None
        self._site_archive_dir = None
        self._site_local_apps_path = None
        self._top_webapps_path = None
        self._top_sessions_path = None

    def _getlegacy(self, key: str, default: str, stacklevel: int = 4) -> str:
        """Retrieves key from configuration.  If key is found, provide a warning.  Only supporting strings for now as a return type
        As default value is mandatory - will always return a string.
        """
        val = cast("Optional[str]", self._cI.get(key))
        if val is not None:
            # logging will repeat with each occurance
            self.__warndeprecated("Access key %s has been used but is deprecated" % key, stacklevel=stacklevel)
        else:
            val = default
        return val

    def _getValue(self, key: str, default: Any = None) -> Any:  # XXXX str?
        val = self._cI.get(key)
        if val is None:
            val = default
        return val

    def _getresourcedir(self) -> Optional[str]:
        if self._resourcedir is None:
            self._resourcedir = self._cI.get("RO_RESOURCE_PATH")
        return self._resourcedir

    def _getrwresourcedir(self) -> Optional[str]:
        """Returns the RW resource directory if set in site-config"""
        if self._rwresourcedir is None:
            self._rwresourcedir = self._cI.get("RW_RESOURCE_PATH")
        return self._rwresourcedir

    def _getreferencedir(self) -> Optional[str]:
        if self._referencedir is None:
            self._referencedir = self._cI.get("REFERENCE_PATH")
        return self._referencedir

    def _get_site_archive_dir(self) -> Optional[str]:
        if self._site_archive_dir is None:
            self._site_archive_dir = self._cI.get("SITE_ARCHIVE_STORAGE_PATH")
        return self._site_archive_dir

    def _get_site_local_apps(self) -> Optional[str]:
        if self._site_local_apps_path is None:
            self._site_local_apps_path = self._cI.get("SITE_LOCAL_APPS_PATH")
        return self._site_local_apps_path

    def _get_top_web_apps_top_path(self) -> Optional[str]:
        if self._top_webapps_path is None:
            self._top_webapps_path = self._cI.get("SITE_WEB_APPS_TOP_PATH")
        return self._top_webapps_path

    def _get_top_sessions_path(self) -> Optional[str]:
        if self._top_sessions_path is None:
            self._top_sessions_path = self._cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")
        return self._top_sessions_path

    def get_site_packages_path(self) -> str:
        """Returns path to site packages path or nopath"""
        lapps = self._get_site_local_apps()
        if lapps is None:
            lapps = ""
        return self._getlegacy("SITE_PACKAGES_PATH", os.path.join(lapps, "packages"))

    def __warndeprecated(self, msg: str, stacklevel: int = 4) -> None:  # noqa: PLR6301
        """Logs warning message"""
        # stacklevel is to get up high enough to get caller
        warnings.warn(msg, DeprecationWarning, stacklevel=stacklevel)


class ConfigInfoAppCc(ConfigInfoAppBase):
    """Class to handle CCD and PRD locations and access"""

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr):
        super(ConfigInfoAppCc, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get_idcode_dir(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            reference_path = ""
        return os.path.join(reference_path, "id_codes")

    def get_extended_ccd_supp(self) -> bool:
        """Returns true if extended width CCD support enabled"""
        val = self._getValue("EXTENDED_CCD_SUPPORT", True)
        if val in ["True", "On", "true", "on", "1", True]:
            return True
        return False

    def get_site_refdata_top_cvs_sb_path(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            reference_path = ""
        ref_cc_dir = os.path.join(reference_path, "components")
        return self._getlegacy("SITE_REFDATA_TOP_CVS_SB_PATH", ref_cc_dir, stacklevel=5)

    def get_site_cc_dict_path(self, stacklevel: int = 4) -> str:
        rpath = self.get_site_refdata_top_cvs_sb_path()
        if rpath is None:
            rpath = ""
        site_cc_dict_path = os.path.join(rpath, "cc-dict")
        return self._getlegacy("SITE_CC_DICT_PATH", site_cc_dict_path, stacklevel=stacklevel)

    def get_cc_dict(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "Components-all-v3.cif")

    def get_cc_path_list(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "PATHLIST-v3")

    def get_cc_id_list(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "IDLIST-v3")

    def get_cc_dict_serial(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "Components-all-v3.sdb")

    def get_cc_dict_idx(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "Components-all-v3-r4.idx")

    def get_cc_db(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "chemcomp_v3.db")

    def get_cc_index(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "chemcomp-index.pic")

    def get_cc_parent_index(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "chemcomp-parent-index.pic")

    def get_cc_fp_patterns(self) -> str:
        return os.path.join(self.get_site_cc_dict_path(stacklevel=5), "fp_patterns.txt")

    def get_site_prdcc_cvs_path(self) -> str:
        rpath = self.get_site_refdata_top_cvs_sb_path()
        if rpath is None:
            rpath = ""
        site_prdcc_cvs_path = os.path.join(rpath, self._getValue("SITE_REFDATA_PROJ_NAME_PRDCC"))
        return self._getlegacy("SITE_PRDCC_CVS_PATH", site_prdcc_cvs_path)

    def get_site_cc_cvs_path(self) -> str:
        site_cc_cvs_path = os.path.join(
            self.get_site_refdata_top_cvs_sb_path(), self._getValue("SITE_REFDATA_PROJ_NAME_CC")
        )
        return self._getlegacy("SITE_CC_CVS_PATH", site_cc_cvs_path)

    def get_site_family_cvs_path(self) -> str:
        site_family_cvs_path = os.path.join(
            self.get_site_refdata_top_cvs_sb_path(), self._getValue("SITE_REFDATA_PROJ_NAME_PRD_FAMILY")
        )
        return self._getlegacy("SITE_FAMILY_CVS_PATH", site_family_cvs_path)

    def get_site_prd_cvs_path(self) -> str:
        site_prd_cvs_path = os.path.join(
            self.get_site_refdata_top_cvs_sb_path(), self._getValue("SITE_REFDATA_PROJ_NAME_PRD")
        )
        return self._getlegacy("SITE_PRD_CVS_PATH", site_prd_cvs_path)

    def get_site_prd_dict_path(self) -> str:
        site_prd_dict_path = os.path.join(self.get_site_refdata_top_cvs_sb_path(), "prd-dict")
        return self._getlegacy("SITE_PRD_DICT_PATH", site_prd_dict_path)

    def get_prd_summary_sdb(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "prd_summary.sdb")

    def get_prd_summary_cif(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "prd_summary.cif")

    def get_prd_dict_file(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "Prd-all-v3.cif")

    def get_prd_dict_serial(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "Prd-all-v3.sdb")

    def get_prd_cc_file(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "Prdcc-all-v3.cif")

    def get_prd_cc_serial(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "Prdcc-all-v3.sdb")

    def get_prd_family_mapping(self) -> str:
        return os.path.join(self.get_site_prd_dict_path(), "PrdFamilyIDMapping.lst")

    def get_unused_prd_file(self) -> str:
        unused_list_file = os.path.join(self.get_idcode_dir(), "unusedPrdId.lst")
        return unused_list_file

    def get_unused_ccd_file(self) -> str:
        unused_list_file = os.path.join(self.get_idcode_dir(), "unusedCodes.lst")
        return unused_list_file


class ConfigInfoAppCommon(ConfigInfoAppCc):
    """Class to provide common site-config lookups.
    The bases shoould be ConfigInfoAppBase when the rest of the uses have been updated
    """

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr) -> None:
        super(ConfigInfoAppCommon, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get_pdbx_dictionary_name_dict(self) -> Dict[str, str]:
        # Built in - so we know always present
        return cast("Dict[str, str]", self._cI.get("PDBX_DICTIONARY_NAME_DICT", {}))

    def get_mmcif_deposit_dict_filename(self) -> str:
        return self.get_pdbx_dictionary_name_dict().get("DEPOSIT", "DEPOSIT_undef")

    def get_mmcif_archive_current_dict_filename(self) -> str:
        return self.get_pdbx_dictionary_name_dict().get("ARCHIVE_CURRENT", "ARCHIVE_CURRENT_undef")

    def get_mmcif_archive_next_dict_filename(self) -> str:
        return self.get_pdbx_dictionary_name_dict().get("ARCHIVE_NEXT", "ARCHIVE_NEXT_undef")

    def get_mmcif_dict_path(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            raise NoReferenceError
        site_pdbx_dict_path = os.path.join(reference_path, "dict")
        return self._getlegacy("SITE_PDBX_DICT_PATH", site_pdbx_dict_path)

    def get_mmcif_next_dictionary_file_path(self) -> str:
        mmcif_dictionary_name = self.get_mmcif_deposit_dict_filename()
        mmcif_dictionary_file_name = mmcif_dictionary_name + ".dic"
        newpath = os.path.join(self.get_mmcif_dict_path(), mmcif_dictionary_file_name)
        return self._getlegacy("SITE_MMCIF_DICT_FILE_PATH", newpath)

    def get_mmcif_next_dictionary_sdb_file_path(self) -> str:
        mmcif_dictionary_name = self.get_mmcif_deposit_dict_filename()
        mmcif_dictionary_file_name = mmcif_dictionary_name + ".sdb"
        return os.path.join(self.get_mmcif_dict_path(), mmcif_dictionary_file_name)

    def get_mmcif_next_dictionary_odb_file_path(self) -> str:
        mmcif_dictionary_name = self.get_mmcif_deposit_dict_filename()
        mmcif_dictionary_file_name = mmcif_dictionary_name + ".odb"
        return os.path.join(self.get_mmcif_dict_path(), mmcif_dictionary_file_name)

    def get_mmcif_archive_dictionary_file_path(self) -> str:
        mmcif_dictionary_name = self.get_mmcif_archive_current_dict_filename()
        mmcif_dictionary_file_name = mmcif_dictionary_name + ".dic"
        return os.path.join(self.get_mmcif_dict_path(), mmcif_dictionary_file_name)

    def get_mmcif_vrpt_dictionary_file_path(self) -> str:
        base_name = self.get_pdbx_dictionary_name_dict().get("VRPT", "vrpt_undef")
        fname = base_name + ".dic"
        rpath = os.path.join(self.get_mmcif_dict_path(), fname)
        return rpath

    def get_site_local_apps_path(self) -> Optional[str]:
        return self._get_site_local_apps()

    def get_site_web_apps_top_path(self) -> Optional[str]:
        return self._get_top_web_apps_top_path()

    def get_site_web_apps_top_sessions_path(self) -> Optional[str]:
        return self._get_top_sessions_path()

    def get_site_web_apps_sessions_path(self) -> str:
        spath = self.get_site_web_apps_top_sessions_path()
        if spath is None:
            raise NoTopWebSessionsError
        fallback = os.path.join(spath, "sessions")
        return self._getlegacy("SITE_WEB_APPS_SESSIONS_PATH", fallback)

    def get_wf_logs_path(self) -> str:
        spath = self.get_site_web_apps_top_sessions_path()
        if spath is None:
            raise NoTopWebSessionsError
        return os.path.join(spath, "wf-logs")

    def get_site_annot_tools_path(self) -> str:
        spath = self.get_site_packages_path()
        return self._getlegacy("SITE_ANNOT_TOOLS_PATH", os.path.join(spath, "annotation"))

    def get_site_cc_apps_path(self) -> str:
        spath = self.get_site_packages_path()
        return self._getlegacy("SITE_CC_APPS_PATH", os.path.join(spath, "cc-tools-v2"))

    def get_sf_valid(self) -> str:
        spath = self.get_site_packages_path()
        return self._getlegacy("SF_VALID", os.path.join(spath, "sf-valid"))

    def get_site_cc_inchi_dir(self) -> str:
        lapps = self._get_site_local_apps()
        if lapps is None:
            raise NoLocalAppsError
        return self._getlegacy("SITE_CC_INCHI_DIR", os.path.join(lapps, "bin"))

    def get_site_cc_corina_dir(self) -> str:
        return self._getlegacy("SITE_CC_CORINA_DIR", os.path.join(self.get_site_packages_path(), "corina"))

    def get_site_cc_cactvs_dir(self) -> str:
        return self._getlegacy("SITE_CC_CACTVS_DIR", os.path.join(self.get_site_packages_path(), "cactvs", "bin"))

    def get_site_openbabel_dir(self) -> str:
        return os.path.join(self.get_site_packages_path(), "openbabel-2.2.3")

    def get_site_cc_babel_lib(self) -> str:
        return self._getlegacy("SITE_CC_BABEL_LIB", os.path.join(self.get_site_openbabel_dir(), "lib"))

    def get_site_cc_babel_dir(self) -> str:
        return self._getlegacy("SITE_CC_BABEL_DIR", os.path.join(self.get_site_openbabel_dir(), "lib"))

    def get_site_cc_babel_datadir(self) -> str:
        return self._getlegacy(
            "SITE_CC_BABEL_DATADIR", os.path.join(self.get_site_openbabel_dir(), "share", "openbabel", "2.2.3")
        )

    def get_site_cc_acd_dir(self) -> str:
        return self._getlegacy("SITE_CC_ACD_DIR", os.path.join(self.get_site_packages_path(), "acd"))

    def get_site_pisa_top_path(self) -> str:
        return self._getlegacy("SITE_PISA_TOP_PATH", os.path.join(self.get_site_packages_path(), "pisa"))

    def get_site_pisa_conf_path(self) -> str:
        return self._getlegacy("SITE_PISA_CONF_PATH", os.path.join(self.get_site_pisa_top_path(), "configure"))

    def get_site_cc_oe_dir(self) -> str:
        return self._getlegacy("SITE_CC_OE_DIR", os.path.join(self.get_site_packages_path(), "openeye"))

    def get_site_cc_oe_licence(self) -> str:
        oe_dir = self.get_site_cc_oe_dir()
        return self._getlegacy("SITE_CC_OE_LICENSE", os.path.join(oe_dir, "etc", "oe_license.txt"))

    def get_site_rcsb_apps_path(self) -> str:
        return self._getlegacy("SITE_RCSB_APPS_PATH", os.path.join(self.get_site_annot_tools_path(), "bin", "maxit"))

    def get_site_space_group_file_path(self) -> str:
        return self._getlegacy(
            "SITE_SPACE_GROUP_FILE_PATH",
            os.path.join(self.get_site_annot_tools_path(), "data", "ascii", "space_group.cif"),
        )

    def get_sg_center_file_path(self) -> str:
        return os.path.join(self.get_site_annot_tools_path(), "data", "ascii", "sg_center.cif")

    def get_taxdump_path(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            raise NoReferenceError
        site_pdbx_dict_path = os.path.join(reference_path, "taxdump")
        return self._getlegacy("SITE_REFDATA_TAXONOMY_PATH", site_pdbx_dict_path)

    def get_for_release_path(self) -> str:
        adir = self._get_site_archive_dir()
        if adir is None:
            raise NoArchiveError
        release_path = os.path.join(adir, "for_release")
        return self._getlegacy("FOR_RELEASE_DATA_PATH", release_path)

    def get_for_release_beta_path(self) -> str:
        adir = self._get_site_archive_dir()
        if adir is None:
            raise NoArchiveError
        release_path = os.path.join(adir, "for_release_beta")
        return release_path

    def get_for_release_version_path(self) -> str:
        adir = self._get_site_archive_dir()
        if adir is None:
            raise NoArchiveError
        release_path = os.path.join(adir, "for_release_version")
        return release_path

    def get_status_export_path(self) -> str:
        status_path = os.path.join(self.get_for_release_path(), "status")
        return self._getlegacy("STATUS_EXPORT_DATA_PATH", status_path)

    def get_nmr_exchange_path(self) -> str:
        adir = self._get_site_archive_dir()
        if adir is None:
            raise NoArchiveError
        release_path = os.path.join(adir, "nmr_exchange_data")
        return self._getlegacy("NMR_EXCHANGE_DATA", release_path)

    def get_site_refdata_sequence_path(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            raise NoReferenceError
        sequence_path = os.path.join(reference_path, "sequence")
        return self._getlegacy("SITE_REFDATA_SEQUENCE_PATH", sequence_path)

    def get_site_refdata_sequence_db_path(self) -> str:
        reference_path = self.get_site_refdata_sequence_path()
        seq_db_path = os.path.join(reference_path, "seq-db")
        return self._getlegacy("SITE_REFDATA_SEQUENCE_DB_PATH", seq_db_path)

    def get_citation_update_path(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            raise NoReferenceError
        return os.path.join(reference_path, "citation_updates")

    def get_citation_finder_path(self) -> str:
        reference_path = self._getreferencedir()
        if reference_path is None:
            raise NoReferenceError
        return os.path.join(reference_path, "citation_finder")

    def get_node_bin_path(self) -> str:
        return os.path.join(self.get_site_packages_path(), "node", "bin", "node")

    def get_molstar_packages_path(self) -> str:
        return os.path.join(self.get_site_packages_path(), "molstar", "node_modules", "molstar")

    def get_volume_server_packages_path(self) -> str:
        return os.path.join(self.get_molstar_packages_path(), "lib", "commonjs", "servers", "volume")

    def get_volume_server_pack_path(self) -> str:
        return os.path.join(self.get_volume_server_packages_path(), "pack.js")

    def get_volume_server_query_path(self) -> str:
        return os.path.join(self.get_volume_server_packages_path(), "query.js")

    def get_db_loader_path(self) -> str:
        return os.path.join(self.get_site_packages_path(), "dbloader", "bin", "db-loader")

    def get_resources_da_internal_path(self) -> str:
        rdir = self._getresourcedir()
        if rdir is None:
            raise NoResourcesRoError
        return os.path.join(rdir, "da_internal")

    def get_resources_da_internal_all_path(self) -> str:
        rdir = self._getresourcedir()
        if rdir is None:
            raise NoResourcesRoError
        return os.path.join(rdir, "da_internal_all")

    def get_site_da_internal_schema_path(self) -> str:
        return self._getlegacy(
            "SITE_DA_INTERNAL_SCHEMA_PATH",
            os.path.join(self.get_resources_da_internal_path(), "status_rcsb_schema_da.cif"),
        )

    def get_site_da_internal_status_schema_path(self) -> str:
        return self._getlegacy(
            "SITE_DA_INTERNAL_STATUS_SCHEMA_PATH",
            os.path.join(self.get_resources_da_internal_path(), "database_status_history_schema.cif"),
        )

    def get_site_da_internal_public_schema_path(self) -> str:
        return self._getlegacy(
            "SITE_DA_INTERNAL_PUBLIC_SCHEMA_PATH",
            os.path.join(self.get_resources_da_internal_all_path(), "schema_map_pdbx_v5.cif"),
        )

    def get_resources_wfe_path(self) -> str:
        rdir = self._getresourcedir()
        if rdir is None:
            raise NoResourcesRoError
        return os.path.join(rdir, "wfe")

    def get_wf_defs_path(self) -> str:
        return self._getlegacy("SITE_WF_XML_PATH", os.path.join(self.get_resources_wfe_path(), "wf-defs"))

    def get_site_registry_file_path(self) -> str:
        return self._getlegacy("SITE_REGISTRY_FILE_PATH", os.path.join(self.get_resources_wfe_path(), "actionData.xml"))

    def get_file_activity_db_support(self) -> bool:
        """Returns true if file activity database support enabled"""
        val = self._getValue("FILE_ACTIVITY_DB_SUPPORT", False)
        if val in ["True", "On", "true", "on", "1", True]:
            return True
        return False


class ConfigInfoAppDepUI(ConfigInfoAppBase):
    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr) -> None:
        super(ConfigInfoAppDepUI, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def __get_depui_dir(self) -> str:
        """Returns the preferred path to depui subdir of resources_ro"""
        rdir = self._getresourcedir()
        if rdir is None:
            raise NoResourcesRoError
        return os.path.join(rdir, "depui")

    def __get_rwdepui_dir(self) -> Optional[str]:
        """Returns the preferred path to depui subdir of resources_rw if variable set or None"""
        rwpath = self._getrwresourcedir()
        if rwpath is not None:
            return os.path.join(rwpath, "depui")
        return None

    def get_depui_resources_ro_dir(self) -> str:
        """Performs legacy lookup of depUI subdir referenced through DEPUI_RESOURCE_PATH.
        Returns either legacy or new hardcoded lookup"""
        return self._getlegacy("DEPUI_RESOURCE_PATH", self.__get_depui_dir())

    def get_site_access_info_file_path(self) -> str:
        newpath = os.path.join(self.__get_depui_dir(), "site_access_info.json")
        return self._getlegacy("SITE_ACCESS_INFO_FILE_PATH", newpath)

    def get_site_dataset_siteloc_file_path(self) -> str:
        """
        Returhs in the following order:
        site-config variable
        r/w tree path
        r/o resources path
        """
        fName = "site_dataset_siteloc_info.json"
        rwdepuipath = self.__get_rwdepui_dir()

        newpath = None

        # Test if rw file exists. else old
        if rwdepuipath is not None:
            fpath = os.path.join(rwdepuipath, fName)
            if os.path.exists(fpath):
                newpath = fpath

        if newpath is None:
            newpath = os.path.join(self.__get_depui_dir(), fName)

        # Legacy definition override
        return self._getlegacy("SITE_DATASET_SITELOC_FILE_PATH", newpath)

    def get_deposit_ui_support(self) -> bool:
        """Returns True if deposit_ui environment is in place on this site."""
        val = self._getValue("SITE_ARCHIVE_UI_STORAGE_PATH")
        return bool(val)


class ConfigInfoAppEm(ConfigInfoAppBase):
    """Access configuration for EM schema, resources, etc."""

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr) -> None:
        super(ConfigInfoAppEm, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def __getemddir(self) -> str:
        """Returns preferred path to emd subdir of resources_ro"""
        rdir = self._getresourcedir()
        if rdir is None:
            raise NoResourcesRoError
        return os.path.join(rdir, "emd")

    def __getlegacyemdpath(self) -> str:
        """Performs legacy lookup of emd subdir referenced through SITE_EM_DICT_PATH.
        Returns either legacy or new hardcoded lookup"""
        return self._getlegacy("SITE_EM_DICT_PATH", self.__getemddir())

    def get_emd_mapping_file_path(self) -> str:
        """Returns the full path to the em <-> emd translator configuration file"""
        # Formerly SITE_EXT_DICT_MAP_EMD_FILE_PATH provided the full path
        newpath = os.path.join(self.__getemddir(), "emd_map_v2.cif")
        val = self._getlegacy("SITE_EXT_DICT_MAP_EMD_FILE_PATH", newpath)
        return val

    def get_emd_fsc_scheme_file_path(self) -> str:
        """Returns the full path the EMD FSC schema file"""
        # Former access was through SITE_EM_DICT_PATH
        return os.path.join(self.__getlegacyemdpath(), "emdb_fsc.xsd")


class ConfigInfoAppValidation(ConfigInfoAppBase):
    """Access configuration for Validation run time variables"""

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr) -> None:
        super(ConfigInfoAppValidation, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get_validation_tools_path(self) -> str:
        return self._getlegacy("VALIDATIONTOOLSPATH", os.path.join(self.get_site_packages_path(), "ValidationSupport"))

    def get_sf_valid(self) -> str:
        return self._getlegacy("DCCROOT", os.path.join(self.get_site_packages_path(), "sf-valid"))

    def get_pymolexe(self) -> str:
        return self._getlegacy("PYMOLEXE", os.path.join(self.get_site_packages_path(), "open_pymol", "pymol"))

    def get_java_home(self) -> str:
        return self._getlegacy("JAVA_HOME", os.path.join(self.get_site_packages_path(), "java", "jdk"))

    def get_ccp4root(self) -> str:
        return self._getlegacy("CCP4ROOT", os.path.join(self.get_site_packages_path(), "ccp4"))

    def get_validator_ccp4setup(self) -> str:
        return self._getlegacy("VALIDATOR_CCP4SETUP", os.path.join(self.get_ccp4root(), "bin", "ccp4.setup-sh"))

    def get_phenixroot(self) -> str:
        return self._getlegacy("PHENIXROOT", os.path.join(self.get_site_packages_path(), "phenix"))

    def get_cnsroot(self) -> str:
        return self._getlegacy("CNSROOT", os.path.join(self.get_site_packages_path(), "cns_solve"))

    def get_edstools(self) -> str:
        return self._getlegacy("EDSTOOLS", os.path.join(self.get_site_packages_path(), "EDStools"))

    def get_cif2text(self) -> str:
        return self._getlegacy("CIF2TEXT", os.path.join(self.get_edstools(), "CIF2TEXT", "cif2text_internal"))

    def get_ccp4symoplib(self) -> str:
        return self._getlegacy("CCP4SYMOPLIB", os.path.join(self.get_edstools(), "symop.lib"))

    def get_edssubpath(self) -> str:
        return self._getlegacy("EDSSUBPATH", os.path.join(self.get_edstools(), "Gerard"))

    def get_dataman(self) -> str:
        return self._getlegacy("DATAMAN", os.path.join(self.get_edssubpath(), "LX_DATAMAN"))

    def get_o2d(self) -> str:
        return self._getlegacy("O2D", os.path.join(self.get_edssubpath(), "LX_O2D"))

    def get_filpdb(self) -> str:
        return self._getlegacy("FILPDB", os.path.join(self.get_edssubpath(), "lx_filpdb"))

    def get_mapman(self) -> str:
        return self._getlegacy("MAPMAN", os.path.join(self.get_edssubpath(), "lx_mapman"))

    def get_stat2o(self) -> str:
        return self._getlegacy("STAT2O", os.path.join(self.get_edssubpath(), "LX_STAT2O"))

    def get_pdbmod(self) -> str:
        return self._getlegacy("PDBMOD", os.path.join(self.get_edssubpath(), "pdb_mod"))

    def get_osymdir(self) -> str:
        return self._getlegacy("OSYMDIR", os.path.join(self.get_site_packages_path(), "symm"))

    def get_chimerax(self) -> str:
        return self._getlegacy("CHIMERAXDIR", os.path.join(self.get_site_packages_path(), "ChimeraX", "bin"))

    def get_chimera(self) -> str:
        return self._getlegacy("CHIMERADIR", os.path.join(self.get_site_packages_path(), "chimera", "bin"))

    def get_chimera_dir(self) -> str:
        return self._getlegacy("CHIMERADIR", os.path.join(self.get_site_packages_path(), "chimera"))

    def get_density_fitness(self) -> str:
        return os.path.join(self.get_ccp4root(), "bin", "density-fitness")


class ConfigInfoAppMessaging(ConfigInfoAppBase):
    """A class for messaging related configuration"""

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr):
        super(ConfigInfoAppMessaging, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get_msgdb_support(self) -> bool:
        """Returns true if site is using database for communication"""
        status = bool(self._cI.get("SITE_MESSAGE_DB_NAME"))
        return status


class ConfigInfoAppCommunication(ConfigInfoAppBase):
    """Access configuration for sending email"""

    def __init__(self, siteId: Optional[str] = None, verbose: bool = True, log: TextIO = sys.stderr):
        super(ConfigInfoAppCommunication, self).__init__(siteId=siteId, verbose=verbose, log=log)

    def get_noreply_address(self) -> str:
        """Returns the noreply email address"""

        noreply_email = cast("str", self._cI.get("SITE_NOREPLY_EMAIL", "noreply@mail.wwpdb.org"))

        return noreply_email

    def get_mailserver_name(self) -> str:
        """Returns the sendmail local server or relay host"""

        return cast("str", self._cI.get("SITE_MAILSERVER_NAME", "localhost"))

    def get_system_notification_address(self) -> str:
        """Returns the email address to notify for errors"""

        return cast("str", self._cI.get("SITE_ERROR_EMAIL", "deposit-help@mail.wwpdb.org"))
