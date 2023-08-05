#!/bin/env/python3
#-*- encdoing: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
import collections
import functools
import time
import sys
import os

from clusterweb.interfaces import ssh

__author__ = "Stephen Offer"

"""
===============================================================================
Memorized Decorator for Reducing Run-time
===============================================================================
"""

class memorized(object):
    
    def __init__(self, func):
        """Decorator. Caches a function's return value each time it is called.
        
        If called later with the same arguments, the cached value is returned
        (not reevaluated).
        """
        self.func = func
        self.cache = {}

    #--------------------------------------------------------------------------

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            return self.func(*args)

        if args in self.cache:
            return self.cache[args]

        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    #--------------------------------------------------------------------------

    def __repr__(self):
        """Return the function's docstring"""
        return self.func.__doc__

    #--------------------------------------------------------------------------

    def __get__(self, obj, objtype):
        """Support instance methods"""
        return functools.partial(self.__call__, obj)


"""
===============================================================================

===============================================================================
"""

class DevCloudFunctions():

    def __init__(self):
        self.devcloud_id = 'd229301155e240db8075e52dae00d918'

    #--------------------------------------------------------------------------

    @memorized
    def can_access_devcloud(self,key):
        """
        Boolean function for searching for ssh key for devcloud
        
        Output: [True,False]
        """
        ssh_interface    = ssh.SSH(key)
        output = ssh_interface.send_command('cat /etc/machine-id')[0]

        return True if output == self.devcloud_id else False

    #--------------------------------------------------------------------------

    @memorized
    def on_devcloud(self):
        """
        Boolean function for running on devcloud 
        
        Output: [True,False]
        """
        machine_id = subprocess.check_output(
            ['cat','/etc/machine-id']).decode()[:-1]

        return True if machine_id == self.devcloud_id else False

"""
===============================================================================

===============================================================================
"""
