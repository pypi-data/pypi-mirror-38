#from distutils.core import setup
from setuptools import setup

with open("README.md") as f:
  long_description = f.read()

setup(
  name = 'error_counter',
  packages = ['error_counter'], # this must be the same as the name above
  version = '0.1.0',
  description = 'Error Counter: Count error (e.g. network error) beyond process boundary, then issue fix command when exceeded threshold.',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Takeyuki UEDA',
  author_email = 'gde00107@nifty.com',
  license='MIT',
  url = 'https://github.com/UedaTakeyuki/error-counter', # use the URL to the github repo
  keywords = ['Counter', 'Error', 'Reset'], # arbitrary keywords
  classifiers = ['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'Topic :: Terminals'
  ],
  install_requires=[
    'incremental_counter'
  ]
)
