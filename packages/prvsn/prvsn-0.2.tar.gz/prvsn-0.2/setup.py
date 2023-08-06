from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
	long_description = f.read()
	
with open(path.join(here, 'requirements.txt')) as f:
	requirements = f.read()

setup(
	name='prvsn',
	version=0.2,
	author='Arnaud Coomans',
	author_email='hello@acoomans.com',
	description='A simple provisioning tool',
	long_description=long_description,
	url='https://github.com/acoomans/prvsn',
	license='BSD',
	platforms='any',
	keywords=[
		'provision',
	],
	install_requires=requirements,
	scripts=['scripts/prvsn'],
	packages=find_packages(exclude=['contrib', 'docs', 'tests']),
	test_suite='tests',
)