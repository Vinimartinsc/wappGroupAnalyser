# Análise de mensagens de grupo do Whatsapp
Analisa, categoriza e armazena mensagens do whatsapp exportadas no formato texto. Uma vez armazenadas em um banco de dados podem ser acessadas por outros pacotes como pandas.

_Este documento também está disponível em [English](readme.md) e [Português do Brasil](readme.pt.md)_

## Estrutura do projeto
```
<raíz>
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
  Pasta padrão para receber arquivos com mensagens exportadas dos grupos. Nela existe um dataset para demonstração de nome _example.txt_.

### .db 
  Pasta padrão para arquivos de banco de dados de extensão .db comumente utilizado por banco de dados sqlite.

### app
  Pacote que contém o código para processar e manipular as mensagens.

### notebooks 
  Pasta padrão para notebooks IPython. Nela possui notebook para demonstração de nome _example.ipynb_.

### app.config.yaml
  Arquivo que contém configurações gerais do pacote como local padrão de pasta ou informações para conexão com banco de dados. 

### logging.config.yaml
  Arquivo contendo parâmetros para formatação de log.

### app/main.py
  O ponto de entrada principal do pacote app.

### app/ConfigService
  Service que provê ao app parâmetros carregados do arquivo app.config.yaml file.

### app/DatabaseSErvice
  Service para interação com banco de dados.

### app/WappMessageIngestService
  Serviço para processamento e manipulação de arquivos com mensagens de grupos de whatsapp (datasets).

## O objeto WhatsappMessagesDTO
  É um objeto que representa a mensagem de um grupo do whatsapp. Os parâmetros deste objeto são privados, logo a interação com esse objeto deve ser feita pelos métodos acessores. A seguir na tabela, tem-se a lista dos parâmetros.

  | Param | Tipo | Descrição | Acessor |
  | ---- | ----- | --- | --- |
  | __at_datetime | datetime | Representa a data e hora que uma mensagem foi enviada. | get_datetime() |
  | __author | str | Representa o autor da mensagem enviada. | get_author() |
  | __content | List[str] | O conteúdo da mensagem em si. | get_content() |
  | __raw | str | A mensagem no seu formato original, como está no dataset. | get_raw() |
  | __type | str | A categoria de uma mensagem. Ex. COMMON_MESSAGE.| get_type() |

## As categorias de uma mensagem (Tipo)
  Uma mensagem pode ser categorizada de acordo com seu formato. A tabela a seguir apresenta o significado de cada categoria.

  | Categoria | Descrição |
  | --- | --- |
  | COMMON_CONVERSATION | Uma conversa comum entre membros de um grupo |
  | MEMBER_LEFT_NOTIFICATION | Notificação do sistema da evasão de membro do grupo | 
  | MEMBER_ADDED_NOTIFICATION | Uma notificação de sistema de ingresso de membro ao grupo. | 
  | MEMBER_ID_MAPPING_NOTIFICATION | A notificação do sistema que um membro mudou de número. | 
  | OTHER | Outro tipo de mensagem que não satisfaz as categorias anteriores. |


## Modo de Uso

  Primeiro é necessário abrir e ler o dataset em modo de texto. Isso pode ser feito com uso do método __read_dataset_file()__. Isso processará o dataset e retornará uma lista de objetos, onde cada objeto é do tipo __WhatsappMessagesDTO__ e contém dados da mensagem. A lista de mensagens pode então ser armazenada no banco de dados com o método __load_database_with_dataset()__. Ele irá gerar por padrão um novo arquivo .db, que é um banco de dados sqlite na pasta .db. Veja o exemplo a seguir.
 
 ```python
  
  import os

  # Se executar de um notebook em uma pasta que não a raíz do projeto   descomente a próxima linha
  # import sys; sys.path.append("../")

  from app.main import read_dataset_file, load_database_with_dataset


  # Lê arquivo exportado pelo grupo de whatsapp
  # o caminho deve apontar para o diretório ou arquivo contendo o dataset
  wpp_messages = read_dataset_file(os.path.join('.datasets', 'example.txt'))

  # armazena as mensagens do dataset no banco de dados
  load_result = load_database_with_dataset(wpp_messages)
 ```
  ### Caso de uso - Pandas
  Se o dataset foi carregado com o método __load_database_with_dataset()__, então pode ser acessado com pacote pandas com método __read_sql()__. Por padrão, a tabela tem o nome __'messages'__.

  ```python 
  import pandas as pd
  from app.main import engine
  
  # Carrega na variável messages todas as mensagens como dataframe
  messages = pd.read_sql('messages', engine)

  ```