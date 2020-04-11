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
        self.create_table()
        return self

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        querry = self.create_table_querry()
        cur = self.conn.cursor()
        cur.execute(querry)

    @abstractmethod
    def create_table_querry(self):
        pass
