from datetime import datetime

from psync.helpers.sqlite_table import SqliteTable
from psync.helpers.observer import Observer
from psync.onedrive.account import OnedriveAccount


class OnedriveAccountTable(SqliteTable):
    def create_table_query(self):
        return """ 
            CREATE TABLE IF NOT EXISTS onedrive_accounts (
                name            TEXT        PRIMARY KEY     NOT NULL,
                access_token    TEXT                        NOT NULL,
                refresh_token   TEXT                        NOT NULL,
                expire_date     DATETIME                    NOT NULL
            );
        """

    def save(self, account):
        query = """
            INSERT OR REPLACE INTO onedrive_accounts (name, access_token, refresh_token, expire_date) VALUES (?,?,?,?);
        """
        cur = self.conn.cursor()
        cur.execute(query, account)
        self.conn.commit()

    def load(self, name):
        query = """
            SELECT * FROM onedrive_accounts WHERE name=?;
        """
        cur = self.conn.cursor()
        cur.execute(query, (name,))
        return cur.fetchone()

    def delete(self, name):
        query = """
            DELETE FROM onedrive_accounts WHERE name=?;
        """
        cur = self.conn.cursor()
        cur.execute(query, (name,))
        self.conn.commit()


def save(account):
    expire_date = account.expire_date.isoformat(' ')
    account_db = (account.account_id, account.access_token, account.refresh_token, expire_date)
    with OnedriveAccountTable() as table:
        table.save(account_db)

def remove(account_id):
    with OnedriveAccountTable() as table:
        table.delete(account_id)


def load(account_id):
    with OnedriveAccountTable() as table:
        account_db = table.load(account_id)
        if not account_db:
            raise ValueError(f'{account_id} account was not found.')
        account_id, access_token, refresh_token, expire_date = account_db
        expire_date = datetime.fromisoformat(expire_date)
        account = OnedriveAccount(account_id, access_token, refresh_token, expire_date)
        return account
