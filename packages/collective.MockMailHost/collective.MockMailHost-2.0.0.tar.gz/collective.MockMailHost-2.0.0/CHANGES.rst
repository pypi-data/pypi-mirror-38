Changelog
=========

2.0.0 (2018-11-06)
------------------

Breaking changes:

- Do not depend on old SecureMailHost any longer.
  [pbauer]

New features:

- Python 3 support.
  [pbauer]


1.1.0 (2018-06-27)
------------------

- Fix import location, Globals has been removed.
  [gforcada]

- Rework tests setup.
  [gforcada]


1.0 (2016-01-25)
----------------

- Fix MIMEText compatibility (broken since 0.9).
  [jone]


0.9 (2015-07-10)
----------------

- Clean up msg before sending. Otherwise Plone self registration
  email does not work [sureshvv]


0.8 (2015-06-13)
----------------

- Add browser view for functional testing [Casecarsid]


0.7 (2013-07-05)
----------------

- MANIFEST [sureshvv]


0.6 (2013-07-03)
----------------

- Track msg_type also.
  [sureshvv]

- Behave more like ``collective.testcaselayer``'s MockMailHost.
  [saily]

- Documentation updates
  [saily]


0.5 - 2012-09-25
----------------

- Remove ZopeSkel and Paster dependency from setup.py
  [saily]

- Moved to github and changed to README.rst, links in setup.py
  [saily]

- Allow multiple paramters for ``send`` and ``secureSend`` method in
  MockMailHost class.  [saily]


0.4 (2011-05-17)
----------------

- Register MockMailHost in SiteManager to get MockMailHost when using
  ``getToolByName(context, 'MailHost')`` or ``getUtility(IMailHost)``.
  [saily]

- Inherit from MailHost instead of SimpleItem
  [saily]

- Implement the secureSend method
  [saily]


0.3 (2011-04-04)
----------------

- Add ``**kwargs`` to MockMailHost's send method to support mto, mfrom, ...
  keyword arguments as default MailHost does.  [saily]

- Added file for generic setup various handlers
  [sureshvv]


0.2 (2010-05-21)
----------------

- Added tests
  [sureshvv]


0.1 (2010-05-16)
----------------

- Initial release
  [sureshvv]
