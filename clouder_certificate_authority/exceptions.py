# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import requests


class CFSSLException(EnvironmentError):
    """ This exception is raised from errors in the CFSSL Library. """


class CFSSLRemoteException(CFSSLException):
    """ This exception is raised to indicate issues returned from API. """
