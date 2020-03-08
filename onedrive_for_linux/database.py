import os
import sqlite3
from pathlib import Path

class Database:

    def __enter__(self):
        db_path = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share' / 'onedrive_for_linux'))
        db_path.mkdir(mode=0o755, parents=True, exist_ok=True) 
        db_file = str(db_path / 'accounts.db')
        self.conn = sqlite3.connect(db_file)
        self._create_account_table()
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def save_account(self, name, account):
        querry = """
            INSERT INTO accounts (name, access_token, refresh_token, expire_date) VALUES (?,?,?,?);
        """
        cur = self.conn.cursor()
        access_token, refresh_token, expire_date = account
        cur.execute(querry, (name, access_token, refresh_token, expire_date))
        self.conn.commit()

    def load_account(self, name):
        querry = """
            SELECT * FROM accounts WHERE name=?;
        """
        cur = self.conn.cursor()
        cur.execute(querry, (name,))
        return cur.fetchone()

    def _create_account_table(self):
        querry = """ 
            CREATE TABLE IF NOT EXISTS accounts (
                id              integer PRIMARY KEY NOT NULL,
                name            text                NOT NULL,
                access_token    text                NOT NULL,
                refresh_token   text                NOT NULL,
                expire_date     text                NOT NULL
            );
        """
        cur = self.conn.cursor()
        cur.execute(querry)

if __name__ == "__main__":
    with Database() as db:
        account = ('at', 'rf', 'date')
        db.save_account('Teste', ('a', 'b', 'c'))
        db.load_account('Teste')