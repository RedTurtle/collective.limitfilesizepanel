Changelog
=========

3.0.4 (unreleased)
------------------

- Fix stale bundle name in add_bundle_on_request: the JSON widget bundle
  was renamed from "z3cform-jsonwidget-bundle" to "z3cform-jsonwidget" in
  collective.z3cform.jsonwidget's Plone 6 port, but this control panel
  never followed the rename. Also request the "react-bundle" bundle,
  which the widget needs and which collective.z3cform.jsonwidget now
  gates behind an explicit opt-in (see collective.z3cform.jsonwidget
  3.0.0 and redturtle.reactbundle).
  [mamico]
- Update classifiers/references to Plone 6.1 (was still declaring Plone
  5.2/Python 3.8 even though this package already runs fine on 6.1 in
  production): added a test_plone61.cfg, bumped Framework/Python
  classifiers, and switched the "Tests" GitHub Actions job to a plain
  pip install + zope-testrunner (the old Python 3.7/3.8 matrix no
  longer resolves on current runners, and buildout.plonetest's
  test-6.1.x.cfg pins a zc.buildout version that fails to install on
  Python 3.11 for unrelated reasons).
  [mamico]
- Fix tests for Plone 6.1: ``plone.namedfile.field.validate_image_field``/
  ``validate_file_field`` were removed (replicated them locally via the
  ``IPluggableImageFieldValidation``/``IPluggableFileFieldValidation``
  adapters they used to wrap); ``FakeImageField``/``FakeFileField`` test
  doubles were missing the ``accept`` attribute the real validators now
  check; ``portal_quickinstaller`` no longer exists (removed the one
  unused reference to it, and the already-existing ``get_installer()``
  based tests continue to use the modern
  ``is_product_installed``/``uninstall_product`` API instead of the
  removed ``isProductInstalled``/``uninstallProducts``).
  [mamico]


3.0.3 (2023-09-27)
------------------

- Fix check in validators if product is not installed.
  [cekk]


3.0.2 (2023-05-02)
------------------

- Raise custom ValidationError to have a 400 on restapi calls.
  [cekk]


3.0.1 (2023-05-02)
------------------

- Raise ValueError instead Invalid for restapi calls.
  [cekk]


3.0.0 (2023-04-27)
------------------

- Python3 support.
  [cekk]
- Drop usage of persistent fields in registry. Now we use collective.z3cform.jsonwidget.
  [cekk]
- Change validator to work also with restapi calls.
  [cekk]


2.1.2 (2018-07-17)
------------------

- Fix release
  [cekk]

2.1.1 (2018-07-17)
------------------

- Fix permission for upload view
  [eikichi18]


2.1.0 (2018-05-09)
------------------

- Fix validators for Dexterity fields. Now works well with Files and images
  [cekk]
- Add support for Tinymce validation also for Plone 5
  [cekk]


2.0.3 (2018-01-30)
------------------

- Don't break validation for view with no spcific context.
  [bsuttor]


2.0.2 (2017-09-15)
------------------
- Fix brown bag release
  [cekk]

2.0.1 (2017-09-14)
------------------

- Don't break validation if the product isn't installed.
  If not installed, shouldn't do nothing.
  [cekk]

- Fix patched__call__ if the product isn't istalled.
  [arsenico13]

2.0.0 (2017-05-04)
------------------

- Version 1.3 don't uninstall cleanly
  [keul]
- Now validates also files and images created in TinyMCE
  [cekk]
- Dexterity support
  [cekk]

1.3 (2015-07-06)
----------------

- Added type+field configuration
  [keul]
- Pyflakes cleanup
  [keul]

1.2 (2013-08-19)
----------------

- Add German translations.
  [jone]
- Ensure consistency of megabyte symbols to be ``MB``.
  [davidjb]


1.1.2 (2013-03-26)
------------------

- run rolemap configurations when upgrading from older versions
  [keul]

1.1.1 (2013-03-26)
------------------

- fixed pypi classifiers [keul]

1.1 (2013-03-26)
----------------

- Added a proper uninstall step [keul]
- Now based on `collective.monkeypatcher`__ [keul]
- i18n refactoring [keul]
- Do not try to automatically validate file size for already existings attachments.

  This provent to get validation error when editing file after size limit
  has been changed [keul]

- Added new permission "collective.limitfilesizepanel: Manage limit file size settings".
  Users with this permission can bypass size validation [cekk]

  __ http://pypi.python.org/pypi/collective.monkeypatcher

1.0 (Unreleased)
----------------

- Initial release
