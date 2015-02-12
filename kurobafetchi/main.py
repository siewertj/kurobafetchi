_usage = """
-----------------------------------------------------------------------------------------------------
Currently requires python3 to run (the urllib mostly uses the python3 way).

Parses the board/thread that you pass it and then will download all the images from that page. This
downloads all files under a folder called '4chan' in the current directory by default. All Files will
download to [dst]/[board]/[thread]/[filename] so 'dst' is basically where you want that rooted.

This is multi-threaded, creating 4 threads by default. If you change that just be aware that each
thread does its own url request so lots of threads could cause you to flood the server you're pulling
from. Respect the sites api. If you have any ideas/suggestions let me know.
-----------------------------------------------------------------------------------------------------
""".format(__file__)

from kurobafetchi.api4chan import ThreadPage
from kurobafetchi.api4chan import BoardListPage
from kurobafetchi.web.webfetcher import WebFetcher
import argparse
from time import sleep
from os.path import normpath, join
from pkg_resources import get_distribution


def get_version():
	dist = get_distribution('kurobafetchi')
	return dist.version


def main():
	""" setup the command line arg information """
	parser = argparse.ArgumentParser(
			prog='kurobafetchi',
			description = _usage,
			formatter_class = argparse.RawDescriptionHelpFormatter)

	parser.add_argument('board', type=str, help="board to grab from")
	parser.add_argument('thread', type=str, help="thread to grab from")
	parser.add_argument('-d', '--destination', metavar='dir', type=str,
			help="directory to download to", default='4chan')
	parser.add_argument('--force-ascii', action='store_true',
			help="forces downloaded files to be in ascii")
	parser.add_argument('-v', '--verbosity', metavar='lvl', type=int, default=1,
			help="how verbose you want output to be. 0=None, 1=Finish, 2=Downloaded, 3=All")
	parser.add_argument('--version', action='version',
			version="%(prog)s {0}".format(get_version()))

	arg = parser.parse_args() #parse from the command line

	title = BoardListPage.get_boardinfo_dict()[arg.board].replace('/','_')
	thread = ThreadPage(arg.board, arg.thread)
	path = normpath('{0}/{1} - {2}/{3}_{4}'.format(
			arg.destination,
			arg.board,
			title,
			thread.title,
			arg.thread))


	if arg.verbosity > 0:
		print('board {0} thread {1} to {2}'.format(arg.board, arg.thread, path))

	kMaxNameSize = 100

	fetcher = WebFetcher()
	for url,name,tim,ext in thread.images():
		if len(name) > kMaxNameSize:
			name = name[:kMaxNameSize]

		filename = '{0}_{1}{2}'.format(name, tim, ext)

		if arg.force_ascii:
			filename = filename.encode('ascii', errors='ignore').decode('utf-8')

		fullpath = join(path, filename)
		fetcher.fetch(url,fullpath,overwrite=False)


	fetcher.wait(verbosity=arg.verbosity)