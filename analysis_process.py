from get_process import GetProcess
from datetime import datetime
from database.process_database import ProcessDatabase
from time import sleep

class AnalysisProcess(GetProcess):
  def __init__(self, database: ProcessDatabase) -> None:
      super().__init__()

      self.time_for_update = 10 # Tempo em segundos
      self.database = database

      # Lista dos nomes dos processos desejados
      self.process_names: list(str) = []
      self.set_process_names()

      self.process: dict = self.make_the_dict_of_process()

      # Variável de controle dos processos
      self.controll_process: list(int) = [{ 'before': False, 'after': False } for _ in range(len(self.process_names))]


  def set_process_names(self):
    with open('process_names.txt', 'r') as file:
      self.process_names = [name.strip() for name in file.read().split('\n')]

  
  def make_the_dict_of_process(self):
    process = dict()


    for name in self.process_names:
      process[name] = self.create_an_empty_dict()

    return process

  def create_an_empty_dict(self) -> dict:
    date_now = datetime.now()

    return {
        'date_init': date_now,
        'date_updated': date_now
      }

  def fill_info_about_process(self) -> None:
    list_info_process = self.get_info_process_active()

    for info_process in list_info_process:
      name = info_process['name']

      if name in self.process_names:
        # Caso o processo esteja vazio, crie um novo com os parâmetros
        if self.process[name] == {}:
          self.process = self.create_an_empty_dict()

        # Salvando as informações do processo
        for attribute, value in info_process.items():
          if attribute is not 'name':
            self.process[name][attribute] = value

        date_now = datetime.now()

        # Atualizar os dados no banco, dependendo do tempo
        if self.datetime_to_int(date_now) - self.datetime_to_int(self.process[name]['date_updated']) >= self.time_for_update:
          self.execute_update(name)

          self.process[name]['date_updated'] = date_now

        # Criando o processo na base de dados caso ele não tenha sido criado ainda
        if 'id' not in self.process[name]:
          self.process[name]['id'] = self.database.create_process(name)

    name_process_active = [i['name'] for i in list_info_process]

    # Controle dos processos, para saber se um ativo foi encerrado
    for i, process in enumerate(self.process_names):
      self.controll_process[i]['before'] = self.controll_process[i]['after']

      self.controll_process[i]['after'] = process in name_process_active

    for i, activations in enumerate(self.controll_process):
      # Caso o processo tenha sido encerrado..      
      before, after = [i[1] for i in activations.items()]

      if before and not after:
        # Atualizando o banco colocando a data de encerramento
        name = self.process_names[i]
        self.database.end_process(self.process[name]['id'])
        self.process[name] = {}

  def datetime_to_int(self, date: datetime) -> int:
    return int(date.strftime('%Y%m%d%H%M%S'))

  # Após determinado tempo, salve no banco os dados atuais do processo
  def execute_update(self, name_process):
    id_process = self.process[name_process]['id']
    memory = self.process[name_process]['memory']
    cpu = self.process[name_process]['cpu_percent']

    self.database.create_data_updated_process(memory, cpu, id_process)


if __name__ == '__main__':
  class_process = AnalysisProcess(ProcessDatabase())

  while True:
    class_process.fill_info_about_process()
    sleep(1)