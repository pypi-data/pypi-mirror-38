import os,sys
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop


_here = os.path.abspath(os.path.dirname(__file__))
dir_mtree = os.path.join(_here,'metricaltree')

def install_stanford_parser(dir_mtree):
	print '>> INSTALLING STANFORD CORENLP PARSER TO DIRECTORY:',dir_mtree
	#os.system('cd '+dir_mtree+' && '+'./get-deps.sh')

class PostDevelopCommand(develop):
	"""Post-installation for development mode."""
	def run(self):
		install_stanford_parser(dir_mtree)
		develop.run(self)

class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		install_stanford_parser(dir_mtree)
		install.run(self)

with open("README.md", "r") as fh:
	long_description = fh.read()

with open("requirements.txt", "r") as fh:
	requirements = [x.strip() for x in fh.read().split('\n') if x.strip()]

setup(
	name='prosodic',
	version='1.1.19',
	description=('PROSODIC: a metrical-phonological parser, written in Python. For English and Finnish, with flexible language support.'),
	long_description=long_description,
	long_description_content_type="text/markdown",
	author='Ryan Heuser',
	author_email='heuser@stanford.edu',
	url='https://github.com/quadrismegistus/prosodic',
	license='MPL-2.0',
	packages=['prosodic','metricaltree'],
	install_requires=requirements,
	include_package_data=True,
	cmdclass={
		'develop': PostDevelopCommand,
		'install': PostInstallCommand,
	},
	classifiers=[
		#'Development Status :: 3 - Alpha',
		#'Intended Audience :: Science/Research',
		#'Programming Language :: Python :: 2.7',
		#'Programming Language :: Python :: 3.6'
	],
	)
