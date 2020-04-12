from datetime import datetime

from onedrive.helpers.sqlite_table import SqliteTable
from onedrive.helpers.observer import Observer
from onedrive.models.account import OnedriveAccount


class OnedriveAccountTable(SqliteTable):
    def create_table_querry(self):
        return """ 
            CREATE TABLE IF NOT EXISTS accounts (
                name            TEXT        PRIMARY KEY     NOT NULL,
                access_token    TEXT                        NOT NULL,
                refresh_token   TEXT                        NOT NULL,
                expire_date     DATETIME                    NOT NULL
            );
        """

    def save(self, account):
        querry = """
            INSERT OR REPLACE INTO accounts (name, access_token, refresh_token, expire_date) VALUES (?,?,?,?);
        """
        cur = self.conn.cursor()
        cur.execute(querry, account)
        self.conn.commit()

    def load(self, name):
        querry = """
            SELECT * FROM accounts WHERE name=?;
        """
        cur = self.conn.cursor()
        cur.execute(querry, (name,))
        return cur.fetchone()


class AccountObserver(Observer):
    def update(self, account):
        expire_date = account.expire_date.isoformat(' ')
        data = (account.account_id, account.access_token, account.refresh_token, expire_date)
        with OnedriveAccountTable() as table:
            table.save(data)


def observe_account(account, update_now=True):
    observer = AccountObserver()
    account.add_observer(observer)
    if update_now:
        observer.update(account)


def load_account(name):
    with OnedriveAccountTable() as table:
        account_db = table.load(name)
        if not account_db:
            raise ValueError(f'{name} account was not found.')
        account_id, access_token, refresh_token, expire_date = account_db
        expire_date = datetime.fromisoformat(expire_date)
        account = OnedriveAccount(account_id, access_token, refresh_token, expire_date)
        observe_account(account, False)
        return account
