import pandas as pd
from database.process_database import ProcessDatabase

database = ProcessDatabase()

# Adquirindo os dados
data_process = database.list_all_data_process()

process = database.list_all_process()
_process = {}

# Indexização das linhas dos dados
for row in process:
  _process[row[0]] = row

columns = ['id', 'memory', 'cpu', 'process_id', 'date_created', 'name', 'process_date_created', 'process_date_end']

data = pd.DataFrame(columns=columns)

# Para cada dados de processos, uma nova linha do arquivo
for row in data_process:
  process_id = row[3]

  process_row = _process[process_id]

  data_row = [row[0], row[1], row[2], process_id, row[4], process_row[1], process_row[2], process_row[3]]

  data.loc[len(data.index)] = data_row

data.to_csv('data.csv')
