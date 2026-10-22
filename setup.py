from setuptools import find_namespace_packages
from setuptools import setup

import os

version = "3.1.0"

tests_require = [
    "plone.app.testing",
    "plone.testing>=5.0.0",
    "plone.app.contenttypes",
    "plone.app.robotframework[debug]",
    "plone.restapi[test]",
]

setup(
    name="collective.limitfilesizepanel",
    version=version,
    description="Configure files and images size limit through Plone control panel",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: OS Independent",
    ],
    keywords="plone plonegov limit filesize validation",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="https://github.com/RedTurtle/collective.limitfilesizepanel",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.limitfilesizepanel/",
        "Source": "https://github.com/RedTurtle/collective.limitfilesizepanel",
        "Tracker": "https://github.com/RedTurtle/collective.limitfilesizepanel/issues",
    },
    license_expression="GPL-2.0-only",
    python_requires=">=3.11",
    packages=find_namespace_packages(include=["collective.*"]),
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(test=tests_require),
    install_requires=[
        "setuptools",
        "plone.api",
        "plone.app.registry",
        "plone.restapi",
        "collective.monkeypatcher>=1.0",
        "z3c.unconfigure",
        # no more used: it's here only to be uninstalled in upgrade step to 1400.
        # Remove it in the next release.
        "collective.z3cform.jsonwidget>=2.0.2",
    ],
    entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
)
