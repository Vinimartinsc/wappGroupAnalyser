import os
from pathlib import Path
import yaml


class Config:
    '''Object wraps the app configs present in app.config.yaml.'''
    
    APP_NAME = "wappGroupAnalyser"

    def __init__(self):
        self.__set_paths()
        
        with open(os.path.join(self.__project_workdir, 'app.config.yaml'), 'r', encoding='utf8') as configFile:
            configfile = yaml.safe_load(configFile)

            configfile['project_workdir'] = self.__project_workdir
            configfile['project_root'] = self.__project_root

        self.__dict__.update(configfile)


    def __set_paths(self):
        path, directory = os.path.split(os.path.abspath(__file__))

        while directory and directory != self.APP_NAME:
            path, directory = os.path.split(path)

        if directory == self.APP_NAME:
            self.__project_workdir = os.path.join(path, directory)
            self.__project_root = os.path.join(self.__project_workdir, 'app')
        else:
            raise Exception("Couldn't determine path to the project root.")


    def get_abs_path(self, path: str):
        '''Return the absolute path of a given path relative to the project path.'''
        return os.path.join(self.__project_workdir, path)


config = Config()
