from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.ConfigService.Config import config
from app.LoggingService.DefaultLogger import logger

from .Models import Base  # this is a re-export
from .Schemas import metadata


class Database:
    def __init__(self) -> None:

        if (config.driver == 'sqlite:///'):
            db_path = config.get_abs_path(config.database_path)
        else:
            db_path = config.database_path

        try:
            # this method of creation does not
            engine = create_engine(
                f'{config.driver}{db_path}')  # type: ignore

            Session = sessionmaker()

            self.__engine = engine

            if not inspect(engine).has_table(table_name=config.table_name):  # type: ignore
                metadata.create_all(engine)
            else:
                # type: ignore
                logger.error(
                    f'Table {config.table_name} already exists, skipping table creation')  # type: ignore

            self.__session = Session(bind=engine)

        except OperationalError as e:
            print(f"Error: {e}")
            logger.error(
                "Unable to access database, please verify if path exist")

    def engine(self):
        return self.__engine

    def session(self):
        return self.__session


database = Database()
session = database.session()
engine = database.engine()
