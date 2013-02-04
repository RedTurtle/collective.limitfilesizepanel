Introduction
============

This product monkey patch the original Plone max size validation (where the configuration is complex 
and hurts all Plone site in the same buildout) to a site-specific ones.

How to use it
=============

Just add the product to the buildout and install it in the site you want to use.

A new "*Limit file size settings*" option will be added in the control panel, where you can change the
*File* and *Image* attachments.

No users will be able to upload files that exceed the limit.

Dependencies
============

This products has been tested on:

* Plone 3.3
* Plone 4.2

It's based on `plone.app.registry`__ that it not part of Plone on 3.3 version. You need to be
sure that a compatible version is used (in my experience: use `version 1.0b1`__).

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
