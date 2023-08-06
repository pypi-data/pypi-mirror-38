from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='asciigraphic',
      version=version,
      description="Ascii graphic",
      long_description="""\
This is ascii graphic project wor somethemes""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ascii graph console',
      author='chetnuy',
      author_email='chetnuy@gmail.com',
      url='https://gitthub.com/chetnuy/ascii',
      license='GPU',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['asciichartpy' ],
      entry_points={'console_scripts': ['asciigraphic = asciigraphic.__main__:main']},
      )
