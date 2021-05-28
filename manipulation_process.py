from time import time
from get_process import GetProcess
from datetime import date, datetime, timedelta

class ManipulationProcess(GetProcess):
  def __init__(self) -> None:
      super().__init__()

      self.time_for_update = 60 # Tempo em segundos

      # Lista dos nomes dos processos desejados
      self.process_names: list(str) = []
      self.set_process_names()

      self.process: dict = self.make_the_dict_of_process() 


  def set_process_names(self):
    with open('process_names.txt', 'r') as file:
      self.process_names = [name.strip() for name in file.read().split('\n')]


  def make_the_dict_of_process(self):
    process = dict()

    for name in self.process_names:
      process[name] = {}

    return process

  
  def fill_info_about_process(self):
    for info_process in self.get_info_process_active():
      name = info_process['name']
      if name in self.process_names:
        for att, value in info_process.items():
          if att is not 'name':
            self.process[name][att] = value

        date_now = datetime.now()

        # Se não tiver o atributo de data de início, crie-o
        if 'date_init' is not self.process[name] and 'date_att' is not self.process[name]:
          self.process[name]['date_init'] = date_now
          self.process[name]['date_att'] = date_now

        # Atualizar os dados no banco, dependendo do tempo
        if self.datetime_to_int(date_now) - self.datetime_to_int(self.process[name]['date_att']) >= self.time_for_update:
          self.execute_att()

          self.process[name]['date_att'] = date_now


    print(self.process)

  def datetime_to_int(self, date: datetime) -> int:
    return int(date.strftime('%Y%m%d%H%M%S'))

  def execute_att(self):
    pass

if __name__ == '__main__':

  class_process = ManipulationProcess()
  class_process.fill_info_about_process()
