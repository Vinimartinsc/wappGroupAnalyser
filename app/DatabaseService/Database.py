from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.ConfigService.Config import config
from app.LoggingService.DefaultLogger import logger

from .Models import Base # this is a re-export
from .Schemas import metadata

# Session = sessionmaker()
# engine = create_engine(f'{config.driver}{config.get_abs_path(config.database_path)}') # type: ignore
# session = Session(bind=engine)

class Database:
    def __init__(self) -> None:
        engine = create_engine(f'{config.driver}{config.get_abs_path(config.database_path)}') # type: ignore
        Session = sessionmaker()

        self.__engine = engine

        if not inspect(engine).has_table(table_name=config.table_name): #type: ignore
            metadata.create_all(engine)
        else:
            logger.error(f'Table {config.table_name} already exists, skipping table creation') #type: ignore

        self.__session = Session(bind=engine)

    def engine(self):
        return self.__engine

    def session(self):
        return self.__session

database = Database()
session = database.session()
engine = database.engine()
