
class ItemDatabase:

    def __init__(self, filename):
        pass

    def insert(self, item):
        pass

    def update(self, item):
        pass

    def upsert(self, item):
        pass

    def select_children(self, drive_id, id):
        pass

    def select_by_id(self, drive_id, id):
        pass

    def select_by_path(self, path, root_drive_id):
        pass

    def select_by_path_no_remote(self, path, root_drive_id):
        pass

    def delete_by_id(self, drive_id, id):
        pass

    def compute_path(self, drive_id, id):
        pass

    def select_remote_items(self):
        pass

    def get_delta_link(self, drive_id, id):
        pass

    def set_delta_link(self, drive_id, id, delta_link):
        pass
