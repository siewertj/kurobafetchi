#! /bin/python3

__author__ = 'siewert'

""" Description:
	Grabs all images on a 4chan board using 4chans api (json pages). GitHub (link below) has
	more information as to how to use the api and other features; this focuses on downloading
	images and has some framework for potentially doing more. This was built with python 3.x
	and will not support 2.x without modifications.

	The 'urlgen_' functions return the urls that point to the various json objects. The args
	for those are:
		board - the 4chan board (ie 'w' for the anime_wallpaper board, or 'b' for the adventurous.
		thread - the thread number
		tim - json field for the image
		tims - json field for the image thumbnail
		ext - the json field for the extension type
"""

api_site = 'https://github.com/4chan/4chan-API'
api_rules = '''API Rules
	1. Do not make more than one request per second.
	2. Thread updating should be set to a minimum of 10 seconds, preferably higher.
	3. Use If-Modified-Since when doing your requests.
	4. Make API requests using the same protocol as the app. Only use SSL when a user is accessing
		your app over HTTPS.
	5. More to come later...'''
api_terms = '''API Terms of Service
	1. You may not use "4chan" in the title of your application, product, or service.
	2. You may not use the 4chan name, logo, or brand to promote your app, product, or service.
	3. You must disclose the source of the information shown by your app, product, or service as
		4chan, and provide a link.
	4. You may not market your application, product, or service as being "official" in any way.
	5. You may not clone 4chan or its existing features/functionality. Example: Don't suck down our
		JSON, host it elsewhere, and throw ads around it.
	6. These terms are subject to change without notice.'''


from .web.jsonpage import JsonPage
from re import findall, sub


def convert_html_entities(s):
	for x in set(findall("&#\d+;", s)):
		s = s.replace(x, chr(int(x[2:-1])))

	s = sub("\<.*\>", '', s) # remove html tags
	print(s)


class urlgen:
	""" This describes the various urls that are accessed through the api (ie the json
	pages). these functions return a string representing the url. """
	@staticmethod
	def thread(board, thread):
		return '{0}/{1}/thread/{2}.json'.format('http://a.4cdn.org', board, thread)
	@staticmethod
	def modtimes(board):
		return '{0}/{1}/threads.json'.format('http://a.4cdn.org', board)
	@staticmethod
	def board(board, page):
		return '{0}/{1}/{2}.json'.format('http://a.4cdn.org', board, page)
	@staticmethod
	def catalog(board):
		return '{0}/{1}/catalog.json'.format('http://a.4cdn.org', board)
	@staticmethod
	def allboards():
		return '{0}/boards.json'.format('http://a.4cdn.org')
	@staticmethod
	def img(board, tim, ext):
		return '{0}/{1}/{2}{3}'.format('http://i.4cdn.org', board, tim, ext)
	@staticmethod
	def thumbnail(board, tims):
		return '{0}/{1}/{2}{3}'.format('http://t.4cdn.org', board, tims, '.jpg')


class BoardListPage:
	@staticmethod
	def get_boardinfo_dict():
		pg = JsonPage(urlgen.allboards())
		data = pg.read()
		return {x['board']: x['title'] for x in data['boards']}

class ThreadPage(JsonPage):
	def __init__(self, board, thread):
		url = urlgen.thread(board, thread)
		JsonPage.__init__(self, url)
		self.jsondata = JsonPage.read(self)
		self.board = board
		self.thread = thread

		firstpost = self.jsondata['posts'][0]
		if 'semantic_url' in firstpost:
			self.title = firstpost['semantic_url']
		else:
			self.title = firstpost.setdefault('sub', '')

	def images(self):
		for post in self.jsondata['posts']:
			if ('tim' in post) and ('ext' in post): # if the post contains an image
				url = urlgen.img(self.board, post['tim'], post['ext']) # get img url
				yield (url, post['filename'], post['tim'], post['ext'])