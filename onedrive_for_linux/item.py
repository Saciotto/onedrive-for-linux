from datetime import datetime, timezone

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
            self.type = 'file'
        elif 'folder' in drive_item:
            self.type = 'folder'
        elif 'remote' in drive_item:
            self.type = 'remote'
        else:
            self.type = 'unknown'

        if not 'root' in drive_item and 'parentReference' in drive_item:
            self.drive_id = drive_item['parentReference']['driveId']

        if 'file' in drive_item and 'hashes' in drive_item['file']:
            hashes = drive_item['file']['hashes']
            self.crc32 = hashes.get('crc32Hash', None)
            self.sha1 = hashes.get('sha1Hash', None)
            self.quick_xor = hashes.get('quickXorHash', None)

        if 'remote' in drive_item:
            self.remote_drive_id = drive_item['remoteItem']['parentReference']['driveId']
            self.remote_id = drive_item['remoteItem']['id']
