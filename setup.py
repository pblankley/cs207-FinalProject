#from distutils.core import setup
from setuptools import setup

setup(
    name = 'chemkin207',
    packages = ['chemkin207','chemkin207.tests'],
    package_data={'chemkin207': ['supporting/*.sqlite','tests/test_xmls/*.xml','tests/test_tables/*.tex']},
    version = '0.1.13',
    description = 'Simple chemical kinetics library.',
    author = 'Paul Blankley, Ryan Janssen, Boyuan Sun',
    author_email = 'pblankley@g.harvard.edu',
    copyright = 'MIT license',
    url = 'https://github.com/cs207-g1/cs207-FinalProject',
    download_url = 'https://github.com/cs207-g1/cs207-FinalProject/tarball/0.1.13',
    keywords = ['chemical kinetics'],
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers = [
        'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License'
        ]
)
