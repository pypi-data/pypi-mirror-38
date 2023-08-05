#!/bin/env/python
#-*- encoding: utf-8 -*-
"""

"""
from __future__ import print_function
from __future__ import division
import numpy as np

from clusterweb.interfaces import ssh
from clusterweb.pbs import config
from clusterweb.pbs import qstat


class QDel():

    def __init__(self):
        self.address = config.USERNAME
        self.ssh = ssh.SSH(self.address)
        self.qstat = qstat.Qstat()

    #--------------------------------------------------------------------------

    def login(self,address):
        """Creates an SSH interface object with the address specified 

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        if not isinstance(address,str):
            raise UserWarning("Invalid address arg type: {}".format(
                type(address).__name__))
        self.ssh = ssh.SSH(address)
        self.username = address

    #--------------------------------------------------------------------------

    def rm_all(self):
        """Creates an SSH interface object with the address specified 

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        output = []
        jobs = self.qstat.process_simple_qstat()
        if len(jobs):
            job_ids = [j.job_id for j in jobs]
            for n in job_ids:
                output.append(self.ssh.send_command('qdel {}'.format(n)))
        return output

    #--------------------------------------------------------------------------

    def rm(self,job_id,flags=[]):
        """Creates an SSH interface object with the address specified 

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        flags = ' '.join(list(map(str,flags)))
        return self.ssh.send_command('qdel {} {}'.format(flags,job_id))

    #--------------------------------------------------------------------------

    def rm_a(self,job_id):
        """Request the job(s) be deleted asynchronously, which for a Running 
        job means that the reply will return before the MOM is requested to 
        delete the job.

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        return self.ssh.send_command('qdel -a {}'.format(flags,job_id))

    #--------------------------------------------------------------------------

    def purge(self,job_id):
        """Forcibly  purge  the  job  from the server.  This should only be 
        used if a running job will not exit because its allocated  nodes are 
        unreachable. The admin should make every attempt at resolving the problem 
        on the nodes. If a job's mother superior recovers after purging the job,
        any epilogue scripts may still run.  This option is only available 
        to a batch operator or the batch administrator.

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        return self.ssh.send_command('qdel -p {}'.format(job_id))

    #--------------------------------------------------------------------------

    def clean(self):
        pass
        

    #--------------------------------------------------------------------------

    def rm_message(self,job_id,message):
        """Creates an SSH interface object with the address specified 

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        return self.ssh.send_command('qdel -m "{}" {}'.format(message,job_id))

    #--------------------------------------------------------------------------

    def rm_delay(self,job_id,delay):
        """Specify the delay between the sending of the SIGTERM and SIGKILL 
        signals. The argument delay specifies a unsigned integer number of 
        seconds.

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        try:
            int(delay)
        except:
            raise UserWarning("Invalid delay arg: {}".format(delay))
        return self.ssh.send_command('qdel -W {} {}'.format(delay,job_id))

    #--------------------------------------------------------------------------

    def rm_range(self,id_range):
        """The  array_range argument is an integer id or a range of integers. 
        Multiple ids or id ranges can be combined in a comma delimted list 
        (examples:   -t  1-100  or  -t 1,10,50-100). 

        The command acts on the array (or  specified range of the array) 
        just as it would on an individual job.

        :param address: Address or name for ssh to
        :type address: str

        :returns: None

        :Example:

        >>> q = Qsub(job,arg)
        >>> q.login('192.168.1.42')

        """
        #TODO: User error parsing
        return self.ssh.send_command('qdel -t {} {}'.format(id_range,job_id))








