import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer


WMT_CLIENT_ID = '5a548c01-29fc-4d89-9a40-475021e774a6'
WMT_CLIENT_SECRET = 'hbIMBWE42_moqdgNH635?%;'


redirect_uri = 'http://localhost:8083/'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
api_base_url='https://api.onedrive.com/v1.0/'

ONEDRIVEDB_WMT_DB_PATH = 'Documents/wmtdb.csv'

# Authentication:
client = onedrivesdk.get_default_client(client_id=WMT_CLIENT_ID, scopes=scopes)
auth_url = client.auth_provider.get_auth_url(redirect_uri)
# this will block until we have the auth code :
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
client.auth_provider.authenticate(code, redirect_uri, WMT_CLIENT_SECRET)

# check if DB exist:
local_file_path = ''


#download it:

root_folder = client.item(drive='me', path='ddddddd').download('./path_to_download_to.txt')
# id_of_file = root_folder[0].id

# self.client.item(drive='me', id=id_of_file).download('./path_to_download_to.txt')



	# def createdb(self):
	# 	wmtfolder = onedrivesdk.Folder()
	# 	wmtfolderitem = onedrivesdk.Item()
	# 	wmtfolderitem.name = '.wmt'
	# 	wmtfolderitem.folder = wmtfolder
	# 	returned_item = self.client.item(drive='me', id='root').children.add(wmtfolderitem)

	# 	dbfile = onedrivesdk.File()
	# 	dbitem = onedrivesdk.Item()
	# 	dbitem.name = 'wmtdb.csv'
	# 	dbitem.file = dbfile
	# 	returned_item = self.client.item(drive='me', id='root').children.add(i)

	# def getdb(self):
	# 	root_folder = self.client.item(drive='me', path=ONEDRIVEDB_WMT_DB_PATH).download
	# 	id_of_file = root_folder[0].id

	# 	self.client.item(drive='me', id=id_of_file).download('./path_to_download_to.txt')
