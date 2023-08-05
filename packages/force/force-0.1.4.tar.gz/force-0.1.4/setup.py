from distutils.core import setup

from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
  name = 'force',
  packages = ['force'], # this must be the same as the name above
  version = '0.1.4',
  description = 'A method for visualizing the receiptive fields of a neural network',
  author = 'Mat Kallada',
  author_email = 'matkallada@gmail.com',
  url = 'https://pypi.org/project/force/', # use the URL to the github repo
  keywords = ['machine learning', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  long_description=long_description,
  long_description_content_type='text/markdown'
)
