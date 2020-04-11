import json
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

from . import routes

ONEDRIVE_TIMEOUT = 5


def get_defualt_drive(access_token):
    url = routes.DRIVE_URL
    headers = {'Authorization': access_token}
    request = Request(url, headers=headers)
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def get_defualt_root(access_token):
    url = f'{routes.DRIVE_URL}/root'
    headers = headers = {'Authorization': access_token}
    request = Request(url, headers=headers)
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def view_changes_by_id(access_token, drive_id, file_id, url=None):
    if not url:
        url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/delta'
        url += routes.SELECT_CHANGES
    headers = {'Authorization': access_token}
    request = Request(url, headers=headers)
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def view_changes_by_path(access_token, path=None, url=None):
    if(not url):
        if not path or path == '.':
            url = f'{routes.DRIVE_URL}/root/delta'
        else:
            url = f'{routes.ITEM_BY_PATH_URL}/{path}:delta'
        url += routes.SELECT_CHANGES
    headers = {'Authorization': access_token}
    request = Request(url, headers=headers)
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def download_by_id(access_token, drive_id, file_id, filename):
    url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/content?AVOverride=1'
    with open(filename, 'wb+') as fp:
        headers = {'Authorization': access_token}
        request = Request(url, headers=headers)
        with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
            fp.write(response.read())


def simple_upload(access_token, local_path, parent_drive_id, parent_id, filename, e_tag=None):
    url = f'{routes.DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}:/{filename}:/content'
    headers = {'Authorization': access_token, "Content-Type": "application/octet-stream"}
    if (e_tag):
        headers['If-Match'] = e_tag
    with open(local_path, 'rb') as fp:
        data = fp.read()
        request = Request(url, headers=headers, data=data, method='PUT')
        with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
            return json.load(response)


def simple_upload_replace(access_token, local_path, drive_id, file_id, e_tag=None):
    url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}/content'
    headers = {'Authorization': access_token, "Content-Type": "application/octet-stream"}
    if (e_tag):
        headers['If-Match'] = e_tag
    with open(local_path, 'rb') as fp:
        data = fp.read()
        request = Request(url, headers=headers, data=data, method='PUT')
        with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
            return json.load(response)


def update_by_id(access_token, drive_id, file_id, data, e_tag=None):
    url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}'
    headers = {'Authorization': access_token, "Content-Type": "application/json"}
    if (e_tag):
        headers['If-Match'] = e_tag
    request = Request(url, headers=headers, data=data, method='PATCH')
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def delete_by_id(access_token, drive_id, file_id, e_tag=None):
    url = f'{routes.DRIVE_BY_ID_URL}/{drive_id}/items/{file_id}'
    headers = {'Authorization': access_token}
    if (e_tag):
        headers['If-Match'] = e_tag
    request = Request(url, headers=headers, method='DELETE')
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as _:
        pass


def create_by_id(access_token, parent_drive_id, parent_id, item):
    url = f'{routes.DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}/children'
    headers = {'Authorization': access_token, "Content-Type": "application/json"}
    request = Request(url, data=item.encode(), headers=headers, method='POST')
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def create_upload_session(access_token, parent_drive_id, parent_id, filename, e_tag=None):
    url = f'{routes.DRIVE_BY_ID_URL}/{parent_drive_id}/items/{parent_id}:/{filename}:/createUploadSession'
    headers = {'Authorization': access_token, "Content-Type": "application/json"}
    if (e_tag):
        headers['If-Match'] = e_tag
    request = Request(url, headers=headers, method='POST')
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def upload_fragment(upload_url, local_path, offset, content_size, filesize):
    content_range = f'bytes {offset}-{offset + content_size - 1}/{filesize}'
    headers = {'Content-range': content_range}
    with open(local_path, 'rb') as fp:
        fp.seek(offset)
        data = fp.read(content_size)
        request = Request(upload_url, headers=headers, data=data, method='PUT')
        with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
            return json.load(response)


def request_upload_status(upload_url):
    with urlopen(upload_url, timeout=ONEDRIVE_TIMEOUT) as response:
        return json.load(response)


def _acquire_token(body):
    now = datetime.now(tz=timezone.utc)
    request = Request(routes.TOKEN_URL, data=body.encode(), method='POST')
    with urlopen(request, timeout=ONEDRIVE_TIMEOUT) as response:
        data = json.load(response)
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        expire = data['expires_in']
        expire_date = now + timedelta(seconds=int(expire))
    return access_token, refresh_token, expire_date


def redeem_token(code):
    body = f'client_id={routes.CLIENT_ID}&code={code}&grant_type=authorization_code'
    return _acquire_token(body)


def renew_token(refresh_token):
    body = f'client_id={routes.CLIENT_ID}&refresh_token={refresh_token}&grant_type=refresh_token'
    return _acquire_token(body)
