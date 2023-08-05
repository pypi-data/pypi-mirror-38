from setuptools import find_packages, setup

VERSION = '0.1.0'
REQUIRED_PYTHON = (3, 6)

long_description = '''NFC Key a security application with
admin interface.'''

setup(
	# Metadata
    name='NFC Key',
    version=VERSION,
	author='Pavel Isupov',
	author_email='pavel.isupov.nz@gmail.com',
	description='NFC Key project',
	long_description=open('README').read(),
	license='LICENSE',
	keywords='NFC',
	url='https://changeme.com',
	
	# Requirements
	python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
	
	# Package info
	packages=find_packages(),
	
)