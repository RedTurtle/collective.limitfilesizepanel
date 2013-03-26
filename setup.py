from setuptools import setup, find_packages
import os

version = '1.2.dev0'

tests_require = ['zope.testing', 'Products.PloneTestCase']

setup(name='collective.limitfilesizepanel',
      version=version,
      description="Configure files and images size limit through Plone control panel",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        ],
      keywords='plone plonegov limit filesize validation',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/products/collective.limitfilesizepanel',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(test=tests_require),
      install_requires=[
          'setuptools',
          'plone.app.registry',
          'collective.monkeypatcher>=1.0',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
