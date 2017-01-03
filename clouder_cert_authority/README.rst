.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

=============================
Clouder Cert Authority
=============================

This module provides a Cert Authority using Clouder and CFSSL,


Configuration
=============

Clouder configuration instructions are available at https://clouder.readthedocs.io/

Usage
=====

To use this module, you need to:

#. Create a CFSSL Service in the Clouder Control Panel

Known issues / Roadmap
======================

* Add more Signature Profile options - https://github.com/cloudflare/cfssl/blob/86ecfbe5750ebf05565e4c80104d0a7919792fee/doc/cmd/cfssl.txt#L113
* Need to add a hook so that services dependent on revoked certs are refreshed
* Don't run as root

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/clouder-community/clouder/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Dave Lasley <dave@laslabs.com>

Maintainer
----------

This module is maintained by Clouder Community.

To contribute to this module, please visit https://github.com/clouder-community/clouder
