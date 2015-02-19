from setuptools import setup

setup(
	name = 'kurobafetchi',
	version = '0.4.0',
	description = 'Grabs pictures from 4chan threads',
	author = 'siewert',
	packages = ['kurobafetchi', 'kurobafetchi.web'],
	scripts = ['scripts/fetchi.py']
)