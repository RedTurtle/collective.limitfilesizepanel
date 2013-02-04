Introduction
============

This product monkey patch the original MaxSizeValidator used in file and image upload field.
Then through plone.app.registry and z3c.form provide a user interface to customize site by
site the limit size in Mb for uploads.


How to use it
=============

Just add the product to the buildout and install it in the site you want to use. A new action
(''Limit file size settings'') will be added in the plone control panel and here, ''Admin'' and
''Site Administrator'' will be able to set a limit for files and images upload.


Dependencies
============

This products has been tested on:
 * Plone 3.3
 * Plone 4.2

It's based on `plone.app.registry`__ that it not part of Plone on 3.3 version. You need to be
sure that a compatible version is used (in my experience: use `version 1.0b1`__)

 __ http://pypi.python.org/pypi/plone.app.registry
 __ http://pypi.python.org/pypi/plone.app.registry/1.0b1


Credits
=======

Developed with the support of `Regione Emilia Romagna`__;


Regione Emilia Romagna supports the `PloneGov initiative`__.

 __ http://www.regione.emilia-romagna.it/
 __ http://www.plonegov.it/


Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
