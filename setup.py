from setuptools import setup, find_packages
import os

version = '1.0b2'

setup(name='collective.archiveviewer',
      version=version,
      description="Allows to upload archive files (check readme for supported types) \
      and access their contents trough the web, without having to download and extract them",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Simone Orsi [simahawk]',
      author_email='simahawk@gmail.com',
      url='https://github.com/collective/collective.archiveviewer',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
