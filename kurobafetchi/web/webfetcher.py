__author__ = 'siewert'

from . import simplepage
import concurrent.futures


def fetchfile(url, fullpath, overwrite):
	page = simplepage.WebPage(url)
	return page.fetch(fullpath, overwrite)


class WebFetcher:
	""" Basically a thread executor that spins off threads to download url pages. The
	basic functionality is to init and then push 'fetch' tasks to it. Downloads will
	start as soon as they are pushed to the queue with 'fetch'. Once all the download
	jobs are added, call 'wait' on the WebFetcher to wait for the downloads to finish
	and clean up the threads. 'wait' will spit out progress information. """

	def __init__(self, workers=4):
		self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=workers)
		self.results = []

	def fetch(self, url, fullpath, overwrite=False):
		self.results.append(self._executor.submit(fetchfile, url,fullpath,overwrite))

	def wait(self, verbosity=1):
		cnt, sztot = 0, 0
		for future in concurrent.futures.as_completed(self.results):
			(dst, url, size) = future.result()
			if size > 0:
				cnt += 1
				sztot += size
				if verbosity >= 2:
					print('[%d/%d] %.2f kB (%.2f MB tot) - %s'
							% (cnt, len(self.results), size/10**3, sztot/10**6, dst.encode('ascii','ignore').decode('utf-8')))

			elif verbosity >= 3:
				print('file %s already exists, did not download' % (dst))

		self._executor.shutdown(wait=True)
		if verbosity >= 1:
			print('Downloaded %d of %d files, %.2f MB downloaded' % (cnt, len(self.results), sztot/10**6))