from datetime import datetime, timezone
from enum import Enum, auto


class ItemType(Enum):
    FILE = auto()
    FOLDER = auto()
    REMOTE = auto()
    UNKNOWN = auto()


class Item:
    def __init__(self, drive_item):
        self.id = drive_item['id']
        self.name = drive_item.get('name', None)
        self.e_tag = drive_item.get('eTag', None)
        self.c_tag = drive_item.get('cTag', None)

        if 'fileSystemInfo' in drive_item and 'lastModifiedDateTime' in drive_item['fileSystemInfo']:
            zulu_time = drive_item['fileSystemInfo']['lastModifiedDateTime']
            self.modified = datetime.strptime(zulu_time, "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            self.modified = datetime.now(tz=timezone.utc)

        if 'file' in drive_item:
            self.type = ItemType.FILE
        elif 'folder' in drive_item:
            self.type = ItemType.FOLDER
        elif 'remote' in drive_item:
            self.type = ItemType.REMOTE
        else:
            self.type = ItemType.UNKNOWN

        if not 'root' in drive_item and 'parentReference' in drive_item:
            self.drive_id = drive_item['parentReference']['driveId']
        else:
            self.drive_id = None

        if 'file' in drive_item and 'hashes' in drive_item['file']:
            hashes = drive_item['file']['hashes']
            self.crc32 = hashes.get('crc32Hash', None)
            self.sha1 = hashes.get('sha1Hash', None)
            self.quick_xor = hashes.get('quickXorHash', None)
        else:
            self.crc32 = self.sha1 = self.quick_xor = None

        if 'remote' in drive_item:
            self.remote_drive_id = drive_item['remoteItem']['parentReference']['driveId']
            self.remote_id = drive_item['remoteItem']['id']
        else:
            self.remote_drive_id = self.remote_id = None

    def __str__(self):
        return f'Item({self.type}, {self.name})'
