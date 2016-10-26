# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from threading import Thread


class ThreadMethod(Thread):
    """ It provides an abstract handler to thread methods """

    def __init__(self, method, *args, **kwargs):
        """ It initializes the thread by setting instance vars for run

        Params:
            method: (function) Method to run in thread
            *args: (mixed) Arguments to pass to method
            **kwargs: (mixed) Keyword arguments to pass to method
        """
        self._method = method
        self._args = args
        self._kwargs = kwargs
        super(ThreadMethod, self).__init__()

    def run(self):
        """ It runs the method in a thread & assigns return to self.result """
        self.result = self._method(*self._args, **self.kwargs)
