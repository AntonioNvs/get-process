import psutil

class GetProcess:
  def __init__(self) -> None:

    self.attrs_info: list(str) = ['name', 'cpu_percent', 'memory_info']


  def get_info_process_active(self) -> list(dict):
    list_info_about_process = list()

    for process in psutil.process_iter():
      try:
        process_info = process.as_dict(attrs=self.attrs_info)

        process_info['memory'] = process.memory_info().vms / (1024**2)

        list_info_about_process.append(process_info)
      except:
        pass

    return list_info_about_process


if __name__ == '__main__':
  class_process = GetProcess()
  print(class_process.get_info_process_active())

  