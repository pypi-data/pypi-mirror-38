#!/bin/env/python
#-*- encoding: utf-8 -*-
"""


"""
from __future__ import print_function
from __future__ import division
import numpy as np
import cloudpickle
import subprocess
import threading
import random
import pickle
import shutil
import time
import sys
import os
import re

from clusterweb.interfaces import ssh
from clusterweb.pbs import scripts
from clusterweb.pbs import config
from clusterweb.pbs import qstat
from clusterweb.pbs import qdel
from clusterweb.pbs import qsession

"""
===============================================================================

===============================================================================
"""

class Qsub():

    def __init__(self,target,args,
            n_nodes=config.DEFAULT_NODES,
            n_cores=config.DEFAULT_CORES,
            set_walltime=config.DEFAULT_WALLTIME,
            set_memory=config.DEFAULT_MEMORY,
            set_cpu=config.DEFAULT_CPU,
            wait_time=config.DEFAULT_WAIT_TIME,
            verbose=0):

        self.username = config.USERNAME
        self.ssh = ssh.SSH(self.username)

        self.qdel = qdel.QDel()

        self.target = target
        self.args = args

        self.temp_dir = 'temp_{}{}'.format(
            ''.join(str(time.time()).split('.')),
            random.randint(1000,10000))

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

        self.complete = False

        self.verbose = verbose

        self.job_id = None

        self.time_use = None

        self.user_quit = False

        self.max_time = None

        self.timer = False

        self.flags = ''

        self.update_qstat_on_comparison = True

        self.__type__ = "qsub"


    #--------------------------------------------------------------------------

    def __contains__(self,fnc):
        """Boolean function for whether a function is contained within a job

        :param fnc: function to find
        :type fnc: Python function

        :returns: True or False

        :Example:

        >>> q = Qsub(job,arg)
        >>> job in q
        True
        """
        return id(self.target) == fnc

    #--------------------------------------------------------------------------

    def quit(self):
        if self.qdel.address != self.username:
            self.qdel.login(self.username)

        if self.job_id != None:
            self.qdel.rm(self.job_id)

        self.user_quit = True

    #--------------------------------------------------------------------------

    def __exit__(self):
        self.__del__()


    #--------------------------------------------------------------------------

    def __and__(self,job):
        """Adds two jobs together to create a QSession job

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> sess = Qsub(job,arg)
        >>> q = Qsub(job,arg)
        >>> sess += q

        .. note:: Equivalent to `__add__` or `q1 + q2`
        """
        return self.complete and job.complete

    #--------------------------------------------------------------------------

    def __or__(self,job):
        """Adds two jobs together to create a QSession job

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> sess = Qsub(job,arg)
        >>> q = Qsub(job,arg)
        >>> sess += q

        .. note:: Equivalent to `__add__` or `q1 + q2`
        """
        return self.complete or job.complete

    #--------------------------------------------------------------------------

    def __ior__(self,job):
        """Adds two jobs together to create a QSession job

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> sess = Qsub(job,arg)
        >>> q = Qsub(job,arg)
        >>> sess += q

        .. note:: Equivalent to `__add__` or `q1 + q2`
        """
        return self.__or__(job)

    #--------------------------------------------------------------------------

    def __add__(self,job):
        """Adds two jobs together to create a QSession job

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> sess = q1 + q2
        """
        if job.__type__ == 'qsub':
            sess = qsession.QSession()
            sess.load(self.target,self.args)
            sess.load(job.target,job.args)
            return sess

        elif job.__type__ == 'qsession':
            job.load(self.target,self.args)
            return job 

        else:
            raise TypeError('Incorrect job arg: {}'.format(
                type(job).__name__))

    #--------------------------------------------------------------------------

    def __iadd__(self,job):
        """Adds two jobs together to create a QSession job

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> sess = Qsub(job,arg)
        >>> q = Qsub(job,arg)
        >>> sess += q

        .. note:: Equivalent to `__add__` or `q1 + q2`
        """
        return self.__add__(job)

    #--------------------------------------------------------------------------

    def __mul__(self,n):
        """Creates a QSession of multiple instances of the target function 
        and args.

        :param n: The number of instances
        :type n: int

        :returns: clusterweb.pbs.qsession.QSession

        :Example:
        
        >>> job = lambda z: meaning_to_life(z)
        >>> q = Qsub(job,arg)
        >>> sess = q * 5
        >>> sess.push()
        >>> sess.pull()
        >>> sess.results
        [42,42,42,42,42]

        """
        if not isinstance(n,int):
            raise TypeError("Arg n not type int: {}".format(type(n).__name__))
        if not n > 0:
            raise UserWarning("Arg n must be greater than 0: {}".format(n))
        sess = qsession.QSession()
        for _ in range(n):
            sess.load(self.target,self.args)
        return sess

    #--------------------------------------------------------------------------

    def __lt__(self,job):
        """Returns whether the job's walltime is less than the other job's
        walltime

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 < q2

        .. note:: It will take almost a second to run when 
            `update_qstat_on_comparison` is True since it checks and parses 
            qstat -f. To make this run faster based on a previous qstat 
            update, set `update_qstat_on_comparison` to False.

        """
        if not self.submitted:
            raise UserWarning("Job not submitted yet")

        if self.update_qstat_on_comparison:
            self.update_qstat()
            job.update_qstat()

        if not 'resources_used_walltime' in self.__dict__:
            pass # FIX
        else:           
            return self.resources_used_walltime < job.resources_used_walltime

    #--------------------------------------------------------------------------

    def __le__(self,job):
        """Returns whether the job's walltime is less than the other job's
        walltime

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 <= q2
        
        .. note:: It will take almost a second to run when 
            `update_qstat_on_comparison` is True since it checks and parses 
            qstat -f. To make this run faster based on a previous qstat 
            update, set `update_qstat_on_comparison` to False.

        """
        if not self.submitted:
            raise UserWarning("Job not submitted yet")

        if self.update_qstat_on_comparison:
            self.update_qstat()
            job.update_qstat()

        if not 'resources_used_walltime' in self.__dict__:
            pass # FIX
        else:           
            return self.resources_used_walltime <= job.resources_used_walltime

    #--------------------------------------------------------------------------

    def __gt__(self,job):
        """Returns whether the job's walltime is greater than the 
        other job's walltime

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 > q2

        .. note:: It will take almost a second to run when 
            `update_qstat_on_comparison` is True since it checks and parses 
            qstat -f. To make this run faster based on a previous qstat 
            update, set `update_qstat_on_comparison` to False.
        
        """
        if not self.submitted:
            raise UserWarning("Job not submitted yet")

        if self.update_qstat_on_comparison:
            self.update_qstat()
            job.update_qstat()

        if not 'resources_used_walltime' in self.__dict__:
            pass # FIX
        else:           
            return self.resources_used_walltime > job.resources_used_walltime

    #--------------------------------------------------------------------------

    def __ge__(self,job):
        """Returns whether the job's walltime is greater than or equal to the 
        other job's walltime

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 >= q2

        .. note:: It will take almost a second to run when 
            `update_qstat_on_comparison` is True since it checks and parses 
            qstat -f. To make this run faster based on a previous qstat 
            update, set `update_qstat_on_comparison` to False.
        
        """
        if not self.submitted:
            raise UserWarning("Job not submitted yet")

        if self.update_qstat_on_comparison:
            self.update_qstat()
            job.update_qstat()

        if not 'resources_used_walltime' in self.__dict__:
            pass # FIX
        else:           
            return self.resources_used_walltime >= job.resources_used_walltime


    #--------------------------------------------------------------------------

    def __eq__(self,job):
        """Returns whether the job's walltime is equal to the 
        other job's walltime

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 == q2

        .. note:: It will take almost a second to run when 
            `update_qstat_on_comparison` is True since it checks and parses 
            qstat -f. To make this run faster based on a previous qstat 
            update, set `update_qstat_on_comparison` to False.
        
        """
        return id(self.target) == id(job.target)

    #--------------------------------------------------------------------------

    def is_(self,job):
        """Returns whether the job's walltime is equal to the 
        other job's walltime

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 is q2
        True

        .. note:: Equivalent to `__eq_-`
        
        """
        return id(self.target) == id(job.target)

    #--------------------------------------------------------------------------

    def is_not(self,job):
        """Returns whether the job's function is not equal to the function of 
        another job.

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 is not q2
        False
        >>> q3 = Qsub(job2,arg)
        >>> q1 is not q3
        True

        .. note:: Equivalent to `__ne__`
        """
        return id(self.target) != id(job.target)

    #--------------------------------------------------------------------------

    def __ne__(self,job):
        """Returns whether the job's function is not equal to the function of 
        another job.

        :param job: Job to be compared to
        :type job: clusterweb.pbs.qsub.Qsub

        :returns: True or False

        :Example:

        >>> q1 = Qsub(job,arg)
        >>> q2 = Qsub(job,arg)
        >>> q1 == q2
        False
        >>> q3 = Qsub(job2,arg)
        >>> q1 != q3
        True
        """
        return id(self.target) != id(job.target)

    #--------------------------------------------------------------------------

    def update_qstat(self):
        """Get the current data about a job from qstat

        :param job_id: The job id given by qsub
        :type job_id: str

        :param user: The user id
        :type user: str

        :returns: None

        .. note:: Must be run after a job is submitted as qstat will only 
            report data if it is in the queue
        """
        if self.complete:
            # Job no longer exists
            pass

        if not self.submitted:
            raise UserWarning("Job not submitted")

        data = qstat.Qstat()

        if self.username != config.USERNAME:
            data.login(self.username)

        job = data.process_id(self.job_id)

        if job != None:
            for n in job.__dict__:
                v = job.__dict__[n]
                self.__dict__[n] = v
        else:
            # Job no longer exists
            pass

    #--------------------------------------------------------------------------

    def login(self,address):
        """Creates an SSH interface object with the address specified 

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        .. note:: The default address is contained in 
            clusterweb/pbs/username.txt and can be adjusted with 
            `change_default_address`

        """
        if not isinstance(address,str):
            raise UserWarning("Invalid address arg type: {}".format(
                type(address).__name__))
        self.ssh_interface = ssh.SSH(address)
        self.username = address

    #--------------------------------------------------------------------------

    def change_default_address(self,address):
        """Change the default SSH address stored in username.txt which Qsub
        automatically sets itself to unless `qsub.login` is used.

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.change_default_address('192.168.1.24')

        """
        if not isinstance(address,str):
            raise UserWarning("Invalid address arg type: {}".format(
                type(address).__name__))
        with open(os.path.join(os.path.dirname(
                os.path.abspath(__file__)),'username.txt'),'w') as f:
            f.write(address)

    #--------------------------------------------------------------------------

    def generate_qsub_script(self):
        """Return the PBS submission script from the specified resource
        allocations.

        :returns: None
        """
        return scripts.qscript.format(
            self.n_nodes,
            self.n_cores,
            self.set_walltime,
            self.set_memory,
            self.set_cpu,
            'python {}/pyscript.py'.format(self.temp_dir))

    #--------------------------------------------------------------------------

    def allocate_walltime(self,walltime):
        """Sets the amount of walltime

        Will raise exception if str argument is not in the form hr:min:sec

        :param walltime: amount of walltime in seconds
        :type walltime: str, int, float

        :returns: None

        :Example:

        >>> q.allocate_walltime('0:05:00') # Five minutes
        >>> q.allocate_walltime(600) # Ten minutes
        >>> q.allocate_walltime(599.6) # Rounds to ten minutes

        .. note:: The walltime configuration can be adjusted by admins in 
            `clusterweb/pbs/config.py`.

        .. warning:: If users adjust `clusterweb/pbs/config.py` to
            settings not authorized by cluster admins, it will raise
            errors on the cluster and the job will not be submitted.
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

    def allocate_memory(self,memory):
        """Set the amount of memory for the job

        :param memory: string in format '10GB' or '500MB' or number of MB
        :type memory: str, int, float

        Example:
        >>> # Use three GB
        >>> qsub_job.allocate_memory('3GB')
        >>> qsub_job.allocate_memory(3000)
        >>> 
        >>> qsub_job.start()

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

    #--------------------------------------------------------------------------

    def allocate_cores(self,n_cores):
        if not isinstance(n_cores,(float,int)):
            raise UserWarning("Invalid type for arg n_cores: {}".format(
                type(n_cores).__name__))
        n_cores = int(n_cores)
        if n_cores <= 0:
            n_cores = 1
        self.n_cores = n_cores

    #--------------------------------------------------------------------------

    def allocate_nodes(self,n_nodes):
        """Sets the number of nodes to a job submission.
        """
        if not isinstance(n_nodes,(float,int,str)):
            raise Exception("Invalid type for arg n_nodes: {}".format(
                type(n_nodes).__name__))

        if isinstance(n_nodes,str):
            try:
                int(n_nodes)
            except:
                raise Exception("Invalid arg n_nodes: {}".format(n_nodes))

        n_nodes = int(n_nodes)

        if n_nodes <= config.MIN_NODES-1:
            n_nodes = 1
            print("Warning: {} lower than {} node, setting to {}".format(
                n_nodes,config.MIN_NODES,config.MIN_NODES),
                file=sys.stderr)

        elif n_nodes > config.MAX_NODES:
            n_nodes = config.MAX_NODES
            print("Warning: {} exceeds limit of {} nodes, setting to {}".format(
                n_nodes,config.MAX_NODES,config.MAX_NODES),
                file=sys.stderr)

        self.n_nodes = n_nodes

    #--------------------------------------------------------------------------

    def set_priority(self,priority):
        """Set the priority of the job, default is 0

        :param priority: The level of priority
        :type priority: int (-1024,1023)

        :returns: None

        :Example:

        >>> q1 = Qsub(important_job,args)
        >>> q1.set_priority(1000)
        >>> 
        >>> q2 = Qsub(not_so_important_job,args)
        >>> q2.set_priority(-100)
        """

        if isinstance(self.priority,int):
            if priority < 1023 and priority > -1024:
                self.flags += ' -p {} '.format(self.priority)
            else:
                raise UserWarning("Invalid priority arg for range \
                    (-1024,1023): {}".format(priority))
        else:
            raise TypeError("Invalid priority arg type: {}".format(
                type(priority).___name__))

    #--------------------------------------------------------------------------

    def create_timer(self,n_seconds):
        """Create a timer that terminates the job if it exceeds the max time

        :param n_seconds: The number of seconds for the timer, (n_seconds) > 0
        :type n_seconds: int, float 

        :returns: None

        :Example:

        >>> q = Qsub(job,args)
        >>> q.create_timer(600)

        .. note:: This is a timer for the time since it was submitted,
            not for walltime.
        """
        if not isinstance(n_seconds,int):
            raise TypeError("Invalid n_seconds arg type: {}".format(
                type(n_seconds).__name__))
        if n_seconds < 1:
            raise UserWarning("n_seconds cannot be less than 1: {}".format(
                n_seconds))

        self.timer = True
        self.max_time = n_seconds

    #--------------------------------------------------------------------------

    def cleanup(self):
        """Remove the temprorary folder that holds the compressed data and
        scripts that are sent to the cluster

        :returns: None

        :Example:

        >>> q = Qsub(job,args)
        >>> q.cleanup()

        .. note:: This is automatically run and is not required to be run
             by the user.
        """
        self.ssh.send_command('rm -rf {}'.format(self.temp_dir))
        self.ssh.send_command('rm qsub_script.*{}'.format(
            self.job_id.split('.')[0]))
        shutil.rmtree(self.temp_dir)

    #--------------------------------------------------------------------------

    def push(self):
        """Push the job to the remote cluster

        Serializes the function, arguments, and send the generated scripts
        to the server. It automatically sends the PBS commands so this is 
        the only command required to start the job on the cluster.

        Resource allocation must occur before `push` is called.

        :returns: None

        :Example:

        >>> q = Qsub(job,args)
        >>> q.push()
        """

        self.fnc = cloudpickle.dumps(self.target)
        self.args = pickle.dumps(self.args)

        os.mkdir(self.temp_dir)

        with open(os.path.join(self.temp_dir,'fnc.pkl'),'wb') as f:
            f.write(self.fnc)

        with open(os.path.join(self.temp_dir,'args.pkl'),'wb') as f:
            f.write(self.args)

        with open(os.path.join(self.temp_dir,'pyscript.py'),'w') as f:
            f.write(scripts.pyscript.format(sys.version_info.major,self.temp_dir))

        with open(os.path.join(self.temp_dir,'qscript'),'w') as f:
            f.write(self.generate_qsub_script())

        self.ssh.send_folder(self.temp_dir,self.temp_dir)


        [self.job_id] = self.ssh.send_command('qsub {} {}'.format(self.flags,
            os.path.join(self.temp_dir,'qscript')))
        
        # print(self.ssh.send_command('ls'))

        if self.timer == True:
            self.start_time = time.time()

        self.job_id = self.job_id.split('.')[0]

        self.submitted = True

    #--------------------------------------------------------------------------

    def fetch_result(self):
        """Get the result of the job from the remote cluster synchronously
        with the main script.

        Will continually check to see if the result file exists given a 
        time interval `self.wait_time`. If it is a longer job, increase the 
        wait time so as to not needless be calling SSH too many times.

        :returns: None

        :Example:

        >>> q = Qsub(job,args)
        >>> q.push()
        >>> q.fetch_result()

        .. note:: This is equivalent to `pull(thread=False)`
        """

        result_path = os.path.join(self.temp_dir,'result.pkl')
        finished = False

        while True:
            if self.timer:
                if time.time()-self.start_time >= self.max_time:
                    self.quit()
                    self.user_quit = True
            if self.user_quit:
                break
            result = subprocess.check_output(
                'ssh colfax [ -f {} ] && echo "1" || echo "0"'.format(
                    result_path),stderr=subprocess.STDOUT,shell=True)
            if int(result[-2]) == 49:
                finished = True
                break
            else:
                time.sleep(self.wait_time)

        if finished:
            self.ssh.recieve_file(result_path,result_path)
            if os.path.getsize(result_path) > 1:
                with open(result_path,'rb') as f:
                    self.result = pickle.loads(f.read())
            else:
                self.result = 'Blank result file: {}'.format(result_path)

        elif (not finished) and self.timer:
            self.result = 'Timer exceeded'

        self.cleanup()
        self.complete = True
        
        
    #--------------------------------------------------------------------------

    def pull(self,thread=True,daemon=False):
        """Get the result of the job from the remote cluster asynchronously
        with the main script.

        Will continually check to see if the result file exists given a 
        time interval `self.wait_time`. If it is a longer job, increase the 
        wait time so as to not needless be calling SSH too many times.

        :returns: None

        :Example:

        >>> q = Qsub(job,args)
        >>> q.push()
        >>> q.fetch_result()
        """
        if thread:
            result_thread = threading.Thread(target=self.fetch_result,args=())
            result_thread.daemon = daemon
            result_thread.start()
        else:
            self.fetch_result()










