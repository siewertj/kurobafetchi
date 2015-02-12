__author__ = 'siewert'

from urllib.request import build_opener
from os import makedirs
from os.path import exists, dirname
from io import BytesIO
from gzip import GzipFile


def get_condis_filename(htmlpage):
		condis = htmlpage.page.info().get('Content-Disposition', None)
		if not condis:
			return None
		for key,_,val in [x.partition('=') for x in condis.split(';')]:
			if key.strip().lower() == 'filename':
				return val.strip(' "')
		return None

		
class WebPage:
	kChunkSize = 5000
	opener = build_opener()
	opener.addheaders = [('Accept-Encoding', 'gzip')] #deflate	
	
	def __init__(self, url):
		self.page = self.opener.open(url)
	
	def read(self):
		encoding = self.page.info().get('Content-Encoding')
		data = self.page.readall()
		if encoding in ['gzip', 'x-gzip']:
			data = GzipFile(None, 'rb', 9, BytesIO(data)).read()
		return data

	def fetch (self, fullpath, overwrite=False):
		if not overwrite and exists(fullpath):
			return None,None,0

		makedirs(dirname(fullpath), exist_ok=True)

		with open(fullpath, 'wb') as fp:
			fp.write(self.read())
			sz = fp.tell()
			#for chunk in iter(lambda: self..read(self.kChunkSize)):
		return (fullpath, self.page.geturl(), sz)