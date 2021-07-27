from omegaconf import OmegaConf
from pathlib import Path
import logging
import os
import sys
logger = logging.getLogger(__name__)


class Config(object):
    _instance = None

    def __new__(cls, path, other_data, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
            cls._instance.init(path, other_data, *args, **kwargs)
        return cls._instance

    def init(self, path, other_data):
        if not path:
            path = os.environ['PATH_ONEDEP_CONFIG']
        self.path = path
        self.other_data = other_data
        self.config_from_yaml = None
        self.config_info_data = None
        self.conf = None

    def load_configuration(self):
        if self.conf is not None:
            logger.info("Configuration loaded from cache")
            return
        logger.info(f"Loading Configuration from path : {self.path}/configuration.yaml")
        try:
            self.config_info_data = OmegaConf.create(self.other_data)

            optional_base_file = Path(f"{self.path}/base.yaml")
            mandatory_config_file = Path(f"{self.path}/configuration.yaml")

            if optional_base_file.exists():
                base_config = OmegaConf.load(optional_base_file)
                self.conf = OmegaConf.merge(self.config_info_data, base_config)

            self.config_from_yaml = OmegaConf.load(mandatory_config_file)
            self.conf = OmegaConf.merge(self.conf, self.config_from_yaml)
            logger.info("Configuration loaded successfully")

        except Exception as e:
            logger.error(f"Could not load configuration on path: {self.path}")
            logger.exception(e)

    def print_config(self):
        print(OmegaConf.to_yaml(self.conf))

    def get_configuration(self):
        return self.conf


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    single_config_path = os.environ['PATH_ONEDEP_CONFIG']
    site = os.environ['WWPDB_SITE_ID'] or 'PDBE_STG'

    cid = ConfigInfoData(siteId=site, verbose=True, single_config=True)
    other_data = cid.getConfigDictionary()
    conf = Config(single_config_path, other_data)
    print(conf._instance)
    another_object = Config(single_config_path)
    print(conf._instance)
    print(another_object._instance)
