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

    def save_account(self, account):
        account_id = account[0]
        if self._contains(account_id):
            self._update_account(account)
        else:
            self._insert_account(account)

    def load_account(self, id):
        querry = """
            SELECT * FROM accounts WHERE id=?;
        """
        cur = self.conn.cursor()
        cur.execute(querry, (id,))
        return cur.fetchone()

    def load_all_accounts(self):
        querry = """
            SELECT * FROM accounts;
        """
        cur = self.conn.cursor()
        cur.execute(querry)
        return cur.fetchall()

    def _create_account_table(self):
        querry = """ 
            CREATE TABLE IF NOT EXISTS accounts (
                id              TEXT        PRIMARY KEY     NOT NULL,
                name            TEXT                        NOT NULL,
                access_token    TEXT                        NOT NULL,
                refresh_token   TEXT                        NOT NULL,
                expire_date     DATETIME                    NOT NULL
            );
        """
        cur = self.conn.cursor()
        cur.execute(querry)

    def _contains(self, id):
        account = self.load_account(id)
        if (account):
            return True
        return False

    def _insert_account(self, account):
        querry = """
            INSERT INTO accounts (id, name, access_token, refresh_token, expire_date) VALUES (?,?,?,?,?);
        """
        cur = self.conn.cursor()
        cur.execute(querry, account)
        self.conn.commit()

    def _update_account(self, account):
        querry = """
            UPDATE accounts SET name=?, access_token=?, refresh_token=?, expire_date=? WHERE id=?;
        """
        cur = self.conn.cursor()
        cur.execute(querry, (account[1], account[2], account[3], account[4], account[0]))
        self.conn.commit()