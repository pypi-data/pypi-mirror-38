import os

from setuptools import setup, find_packages

DESCRIPTION = "Extenions - Set of iPython and Jupyter extensions"
NAME = "pppextensions"
AUTHOR = "Extensions Development Team"
AUTHOR_EMAIL = "qwjlegend@gmail.com"
URL = 'https://github.com/qwjlegend/ppextensions'
DOWNLOAD_URL = 'https://github.com/qwjlegend/ppextensions'
LICENSE = 'BSD License'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
print(README)
VERSION = '0.0.2'

install_requires = [
    'ipython>=1.0',
    'requests',
    'Gitpython',
    'nbdime'
]

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=README,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      download_url=DOWNLOAD_URL,
      license=LICENSE,
      packages=find_packages(),
      classifiers=[
          'Intended Audience :: System Administrators',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'],
      install_requires=install_requires,
      extras_require={
          'dev': [
              'pycodestyle'
          ]
      })

