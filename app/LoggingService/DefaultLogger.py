import os
import yaml
import logging

import logging.config
from app.ConfigService.Config import config

class Logger:
    def __init__(self) -> None:
        with open(os.path.join(config.project_workdir, 'logging.config.yaml'), 'r', encoding='utf8') as configFile: # type: ignore
            logfile = yaml.safe_load(configFile)
            logging.config.dictConfig(logfile)

        self.__logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.__logger;

logger = Logger().get_logger()