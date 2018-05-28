Changelog
=========

2.1.1 (unreleased)
------------------

- Change fileupload view permission: collective.limitfilesizepanel.LimitFileSizePanel 
  is too strinct. Better a cmf.AddPortalContent
  [lucabel]


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
