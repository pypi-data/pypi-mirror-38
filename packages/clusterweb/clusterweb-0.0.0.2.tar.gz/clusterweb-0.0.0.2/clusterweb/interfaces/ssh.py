#!/bin/env/python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
import numpy as np
import subprocess
import threading
import random
import time
import sys
import os
import re

from clusterweb.pbs.cluster_functions import *

"""
===============================================================================

===============================================================================
"""

class SSH():

    def __init__(self,host):
        self.port=None
        self.set_address(host,self.port)

    #--------------------------------------------------------------------------

    @classmethod
    def change_default(self,address,verify=True):
        if verify:
            ssh_config_path = os.path.join(os.path.expanduser('~'),
                '.ssh/config')

            if not os.path.exists(ssh_config_path):
                raise FileNotFoundError("SSH Config file not found: {}".format(
                    ssh_config_path))

            valid = False
            with open(ssh_config_path,'r') as f:
                ssh_config = f.read()

                for n in ssh_config.split('\n'):
                    n = n.split(' ')

                    if n[0] == 'Host':
                        if n[1] == address:
                            valid = True
            if not valid:
                raise UserWarning("{} not found in ssh config: {}".format(
                    address,ssh_config_path))

        config_file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))),'pbs/username.txt')

        if os.path.exists(config_file):
            with open(config_file,'r') as f:
                address_book = f.read()
        else:
            address_book = ''

        with open(config_file,'w') as f:
            if address_book != '':
                address_book = '\n'.join([n for n in address_book.split('\n') 
                    if n != address])

            f.write('{}\n{}'.format(address,address_book))


    #--------------------------------------------------------------------------

    def ssh_exists(self):
        """
        A method's docstring with parameters and return value.
        
        Use all the cool Sphinx capabilities in this description, e.g. to give
        usage examples ...
        
        :Example:

        >>> another_class.foo('', AClass())        
        
        :param arg1: first argument
        :type arg1: string
        :param arg2: second argument
        :type arg2: :class:`module.AClass`
        :return: something
        :rtype: string
        :raises: TypeError
        """
        try:
            subprocess.Popen(["ssh"],shell=False,
                stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False



    #--------------------------------------------------------------------------

    def set_address(self,host,port):
        """
        A method's docstring with parameters and return value.
        
        Use all the cool Sphinx capabilities in this description, e.g. to give
        usage examples ...
        
        :Example:

        >>> another_class.foo('', AClass())        
        
        :param arg1: first argument
        :type arg1: string
        :param arg2: second argument
        :type arg2: :class:`module.AClass`
        :return: something
        :rtype: string
        :raises: TypeError
        """
        #if self.legal_address(host,port):  # FIX!!!
        self.host = host
        self.port = port
        #else:
        #    raise Exception("Invalid ssh argument: {}:{}".format(host,port))


    #--------------------------------------------------------------------------

    def legal_address(self,host,port):
        """ 

        """
        if not (re.match(r'^((\d){1,3}.){3}(\d{1,3})$',host,re.M|re.I)):
            if not (host == 'localhost'):
                return False

        if port != None:
            if not isinstance(port,int):
                return False

            if not (port >= 0 and port < 65535):
                return False

        return True


    #--------------------------------------------------------------------------

    def send_command(self,command):
        """ 

        """
        if not isinstance(command,str):
            raise Exception("Invalid command arg type: {}".format(
                type(command).__name__))

        if 'python ' in command:
            subprocess.call(['ssh',
                self.host,
                'python',command.split(' ')[1]],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE) # FIX!!!
            result = None

        else:

            ssh_output = subprocess.Popen(["ssh","%s"%self.host,command],
                   shell=False,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)

            result = ssh_output.stdout.readlines()
            for i,n in enumerate(result):
                result[i] = n.decode()[:-1]

        return result

    #--------------------------------------------------------------------------

    def send_file(self,origin_path,destination_path):
        """ 

        """
        if not os.path.exists(origin_path):
            raise Exception("Invalid origin_path: {}".format(
                origin_path))

        scp = subprocess.Popen(["scp","{}".format(origin_path),
            "{}:{}".format(self.host,destination_path)],
               shell=False,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
        result = scp.stdout.readlines()

    #--------------------------------------------------------------------------

    def send_folder(self,origin_dir,destination_dir):
        """ 

        """
        if not os.path.exists(origin_dir):
            raise Exception("Invalid origin_path: {}".format(
                origin_path))

        if not os.path.isdir(origin_dir):
            raise Exception("Directory arg invalid: {}".format(
                origin_reipath))

        scp = subprocess.Popen(["scp",'-r',"{}".format(origin_dir),
            "{}:{}".format(self.host,destination_dir)],
               shell=False,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)

        result = scp.stdout.readlines()

    #--------------------------------------------------------------------------

    def recieve_file(self,origin_path,destination_path):

        scp = subprocess.Popen(["scp","{}:{}".format(self.host,
            origin_path),"{}".format(destination_path)],
               shell=False,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
        result = scp.stdout.readlines()

