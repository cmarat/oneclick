#!/usr/bin/env python

from setuptools import setup, find_packages

requirements = open('requirements.txt').read().splitlines()
setup(name='CommitDemo',
      version='0.1',
      package_data={'linkitup': ['plugins.yaml', 'templates/*.html',
                  'templates/*.query', 'templates/*.js', 'static/js/*.js',
                  'static/css/*.css', 'static/css/*.png', 'static/img/*.png',
                  'static/js/vendor/*.js', 'migrations/*.*',
                  'migrations/versions/*']},
      packages=find_packages(),
      scripts=['manage.py'],
      install_requires=requirements)
