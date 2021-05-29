import sqlite3

class Database:
  def __init__(self):
    self.name_database = 'database/database.db'

    self.create_init_tables()
    self.close_database()

  def create_init_tables(self) -> None:
    self.open_database_and_init_cursor()
    
    self.cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS process (
          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          name varchar(255) NOT NULL,
          date_created DATETIME NOT NULL,
          date_end DATETIME
        );
      """)

    self.cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS data_process (
          id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
          memory varchar(255) NOT NULL,
          cpu varchar(10) NOT NULL,
          process_id INTEGER NOT NULL,
          date_created DATETIME NOT NULL,
          FOREIGN KEY(process_id) REFERENCES process(id)
        );
      """)

  def open_database_and_init_cursor(self):
    self.conn: sqlite3.Connection = sqlite3.connect(self.name_database)
    self.cursor = self.conn.cursor()

  def close_database(self):
    self.cursor.close()
    self.conn.close()

  def execute_command(self, command: str):
    self.open_database_and_init_cursor()

    self.cursor.execute(command)

    self.conn.commit()

    self.close_database()

  def insert_in_table(self, command: str) -> int:
    self.open_database_and_init_cursor()

    self.cursor.execute(command)

    self.conn.commit()

    last_id = self.cursor.lastrowid

    self.close_database()

    return last_id

  def select_table(self, command) -> list:
    self.open_database_and_init_cursor()

    self.cursor.execute(command)

    rows = []
    for row in self.cursor.fetchall():
      rows.append(row)

    self.close_database()

    return rows