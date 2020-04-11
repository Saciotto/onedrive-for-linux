from .item import Item

class SyncEngine:
    def __init__(self, account):
        self.onedrive = account.onedrive
        self.folder = '~/onedrive'

    def apply_differences(self):
        self.default_drive_id = self.onedrive.get_defualt_drive()['id']
        self.root_id = self.onedrive.get_defualt_root()['id']
        self._apply_differences(self.default_drive_id, self.root_id)

    def _apply_differences(self, drive_id, file_id):
        changes = self.onedrive.view_changes_by_id(drive_id, file_id)
        for item in changes['value']:
            is_root = (file_id == item['id'])
            self._apply_difference(item, file_id, is_root)

    def _apply_difference(self, drive_item, drive_id, is_root):
        item = Item(drive_item)
        print(item)

    def scan_for_differences(self, path='.'):
        pass

    def upload_move_item(self, file_from, file_to):
        pass

    def delete_by_path(self, path):
        pass
