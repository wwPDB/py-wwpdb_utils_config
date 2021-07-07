from omegaconf import OmegaConf
import logging
import os
logger = logging.getLogger(__name__)



class Config():
    _instance = None

    def __new__(cls, *args, **kwargs):
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

    def load_configuration(self):
        try:
            config_info_data = OmegaConf.create(self.other_data)
            config_from_yaml = OmegaConf.load(f"{self.path}/configuration.yaml")
            self.conf = OmegaConf.merge(config_info_data, config_from_yaml)
        except Exception as e:
            logger.error(f"Could not load configuration on path: {self.path}")
            logger.exception(e)

    def print_config_from_yaml(self):
        print(OmegaConf.to_yaml(self.config_from_yaml))

    def get_configuration(self):
        return self.conf


if __name__ == '__main__':
    single_config_path = os.environ['PATH_ONEDEP_CONFIG']
    print('Fetching YAML from:')
    conf = Config(single_config, other_data)
    print('Printing Configuration:')
    conf.print_config_from_yaml()
