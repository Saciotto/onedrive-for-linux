
# Microsoft Authorization
AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# Microsoft Graph API
DRIVE_URL = 'https://graph.microsoft.com/v1.0/me/drive'
ITEM_BY_ID_URL = 'https://graph.microsoft.com/v1.0/me/drive/items/'
ITEM_BY_PATH_URL = 'https://graph.microsoft.com/v1.0/me/drive/root:/'
DRIVE_BY_ID_URL = 'https://graph.microsoft.com/v1.0/drives/'

# Applicaton
REDIRECT_URL = 'http://localhost:8000'

# Request information
CLIENT_ID = 'c22bd74f-da4c-460d-af0a-f97aa232a908'
SCOPES = 'Files.ReadWrite%20Files.ReadWrite.all%20Sites.ReadWrite.All%20offline_access'
SELECT_CHANGES = '?select=id,name,eTag,cTag,deleted,file,folder,root,fileSystemInfo,remoteItem,parentReference'
