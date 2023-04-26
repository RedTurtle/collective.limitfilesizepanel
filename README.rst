This is an helper package that setup a RedTurtle's Plone site ready to work with Volto.


|python| |version| |ci| |coverage| |downloads| |license|

.. |python| image:: https://img.shields.io/pypi/pyversions/collective.limitfilesizepanel.svg
  :target: https://pypi.python.org/pypi/collective.limitfilesizepanel/

.. |version| image:: http://img.shields.io/pypi/v/collective.limitfilesizepanel.svg
  :target: https://pypi.python.org/pypi/collective.limitfilesizepanel

.. |ci| image:: https://github.com/RedTurtle/collective.limitfilesizepanel/actions/workflows/tests.yml/badge.svg
  :target: https://github.com/RedTurtle/collective.limitfilesizepanel/actions

.. |downloads| image:: https://img.shields.io/pypi/dm/collective.limitfilesizepanel.svg
   :target: https://pypi.org/project/collective.limitfilesizepanel/

.. |license| image:: https://img.shields.io/pypi/l/collective.limitfilesizepanel.svg
    :target: https://pypi.org/project/collective.limitfilesizepanel/
    :alt: License

.. |coverage| image:: https://coveralls.io/repos/github/redturtle/collective.limitfilesizepanel/badge.svg?branch=master
    :target: https://coveralls.io/github/redturtle/collective.limitfilesizepanel?branch=main
    :alt: Coverage
    

Introduction
============

Plone Archetypes framework already gives you a max size validation for files and images, but the default
configuration has some drawbacks:

* is not simple to customize (best way is to use `plone.recipe.atcontenttypes`__)
* is the same for every Plone site of the environment

__ http://pypi.python.org/pypi/plone.recipe.atcontenttypes/

This product will let you customize this validation from Plone user interface.

How to use it
=============

Just add the product to the buildout and install it in the site you want to use.

A new "*Limit file size settings*" option will be added in the control panel, where you can change the
*File* and *Image* attachments.

No users will be able to upload files that exceed the limit. Also in TinyMCE text editor.

.. image:: https://raw.githubusercontent.com/RedTurtle/collective.limitfilesizepanel/93abb025ecae1070e28ead13874fc07dc25de52e/docs/collective.limitfilesizepanel-1.3-01.png
   :alt: Settings

Advanced use
------------

While default general purpose file and image settings can be OK for most common scenarios,
you can also define custom settings for specific content types: just fill the
"**Settings for other content types and fields**" section.

.. image:: https://raw.githubusercontent.com/RedTurtle/collective.limitfilesizepanel/93abb025ecae1070e28ead13874fc07dc25de52e/docs/collective.limitfilesizepanel-1.3-02.png
   :alt: Type's settings

Configuration in that section wins over global configuration.

Validator bypass
================

If some users need to bypass the validation and upload some larger files, there is a new permission
"*collective.limitfilesizepanel: Bypass limit size*" that allows to do this.

You only need to set this permission to some roles, and they'll have no upload limits.

Dependencies
============

This products has been tested on:

* Plone 3.3
* Plone 4.2
* Plone 4.3

It's based on `plone.app.registry`__ that it not part of Plone on 3.3 version. You need to be
sure that a compatible version is used (in my experience: use `version 1.0b1`__).

 __ http://pypi.python.org/pypi/plone.app.registry
 __ http://pypi.python.org/pypi/plone.app.registry/1.0b1

Credits
=======

Developed with the support of:

* `Regione Emilia Romagna`__
* `Province of Vicenza`__

  .. image:: http://www.provincia.vicenza.it/logo_provincia_vicenza.png
     :alt: Province of Vicenza - logo

All of them supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.provincia.vicenza.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
