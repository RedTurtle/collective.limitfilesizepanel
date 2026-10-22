Changelog
=========

3.0.4 (unreleased)
------------------

- Added @limit-sizes service and limit-sizes expander to expose file and
  image size limits (in MB), the new_data_only setting and the bypass
  permission of the current user.
  Run upgrade step to 1400 to set the new permission's roles.
  [daniele]
- Removed "Settings for other content types and fields" (types_settings) setting
  and collective.z3cform.jsonwidget dependency: limits are now only the global
  ones for files and images.
  Upgrade step to 1400 removes the old registry record and uninstalls
  collective.z3cform.jsonwidget (if installed and not required by other products).
  collective.z3cform.jsonwidget is still in install_requires only to allow its
  uninstall: it will be removed in the next release.
  [cekk]
- Use native (PEP 420) namespace for ``collective``.
  [cekk]
- Expose the control panel on plone.restapi (@controlpanels/limitfilesize-settings),
  so it can be managed from Volto.
  [cekk]
- "Validate only new data" is no more required, so it can be unchecked.
  [cekk]
- Support Plone 6.0, 6.1 and 6.2 on Python 3.11+ and drop Plone 5.2 support.
  Configure the package with plone.meta (tox and GitHub Actions) and remove
  the old buildout-based test setup.
  [cekk]


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

- Don't break validation for view with no specific context.
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

- Fix patched__call__ if the product isn't installed.
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
