import os
import sqlite3
from pathlib import Path
from abc import ABC, abstractmethod


class SqliteTable(ABC):

    def __enter__(self):
        db_path = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share' / 'onedrive_for_linux'))
        db_path.mkdir(mode=0o755, parents=True, exist_ok=True)
        db_file = str(db_path / 'onedrive.db')
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()
        return self

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        query = self.create_table_query()
        self.cur.execute(query)

    @abstractmethod
    def create_table_query(self):
        pass
