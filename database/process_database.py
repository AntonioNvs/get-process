from database.main import Database
from datetime import date, datetime

class ProcessDatabase(Database):
  def __init__(self) -> None:
      super().__init__()

  def create_process(self, name_process) -> int:
    return self.insert_in_table(
      f"""
        INSERT INTO process (name, date_created) VALUES ('{name_process}', '{datetime.now()}');
      """
    )

  def create_data_updated_process(self, memory, cpu, process_id) -> int:
    return self.insert_in_table(
      f"""
        INSERT INTO data_process (memory, cpu, process_id, date_created) VALUES
        ('{memory}', '{cpu}', '{process_id}', '{datetime.now()}');
      """
    )

  def end_process(self, process_id) -> None:
    self.execute_command(
      f"""
        UPDATE process
        SET date_end = '{datetime.now()}'
        WHERE id = '{process_id}'
      """
    )
