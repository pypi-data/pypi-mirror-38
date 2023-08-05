#!/bin/env/python3
#-*- encdoing: utf-8 -*-
"""




"""
from __future__ import print_function
from __future__ import division
import numpy as np
import cloudpickle
import subprocess
import threading
import datetime
import pickle
import random
import shutil
import time
import sys
import os
import re

from clusterweb.interfaces import ssh
from clusterweb.pbs import scripts
from clusterweb.pbs import config

__author__ = "Stephen Offer"

"""
===============================================================================

===============================================================================
"""

class QSession():

    def __init__(self,
            n_nodes=config.DEFAULT_NODES,
            n_cores=config.DEFAULT_CORES,
            set_walltime=config.DEFAULT_WALLTIME,
            set_memory=config.DEFAULT_MEMORY,
            set_cpu=config.DEFAULT_CPU,
            wait_time=config.DEFAULT_WAIT_TIME,
            verbose=0):
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
        """
        Multi-job control of qsub submissions

        Multi-job Usage:
            >> with devcloud.Session() as sess:
            >>     sess.load(job1)
            >>     sess.load(job2)
            >>     sess.load(job3)
            >>     sess.run()
            >>     [output1,output2,output3] = sess.output
        """
        self.jobs = []
        self.args = []

        self.output = []

        self.ssh = ssh.SSH(config.USERNAME)

        self.temp_dir = 'temp_{}{}'.format(
            ''.join(str(time.time()).split('.')),
            random.randint(10000,100000))

        # FIX: Allocate resource functions
        self.n_nodes        = n_nodes
        # Qsub script placeholder for number of cores
        self.n_cores        = n_cores
        # Qsub script placeholder for the walltime allocated
        self.set_walltime   = set_walltime
        self.allocate_walltime(self.set_walltime)

        # Qsub script placeholder for memory allocated
        self.set_memory     = set_memory
        # Qsub script placeholder for cpu time allocated
        self.set_cpu        = set_cpu

        self.wait_time = wait_time

        self.all_complete = False

        self.verbose = verbose

        self.__type__ = "qsession"

    #--------------------------------------------------------------------------

    def __len__(self):
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
        # Return 
        pass

    #--------------------------------------------------------------------------

    def __mul__(self,value):
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
        # Return multiple qsub submissions job objects
        pass

    #--------------------------------------------------------------------------

    def __eq__(self,value):
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
        """
        Return true if both jobs are for the same function else false
        
        Input
        """
        pass

    #--------------------------------------------------------------------------

    def __ne__(self,value):
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
        """Return false if both jobs are the same function else true"""
        pass

    #--------------------------------------------------------------------------

    def __ge__(self,value):
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
        """ Return True if walltime is greater than or equal to the wall time 
        of job object or integer or float else return False
        

        """
        pass

    #--------------------------------------------------------------------------

    def __getitem__(self,key):
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
        """Return the item by the index key if a multitask job object"""
        pass

    #--------------------------------------------------------------------------

    def __gt__(self,value):
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
        """ Return True if walltime is greater than wall time of job object or 
        integer or float else return False
        

        """
        pass


    #--------------------------------------------------------------------------

    def __le__(self,value):
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
        """ Return True if walltime is less than or equal to the wall time of 
        job object or integer or float else return False
        

        """
        pass

    #--------------------------------------------------------------------------

    def __lt__(self,value):
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
        """ Return True if walltime is less than wall time of job object or 
        integer or float else return False
        

        """
        pass

    #--------------------------------------------------------------------------

    def index(self,value):
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
        """Return the index of the job ids if a multijob object"""
        pass


    #--------------------------------------------------------------------------

    def __del__(self):
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
        pass

    #--------------------------------------------------------------------------

    def __enter__(self):
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
        return self

    #--------------------------------------------------------------------------

    def __exit__(self, type, value, traceback):
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
        #Exception handling here
        return

    #--------------------------------------------------------------------------

    def allocate_nodes(self,n_nodes):
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
        """Set the number of nodes for a job
        Input: n number of nodes
            Type: int, float

        Usage:
            >> # Use two nodes
            >> qsub_job.allocate_nodes(2)
            >> qsub_job.start()
        """
        if not isinstance(n_nodes,(float,int)):
            raise UserWarning("Invalid type for arg n_nodes: {}".format(
                type(n_nodes).__name__))

        n_nodes = int(n_nodes)
        if n_nodes <= 0:
            n_nodes = 1

        self.n_nodes = n_nodes

    #--------------------------------------------------------------------------

    def allocate_cpu_time(self,cpu_time):
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
        if isinstance(cpu_time,(int,float)):
            cpu_time = str(datetime.timedelta(seconds=cpu_time))

        def intable(z):
            try:
                int(z)
                return True 
            except:
                return False

        if isinstance(cpu_time,str):
            split_exp = cpu_time.split(':')
            if np.all(list(map(intable,split_exp))) and len(split_exp) == 3:
                # TODO: Add config check
                pass
            else:
                raise Exception("Invalid CPU time arg: {}".format(cpu_time))

        c = [3600,60,1]
        self.set_cpu = sum([int(A)*int(B) for A,B in zip(
            cpu_time.split(':'),c)])

        self.set_cpu = cpu_time

    #--------------------------------------------------------------------------

    def allocate_walltime(self,walltime):
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
        if isinstance(walltime,(int,float)):
            walltime = str(datetime.timedelta(seconds=walltime))

        def intable(z):
            try:
                int(z)
                return True 
            except:
                return False

        if isinstance(walltime,str):
            split_exp = walltime.split(':')
            if np.all(list(map(intable,split_exp))) and len(split_exp) == 3:
                # TODO: Add config check
                pass
            else:
                raise Exception("Invalid walltime arg: {}".format(walltime))

        c = [3600,60,1]
        self.total_walltime = sum([int(A)*int(B) for A,B in zip(
            walltime.split(':'),c)])

        self.set_walltime = walltime

    #--------------------------------------------------------------------------

    def allocate_cores(self,n_cores):
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
        """Set the number of cores for a job
        Input: n number of cores
            Type: int, float

        Usage:
            >> # Use two cores
            >> qsub_job.allocate_cores(2)
            >> qsub_job.start()
        """
        if not isinstance(n_cores,(float,int)):
            raise UserWarning("Invalid type for arg n_cores: {}".format(
                type(n_cores).__name__))
        n_cores = int(n_cores)
        if n_cores <= 0:
            n_cores = 1
        self.n_cores = n_cores

    #--------------------------------------------------------------------------

    def allocate_memory(self,memory):
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
        """Set the amount of memory for the job
        Input: string in format '10GB' or '500MB'
            Type: str

        Usage:
            >> # Use three GB
            >> qsub_job.allocate_memory('3GB')
            >> qsub_job.start()
        """
        if isinstance(memory,int):
            if memory > config.MAX_MEMORY:
                raise ValueError("Max memory arg {} exceeded: {}".format(
                    config.MAX_MEMORY,memory))

            if memory < config.MIN_MEMORY:
                raise ValueError("Lower than min memory {} arg: {}".format(
                    config.MIN_MEMORY,memory))

            memory = "{}MB".format(memory)

        elif isinstance(memory,str):
            valid = True

            if memory.upper().endswith(('GB','MB')):
                try:

                    n = int(memory[:-2])

                    if 'G' in memory.upper():
                        if n > int(config.MAX_MEMORY/1000):
                            valid = False

                        elif n < int(config.MIN_MEMORY/1000):
                            valid = False

                    elif 'M' in memory.upper():
                        if n > config.MAX_MEMORY:
                            valid = False

                        elif n < config.MIN_MEMORY:
                            valid = False

                except Exception as e:
                    valid = False
            else:
                valid = False

            if not valid:
                raise Exception("Invalid memory arg: {}".format(memory))
        else:
            raise ValueError("Invalid memory arg type: {}".format(
                type(memory).__name__))

        self.set_memory = memory
        self.job.set_memory = memory

    #--------------------------------------------------------------------------

    def generate_qsub_script(self):
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
        """Generate a qsub submission bash script"""
        return scripts.qscript.format(
            self.n_nodes,
            self.n_cores,
            self.set_walltime,
            self.set_memory,
            self.set_cpu,
            'python {}/pyscript.py'.format(self.temp_dir))

    #--------------------------------------------------------------------------

    def data_dump(self,data,path):
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
        if not isinstance(path,str):
            raise TypeError("Invalid path arg type: {}".format(
                type(path).__name__))

        with open(path,'wb') as f:
            dill.dump(data,f)        


    #--------------------------------------------------------------------------

    def write_script(self,script,path,mode='w'):
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
        """Writes a string to a file specified

        Input: 
                script: str of python script
                path:   str of path for the output file
                mode:   char of open mode

                    `w'   Truncate file to zero length or create text file 
                    for writing. The stream is positioned at the beginning 
                    of the file.

                    `w+'  Open for reading and writing. The file is created 
                    if it does not exist, otherwise it is truncated. 
                    The stream is positioned at the beginning of the file.

                    `a`   Open for writing. The file is created if it does 
                    not exist.  The stream is positioned at the end of the 
                    file. Subsequent writes to the file will always end up 
                    at the then current end of file, irrespective of any 
                    intervening fseek(3) or similar.

                    `a+'  Open for reading and writing. The file is created 
                    if it does not exist.  The stream is positioned at the 
                    end of the file.  Subsequent writes to the file will 
                    always end up at the then current end of file, 
                    irrespective of any intervening fseek(3) or similar.
                
        Output: None

        Usage:
            >> q = qsub()
            >> q.write_script("print('hello')","test.py")
        """
        if not mode in ['w','w+','a','a+']:
            raise Exception("Invalid mode arg: {}".format(mode))

        if not isinstance(script,str):
            raise TypeError("Invalid script arg type: {}".format(
                type(script).__name__))

        if not isinstance(path,str):
            raise TypeError("Invalid path arg type: {}".format(
                type(path).__name__))

        with open(path,mode) as f:
            f.write(script)

    #--------------------------------------------------------------------------

    def load(self,target=None,args=None):
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
        self.jobs.append(target)
        self.args.append(args)

    #--------------------------------------------------------------------------

    def push(self):
        os.mkdir(self.temp_dir)

        for i,fnc in enumerate(self.jobs):
            with open(os.path.join(self.temp_dir,'fnc{}.pkl'.format(
                    i)),'wb') as f:
                f.write(cloudpickle.dumps(fnc))

        for i,arg in enumerate(self.args):      
            with open(os.path.join(self.temp_dir,'args{}.pkl'.format(
                    i)),'wb') as f:
                f.write(pickle.dumps(arg))

        with open(os.path.join(self.temp_dir,'pyscript.py'),'w') as f:
            f.write(scripts.session_pyscript.format(
                sys.version_info.major,self.temp_dir))

        with open(os.path.join(self.temp_dir,'qscript'),'w') as f:
            f.write(self.generate_qsub_script())

        self.ssh.send_folder(self.temp_dir,self.temp_dir)

        [self.job_id] = self.ssh.send_command('qsub {}'.format(os.path.join(
            self.temp_dir,'qscript')))

    #--------------------------------------------------------------------------

    def fetch_result(self):

        self.results = [None for _ in self.jobs]
        self.complete = [False for _ in self.jobs]

        result_index = list(map(str,list(range(len(self.jobs)))))

        while True:

            for i in result_index:
                local_result_file = "{}/res{}.pkl".format(self.temp_dir,i)
                path = "{}/res{}.pkl".format(self.temp_dir,i)

                result = subprocess.check_output(
                    'ssh colfax [ -f {} ] && echo "1" || echo "0"'.format(
                        path),stderr=subprocess.STDOUT,shell=True)

                if int(result[-2]) == 49:
                    self.ssh.recieve_file(path,local_result_file)
                    result_index.remove(i)

                    with open(local_result_file,'rb') as f:
                        self.results[int(i)] = dill.load(f)
                        self.complete[int(i)] = True

                    subprocess.call(['rm',local_result_file])

            if not len(result_index):
                break

            time.sleep(self.wait_time)

        self.all_complete = True
        
        self.ssh.send_command('rm -rf {}'.format(self.temp_dir))
        self.ssh.send_command('rm qsub_script.*{}'.format(
            self.job_id.split('.')[0]))
        shutil.rmtree(self.temp_dir)
            
    #--------------------------------------------------------------------------

    def pull(self):
        result_thread = threading.Thread(target=self.fetch_result,args=())
        result_thread.start()


