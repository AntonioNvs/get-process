from get_process import GetProcess
from datetime import datetime
from database.process_database import ProcessDatabase
from time import sleep

class AnalysisProcess(GetProcess):
  def __init__(self, database: ProcessDatabase) -> None:
      super().__init__()

      self.time_for_update = 90 # Tempo de atualziação em segundos
      self.database = database
      self.name_file_with_name_process = 'process_names.txt'
      self.name_all_task_pc = 'all_info_pc'
      self.files_updated = 0

      # Lista dos nomes dos processos desejados
      self.process_names: list(str) = []
      self.set_process_names()

      # Dicionário das tarefas desejadas
      self.process: dict = self.make_the_dict_of_process()

      # Criação do processo de todo o computador de forma separada
      self.process[self.name_all_task_pc] = self.create_an_empty_dict()
      self.process[self.name_all_task_pc]['id'] = self.database.create_process(self.name_all_task_pc)

      # Variável de controle dos processos
      self.controll_process: list(int) = [{ 'before': False, 'after': False } for _ in range(len(self.process_names))]

  # Selecionando as tarefas desejadas pelo arquivo de texto
  def set_process_names(self):
    with open(self.name_file_with_name_process, 'r') as file:
      self.process_names = [name.strip() for name in file.read().split('\n')]

  # Preenchendo as informações de todo o pc
  def info_dict_all_pc(self):
    name = self.name_all_task_pc
    date_now = datetime.now()

    cpu, memory = self.get_info_pc()

    self.process[name]['cpu_percent'] = cpu
    self.process[name]['memory'] = memory

    # Atualizar os dados no banco, dependendo do tempo
    if self.datetime_to_int(date_now) - self.datetime_to_int(self.process[name]['date_updated']) >= self.time_for_update:
      self.execute_update(name)

      self.process[name]['date_updated'] = date_now

      self.files_updated += 1

  # Criando um dicionário em todos os processos
  def make_the_dict_of_process(self):
    process = dict()

    for name in self.process_names:
      process[name] = dict()

    return process

  # Dicionário padrão de uma tarefa após ser iniciada
  def create_an_empty_dict(self) -> dict:
    date_now = datetime.now()

    return {
        'date_init': date_now,
        'date_updated': date_now
      }

  # Função principal da classe, a qual vai preencher todas as variáveis cadastradas
  def fill_info_about_process(self) -> None:
    list_info_process = self.get_info_process_active() # Lista dos processos ativos

    for info_process in list_info_process:
      name = info_process['name']

      # Caso o processo desejado esteja na lista dos processos ativos
      if name in self.process_names:

        # Caso o processo esteja vazio, crie um novo com os parâmetros
        if self.process[name] == {}:
          self.process[name] = self.create_an_empty_dict()

        # Salvando as informações do processo
        for attribute, value in info_process.items():
          if attribute is not 'name':
            self.process[name][attribute] = value

        date_now = datetime.now()

        # Atualizar os dados no banco, dependendo do tempo
        if self.datetime_to_int(date_now) - self.datetime_to_int(self.process[name]['date_updated']) >= self.time_for_update:
          self.execute_update(name)

          self.process[name]['date_updated'] = date_now

          self.files_updated += 1

        # Criando o processo na base de dados caso ele não tenha sido criado ainda
        if 'id' not in self.process[name]:
          self.process[name]['id'] = self.database.create_process(name)

    # Lista do nome de todos os processos ativos
    name_process_active = [i['name'] for i in list_info_process]

    # Controle dos processos, para saber se um ativo foi encerrado
    for i, process in enumerate(self.process_names):
      self.controll_process[i]['before'] = self.controll_process[i]['after']

      self.controll_process[i]['after'] = process in name_process_active

    for i, activations in enumerate(self.controll_process):
      before, after = [i[1] for i in activations.items()]

      # Caso o processo tenha sido encerrado..
      if before and not after:
        # Atualizando o banco colocando a data de encerramento
        name = self.process_names[i]
        self.database.end_process(self.process[name]['id'])
        self.process[name] = {}

    self.info_dict_all_pc()

  # Função para encerrar os processos caso o programa seja interrompido
  def end_process(self):
    for name in self.process:
      try:
        self.database.end_process(self.process[name]['id'])
      except KeyError:
        pass

  # Transformando a classe datetime em um inteiro
  def datetime_to_int(self, date: datetime) -> int:
    return date.day * 86400 + date.hour * 3600 * date.minute * 60 + date.second

  # Após determinado tempo, salve no banco os dados atuais do processo
  def execute_update(self, name_process):
    id_process = self.process[name_process]['id']
    memory = self.process[name_process]['memory']
    cpu = self.process[name_process]['cpu_percent']

    self.database.create_data_updated_process(memory, cpu, id_process)