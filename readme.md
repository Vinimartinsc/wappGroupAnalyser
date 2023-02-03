# Whatsapp group messages analyser
Analyse, label and store exported whatsapp group messages in a text format. 
Once stored in database, they can be accessed by other packages like Pandas.

_You can also read this in [English](readme.md) and [Português do Brasil](readme.pt.md)_

## Project structure
```
<root>
│
├── .datasets
│   └── example.txt
│
├── .db
│
├── app
│   ├── ConfigService
│   ├── DatabaseService
│   ├── LoggingService
│   ├── WappMessageIngestService
│   └── main.py
│
├── notebooks
│   └── example.ipynb
│
├── app.config.yaml
└── logging.config.yaml
```

### .datasets
  Default folder to receive the exported group message files. There is a example file named _example.txt_, that is a dataset for demonstration purpose.

### .db 
  Default folder for database files, generaly used for sqlite databases.

### app
  Package containing all the code for processing the datasets. 

### notebooks 
  Default folder for IPython notebooks. There can be found a example notebook named _example.ipynb_.

### app.config.yaml
  File containing app general configurations like default folder locations or database connection parameters.

### logging.config.yaml
  File containing log formating configurations.

### app/main.py
  The app package main entry point.

### app/ConfigService
  Service for loading available configurations in app.config.yaml file.

### app/DatabaseSErvice
  Service for database manipulation.

### app/WappMessageIngestService
  Service for processing and manipulate Whatsapp group messages.

## The WhatsappMessagesDTO object
  Is a object that represents a whatsapp message. The params are private, so it has to be accessed by its _get_ accessors. The table below list the available params in the object.

  | Param | Type | Description | Acessor |
  | ---- | ----- | --- | --- |
  | __at_datetime | datetime | Represents date and time a message was sent. | get_datetime() |
  | __author | str | Represents a author, can be a name or phone number. | get_author() |
  | __content | List[str] | The message _de facto_. | get_content() |
  | __raw | str | The raw message string as in the dataset file line. | get_raw() |
  | __type | str | A message label. I.e. COMMON_MESSAGE.| get_type() |

## The Message categories (Type)
  A message can be labeled by its formfactor. The table below describes the labeling criteria.

  | Label | Description |
  | --- | --- |
  | COMMON_CONVERSATION | A common message exchange between group members |
  | MEMBER_LEFT_NOTIFICATION | A system notification that a user is no longer part of a group | 
  | MEMBER_ADDED_NOTIFICATION | A system notification that a user is now part of a group | 
  | MEMBER_ID_MAPPING_NOTIFICATION | A system notification that a user has changed number | 
  | OTHER | A message could not be labeled in any other category |


## Usage

  First it is needed to open and read the dataset text file. This can be done by using the __read_dataset_file()__ method. This will process the dataset file and return a array of objects, where each object is a __WhatsappMessagesDTO__ object containing the message data. The list of messages can be loaded to a database with __load_database_with_dataset()__. It will generate by default a sqlite database file in .db folder. See the example below.
 
 ```python
  
  import os

  # If executing from a notebook in a folder that is not the project root
  # it is needed to add the line below to access the app.main package.
  # import sys; sys.path.append("../")

  from app.main import read_dataset_file, load_database_with_dataset


  # read export file from whatsapp export - path has to point to a directory or file inside project
  wpp_messages = read_dataset_file(os.path.join('.datasets', 'example.txt'))

  # load processed file to a database
  load_result = load_database_with_dataset(wpp_messages)
 ```
  ### Use case - Pandas
  If the dataset was loaded to a database with method __load_database_with_dataset()__, it can be accessed with pandas __read_sql()__ method. By default the table name is __'messages'__. To do so, first it is needed to import the database engine from the app package.

  ```python 
  import pandas as pd
  from app.main import engine
  
  messages = pd.read_sql('messages', engine)

  ```
