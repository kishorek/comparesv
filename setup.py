try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

from version import __version__
import os


def open_file(fname):
	return open(os.path.join(os.path.dirname(__file__), fname))


setup(
	name='comparesv',
	packages=[''],
	version=__version__,
	license='MIT',
	description='CSV Comparison on steroids',
	long_description=open_file('README.md').read(),
	long_description_content_type="text/markdown",
	author='Kishore Kumar',
	author_email='ukisho@gmail.com',
	url='https://github.com/kishorek',
	keywords=['CSV', 'Comparison', 'Compare'],
	install_requires=[
		'chardet==3.0.4',
		'tqdm==4.18.0',
		'unidecode==1.1.1',
		'doublemetaphone==0.1',
		'fuzzywuzzy==0.18.0',
		'python-Levenshtein==0.12.0'
	],
	entry_points={
		'console_scripts': [
			'comparesv = cli:main'
		]
	},
	classifiers=[
		'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		'Intended Audience :: Developers',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3.6',
		'Natural Language :: English',
		'Topic :: Scientific/Engineering :: Information Analysis',
		'Topic :: Utilities'
	]
)
