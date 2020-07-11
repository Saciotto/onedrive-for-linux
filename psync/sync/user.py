import os
from pathlib import Path

from psync.helpers.sqlite_table import SqliteTable

from psync.onedrive.account import OnedriveAccount
from psync.onedrive import accounts

class UsersTable(SqliteTable):
    def create_table_query(self):
        return """ 
            CREATE TABLE IF NOT EXISTS users (
                user_id         TEXT        PRIMARY KEY     NOT NULL,
                folder          TEXT                        NOT NULL,
                name            TEXT                        NOT NULL,
                username        TEXT                        NOT NULL
            );
        """

    def save(self, user):
        query = """
            INSERT OR REPLACE INTO users (user_id, folder, name, username) VALUES (?,?,?,?);
        """
        cur = self.conn.cursor()
        cur.execute(query, user)
        self.conn.commit()

    def load(self, user_id):
        query = """
            SELECT * FROM users WHERE user_id=?;
        """
        cur = self.conn.cursor()
        cur.execute(query, (user_id,))
        return cur.fetchone()

    def delete(self, user_id):
        query = """
            DELETE FROM users WHERE user_id=?;
        """
        cur = self.conn.cursor()
        cur.execute(query, (user_id,))
        self.conn.commit()

    def load_all(self):
        query = """
            SELECT * FROM users;
        """
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()


def get_users():
    with UsersTable() as table:
        users = []
        for account_db in table.load_all():
            users.append(account_db[0])
        return users

class User:

    def __init__(self, user_id, account, root_folder, name, username):
        self.__user_id = user_id
        self.__account = account
        self.__root_folder = root_folder
        self.__name = name
        self.__username = username

    @staticmethod
    def login(user_id, root_folder=None):
        if not root_folder:
            root_folder = Path.home() / 'psync' / 'OneDrive' / user_id
        account = OnedriveAccount.webbrowser_login(user_id)
        accounts.add(account)

        user_info = account.get_user_info()
        name = user_info['displayName']
        username = user_info['userPrincipalName']

        with UsersTable() as table:
            user_db = (user_id, str(root_folder), name, username)
            table.save(user_db)

        return User(user_id, account, root_folder, name, username)

    @staticmethod
    def load(user_id):
        with UsersTable() as table:
            user_db = table.load(user_id)
            if not user_db:
                raise ValueError(f'{user_id} account was not found.')
            user_id, root_folder, name, username = user_db

            account = accounts.load(user_id)
            return User(user_id, account, root_folder, name, username)

    @staticmethod
    def list_all():
        users = get_users()
        for onedrive_user in users:
            user = User.load(onedrive_user)
            print(user)

    def __str__(self):
        return f'{self.__user_id}: {self.__name} - {self.__username} - {self.__root_folder}'
