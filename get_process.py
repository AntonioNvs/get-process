import psutil

class GetProcess:
  def __init__(self) -> None:

    self.attrs_info: list(str) = ['name', 'cpu_percent']

  # Lista dos processos ativos, com as informações desejadas
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

  # Informações específicas gerais do computador (CPU e RAM)
  def get_info_pc(self):
    return psutil.cpu_percent(), psutil.virtual_memory().percent