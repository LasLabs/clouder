.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

==============================
Clouder Template - Red October
==============================

This module provides a Clouder Template for Red Octover.

Red October is a cryptographically-secure implementation of the two-person rule
to protect sensitive data. From a technical perspective, Red October is a
software-based encryption and decryption server. The server can be used to
encrypt a payload in such a way that no one individual can decrypt it. The
encryption of the payload is cryptographically tied to the credentials of the
authorized users.

Authorized persons can delegate their credentials to the server for a period of
time. The server can decrypt any previously-encrypted payloads as long as the
appropriate number of people have delegated their credentials to the server.

This architecture allows Red October to act as a convenient decryption service.
Other systems, including CloudFlare’s build system, can use it for decryption
and users can delegate their credentials to the server via a simple web interface.
All communication with Red October is encrypted with TLS,
ensuring that passwords are not sent in the clear.

`Read More on CloudFlare's Blog
<https://blog.cloudflare.com/red-october-cloudflares-open-source-implementation-of-the-two-man-rule/>`_.

`Browse Red October on Github
<https://github.com/cloudflare/redoctober>`_.

Configuration
=============

Clouder configuration instructions are available at https://clouder.readthedocs.io/

Usage
=====

To use this module, you need to:

#. Create a CFSSL Service in the Clouder Control Panel

Known issues / Roadmap
======================

* Add more Signature Profile options - https://github.com/cloudflare/redoctober/blob/86ecfbe5750ebf05565e4c80104d0a7919792fee/doc/cmd/redoctober.txt#L113

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
