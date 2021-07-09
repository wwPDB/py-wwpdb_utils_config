from omegaconf import OmegaConf
import logging
import os
import sys
logger = logging.getLogger(__name__)



class Config(object):
    _instance = None

    def __new__(cls, path, other_data, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, path, other_data):
        if not path:
            path = os.environ['PATH_ONEDEP_CONFIG']
        self.path = path
        self.other_data = other_data
        self.config_from_yaml = None
        self.config_info_data = None
        self.conf = None
        self.load_configuration()

    def load_configuration(self):
        logger.info("Loading Configuration")
        logger.info(f"Config path : {self.path}/configuration.yaml")
        try:
            self.config_info_data = OmegaConf.create(self.other_data)
            self.config_from_yaml = OmegaConf.load(f"{self.path}/configuration.yaml")
            self.conf = OmegaConf.merge(self.config_info_data, self.config_from_yaml)
        except Exception as e:
            logger.error(f"Could not load configuration on path: {self.path}")
            logger.exception(e)

    def print_config_from_yaml(self):
        print(OmegaConf.to_yaml(self.config_from_yaml))

    def get_configuration(self):
        return self.conf


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    single_config_path = os.environ['PATH_ONEDEP_CONFIG']
    conf = Config(single_config_path, {})
    conf.print_config_from_yaml()
