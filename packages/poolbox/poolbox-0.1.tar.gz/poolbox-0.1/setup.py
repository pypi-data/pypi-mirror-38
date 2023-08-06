import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()


setup(name='poolbox',
      version=0.1,
      description='PDF Toolbox WebService',
      long_description=README,
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Framework :: Pylons",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='atReal',
      author_email='contact@atreal.fr',
      url='https://www.atreal.fr',
      license='GPLv2',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'cornice',
          'cornice_swagger',
          'ipdb',
          'jinja2',
          'lxml',
          'pdfkit',
          'requests',
          'waitress',
      ],
      entry_points="""\
      [paste.app_factory]
      main=poolbox:main
      """,
      paster_plugins=['pyramid'])
