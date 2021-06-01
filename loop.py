from analysis_process import AnalysisProcess
from os import system
from database.process_database import ProcessDatabase
from threading import Thread
from time import sleep
from datetime import timedelta
import msvcrt as m

class Loop(AnalysisProcess):
  def __init__(self, database: ProcessDatabase) -> None:
    super().__init__(database)

    system('cls')
    print('Começando o looping..')

    self.process_continuos = True
    self.seconds = 0

    self.init()

  def init(self) -> None:
    # Iniciando Thread de análise de processes
    self._th_process = Thread(target=self.loop_process)
    self._th_process.start()
    
    self._th_time = Thread(target=self.print_the_time)
    self._th_time.start()

    # Espera qualquer tecla ser digitada e termina o programa
    m.getch()
    self.process_continuos = False

  def loop_process(self) -> None:
    while self.process_continuos:
      self.fill_info_about_process()

  def print_the_time(self) -> None: 
    while self.process_continuos:
      system('cls')
      print(timedelta(seconds=self.seconds))
      
      sleep(1)
      self.seconds += 1


    



if __name__ == "__main__":
  Loop(ProcessDatabase())