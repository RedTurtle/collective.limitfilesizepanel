from setuptools import setup, find_packages
import os

version = '1.1.dev0'

setup(name='collective.limitfilesizepanel',
      version=version,
      description="Add configuration to set file size limit through control panel",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.3"
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        ],
      keywords='plone limit file size',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/collective.limitfilesizepanel',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.registry',
          'collective.monkeypatcher',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
