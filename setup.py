try:
	from setuptools import setup 
except ImportError:
	from distutils.core import setup 

config = {
	'description' : 'Auto Work',
	'author' : 'renyongjian',
	'url' : 'URL to get it as qq.com',
	'download_url' : 'here',
	'author_email' : '731634539@qq.com',
	'version' : '0.1',
	'install_requires' : ['nose'],
	'packages' : ['autowork'],
	'scripts' : [],
	'name' : 'auto_work',
}

setup(**config)

