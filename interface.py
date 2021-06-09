from analysis_process import AnalysisProcess
from database.process_database import ProcessDatabase

from threading import Thread
from datetime import datetime, date, timedelta
import os, sys
import msvcrt as m
import time

class Interface(AnalysisProcess):
  def __init__(self, database: ProcessDatabase):
    super().__init__(database)
    self.is_exit = False

    time.clock() # Início do tempo

    # Instanceando a thread do loop de análise de processos
    self._th_process = Thread(target=self.loop_process)
    self._th_process.start()
    
    # Instanceando a thread responsável em escrever no terminal
    self._th_print_in_screen =Thread(target=self.print_in_screen) 
    self._th_print_in_screen.start()
    
    # Função de 'exit' do programa
    self.how_can_exit()

  def print_in_screen(self):
    while not self.is_exit:
      # Impressões básicas
      os.system('cls')
      print('Aperte "q" para finalizar o programa!')
      print()
      print(self.seconds_to_time())
      print(f'Dados já capturados: {self.files_updated}')
      print()
      print('TOTAL:')
      print()

      # Cálculo da barra de impressão dos dados de cpu e memória
      cpu, memory = self.get_info_pc()
      number_cpu = int(cpu / 5)
      number_memory = int(memory / 5)

      # Cálculo dos caracteres das barras
      bar_cpu = "#".join(['' for _ in range(number_cpu)]) + "-".join(['' for _ in range(20 - number_cpu)])
      bar_memory = "#".join(['' for _ in range(number_memory)]) + "-".join(['' for _ in range(20 - number_memory)])

      print(f'{bar_cpu}  =  {cpu}% CPU')
      print(f'{bar_memory}  =  {memory}% RAM')

      # Lista de processos ativos
      print('\n\n')

      task_actives = []

      for task in self.process:
        if 'id' in self.process[task].keys():
          task_actives.append(task)

      print(f'TAREFAS ATIVAS: {len(task_actives)}\n')

      for task in task_actives:
        now = datetime.now()
        init = self.process[task]['date_init']
        
        print(f'{task} - {self.subtration_beetween_two_datetimes(init, now)}')

      time.sleep(1)

  # Subtraindo duas datas a partir do timedelta da lib datetime
  def subtration_beetween_two_datetimes(self, start: datetime, stop: datetime):
    start_delta = timedelta(hours=start.hour, minutes=start.minute, seconds=start.second)
    stop_delta = timedelta(hours=stop.hour, minutes=stop.minute, seconds=stop.second)

    return stop_delta - start_delta

  # Transformando segundos em tempo de HH/MM/SS
  def seconds_to_time(self, default_time = None) -> str:
    seconds = int(time.clock())

    if default_time is not None:
      seconds = default_time

    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60

    return f'{hours if hours >= 10 else f"0{hours}"}:{minutes if minutes >= 10 else f"0{minutes}"}:{seconds if seconds >= 10 else f"0{seconds}"}'

  # Thread do processo de looping
  def loop_process(self):
    while not self.is_exit:
      self.fill_info_about_process()

  def how_can_exit(self):
    while True:
      # Se um botão for pressionado, a função retorna um valor
      caracter = m.getch().decode('utf-8')

      if caracter == 'e':
        # Abrindo o arquivo de edição
        os.system(os.path.abspath(os.getcwd()) + '\\' + self.name_file_with_name_process)

      elif caracter == 'q':
        break
    
    # Encerrando o processo do programa
    self.is_exit = True
    self.end_process()
    time.sleep(1)

    sys.exit()


if __name__ == '__main__':
  Interface(ProcessDatabase())