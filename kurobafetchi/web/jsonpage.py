__author__ = 'siewert'

from . import simplepage
import json


class JsonPage(simplepage.WebPage):

	def read(self):
		data = simplepage.WebPage.read(self)
		jsondata = json.loads(data.decode('utf-8'))
		return jsondata