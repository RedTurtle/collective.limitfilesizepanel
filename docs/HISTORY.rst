Changelog
=========

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
