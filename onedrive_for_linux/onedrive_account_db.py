from .sqlite_table import SqliteTable


class OnedriveAccountDB(SqliteTable):

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
        name = account[0]
        if self._contains(name):
            self._update_account(account)
        else:
            self._insert_account(account)

    def load(self, name):
        querry = """
            SELECT * FROM accounts WHERE name=?;
        """
        cur = self.conn.cursor()
        cur.execute(querry, (name,))
        return cur.fetchone()

    def load_all(self):
        querry = """
            SELECT * FROM accounts;
        """
        cur = self.conn.cursor()
        cur.execute(querry)
        return cur.fetchall()

    def _contains(self, id):
        account = self.load(id)
        if (account):
            return True
        return False

    def _insert_account(self, account):
        querry = """
            INSERT INTO accounts (name, access_token, refresh_token, expire_date) VALUES (?,?,?,?);
        """
        cur = self.conn.cursor()
        cur.execute(querry, account)
        self.conn.commit()

    def _update_account(self, account):
        querry = """
            UPDATE accounts SET access_token=?, refresh_token=?, expire_date=? WHERE name=?;
        """
        cur = self.conn.cursor()
        cur.execute(querry, (account[1], account[2], account[3], account[0]))
        self.conn.commit()
