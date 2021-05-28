import psutil
from datetime import date, datetime

class GetProcess:
  def __init__(self) -> None:

    self.attrs_info: list(str) = ['name', 'cpu_percent']


  def get_info_process_active(self):
    list_info_about_process = list()

    for process in psutil.process_iter():
      try:
        process_info = process.as_dict(attrs=self.attrs_info)

        process_info['memory'] = process.memory_info().vms / (1024**2)

        list_info_about_process.append(process_info)
      except:
        pass

    return list_info_about_process


class ManipulationProcess(GetProcess):
  def __init__(self) -> None:
      super().__init__()

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

        # Se não tiver o atributo de data de início, crie-o
        if 'date_init' is not self.process[name]:
          self.process[name]['date_init'] = datetime.now()

    print(self.process)

if __name__ == '__main__':
  class_process = ManipulationProcess()
  class_process.fill_info_about_process()
  