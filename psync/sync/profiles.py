from psync.helpers.sqlite_table import SqliteTable
from psync.onedrive import accounts
from psync.sync import profile

class ProfilesTable(SqliteTable):
    def create_table_query(self):
        return """ 
            CREATE TABLE IF NOT EXISTS profiles (
                id              TEXT        PRIMARY KEY     NOT NULL,
                folder          TEXT                        NOT NULL,
                name            TEXT                        NOT NULL,
                username        TEXT                        NOT NULL
            );
        """

    def save(self, profile_db):
        query = """
            INSERT OR REPLACE INTO profiles (id, folder, name, username) VALUES (?,?,?,?);
        """
        self.cur.execute(query, profile_db)
        self.conn.commit()

    def load(self, profile_id):
        query = """
            SELECT * FROM profiles WHERE id=?;
        """
        cur = self.conn.cursor()
        cur.execute(query, (profile_id,))
        return cur.fetchone()

    def delete(self, profile_id):
        query = """
            DELETE FROM profiles WHERE id=?;
        """
        cur = self.conn.cursor()
        cur.execute(query, (profile_id,))
        self.conn.commit()

    def select_all(self):
        query = """
            SELECT * FROM profiles;
        """
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()


def get_all_ids():
    with ProfilesTable() as table:
        ids = []
        for profile_db in table.select_all():
            ids.append(profile_db[0])
        return ids


def save(profile):
    profile_db = (profile.profile_id, str(profile.root_folder), profile.name, profile.username)
    with ProfilesTable() as table:
        table.save(profile_db)


def remove(profile_id):
    with ProfilesTable() as table:
        table.delete(profile_id)
    

def load(profile_id):
    with ProfilesTable() as table:
        profile_db = table.load(profile_id)
        if not profile_db:
            raise ValueError(f'{profile_id} profile was not found.')
        profile_id, root_folder, name, username = profile_db
        account = accounts.load(profile_id)
        return profile.Profile(profile_id, account, root_folder, name, username)

def print_all():
    ids = get_all_ids()
    for profile_id in ids:
        profile = load(profile_id)
        print(profile)
