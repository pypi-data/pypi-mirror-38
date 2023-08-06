====================
netapp-lib Changelog
====================

Change Log
----------

version: 2017.10.30
~~~~~~~~~~~~~~~~~~~
released: Mon Oct 30 2017
tags: bug-fix
 - Remove dependency on oslo.log.
 - Add lxml as a setup requirement
 - Remove i18n markup
 - Remove proprietary license. This code was borrowed from NetApp's
   integrations in OpenStack Cinder and OpenStack Manila, which are
   both licensed under Apache V2 License.

version: 2016.10.14
~~~~~~~~~~~~~~~~~~~
released: Fri Oct 14 2016
tags: minor bug-fix
- Fixed bug in code parsing ZAPI errors.

version: 2015.09.25
~~~~~~~~~~~~~~~~~~~
released: Fri Sep 25 2015
tags: attributions
- Updated source files to include OpenStack attributions.
- Added NOTICE.txt to include previous License.
- Added description to setup.py

version: 2015.08.20
~~~~~~~~~~~~~~~~~~~
released: Thu Aug 20 2015
tags: release

- Updated README.rst.
- Updated initial LICENSE.txt.
- Updated setup to include static files on installation.

version: 0.2
~~~~~~~~~~~~
released: Fri Aug 07 2015
tags: pre-release
- Added xmltodict and translation capability to NaServer ZAPI interface

version: 0.1
~~~~~~~~~~~~
released: Mon Jul 21 2015
tags: initial
- Compiled the ZAPI and REST interface code used within manila and cinder
  clients on OpenStack.
- Structured the project for PyPi release.
- Added tox.ini to enforce pep8 style-guide and run unit tests.
