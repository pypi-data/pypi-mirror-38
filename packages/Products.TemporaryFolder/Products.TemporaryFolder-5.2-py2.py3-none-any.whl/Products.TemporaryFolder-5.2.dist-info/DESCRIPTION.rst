Overview
========

Zope temporary storage / folder support.

Contains ``Products.TemporaryFolder`` and ``Products.ZODBMountPoint``.

Changelog
=========

5.2 (2018-11-06)
----------------

- Add support for Python 3.7.

- Update forms to Bootstrap ZMI.
  (`#6 <https://github.com/zopefoundation/Products.TemporaryFolder/pull/6>`_)

- Fix logging traceback in Python 2.
  [pbauer]

- Fix creating a temp_folder in Python 2.
  (`#7 <https://github.com/zopefoundation/Products.TemporaryFolder/pull/7>`_)


5.1 (2018-06-06)
----------------

- Bring back Application initialization (creation of BrowserIdManager and
  SessionDataManager in the ZODB on first startup).
  This release requires Zope >= 4.0b5.

- Drop support for Python 3.4.


5.0 (2018-04-13)
----------------

- Remove dysfunctional LowConflictConnection.

- Add support for Python 3.4, 3.5 and 3.6.

4.0 (2016-08-02)
----------------

- Add in code of `Products.TemporaryFolder` and `Products.ZODBMountPoint`.

- Require `Zope >= 4`.

3.0 (2016-08-02)
----------------

- Create a separate distribution called `Products.TemporaryFolder` without
  any code inside it. This allows projects to depend on this project
  inside the Zope 2.13 release line.


