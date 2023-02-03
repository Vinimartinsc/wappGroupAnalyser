from sqlalchemy import MetaData
from sqlalchemy import Table, Column, String, Integer

from app.ConfigService.Config import config

metadata = MetaData()

# Messages Collection Table
Messages = Table(
    config.table_name, # type: ignore # must be the dataset name and datetime. I.e. exemple_dataset_20220201 
    metadata,
    Column("id", Integer,  primary_key=True),
    Column("at_datetime", String() , nullable=False),
    Column("author", String(), nullable=False),
    Column("raw", String(), nullable= False),
    Column("type", String(), nullable=False),
    Column("content", String(), nullable=False)
)