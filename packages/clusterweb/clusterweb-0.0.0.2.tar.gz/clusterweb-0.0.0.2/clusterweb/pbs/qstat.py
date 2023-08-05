 #!/bin/env/python3
#-*- encdoing: utf-8 -*-
"""


"""
from __future__ import print_function
from __future__ import division
import numpy as np
import calendar
import datetime
import time
import sys
import os

from clusterweb.interfaces import ssh
from clusterweb.pbs import config

__author__ = "Stephen Offer"

"""
===============================================================================

===============================================================================
"""

exchange = {
    "Job Id"                        :   "job_id",
    "Job_Owner"                     :   "user",
    "Job_Name"                      :   "name",
    "job_state"                     :   "job_state",
    "queue"                         :   "queue",
    "resources_used.cput"           :   "resources_used_cput",  
    "resources_used.energy_used"    :   "resources_used_energy_used",  
    "resources_used.mem"            :   "resources_used_mem",  
    "resources_used.vmem"           :   "resources_used_vmem",  
    "resources_used.walltime"       :   "resources_used_walltime",     
    "server"                        :   "server",  
    "Checkpoint"                    :   "checkpoint",  
    "ctime"                         :   "ctime",
    "Error_Path"                    :   "error_path",  
    "exec_host"                     :   "exec_host",  
    "Hold_Types"                    :   "hold_types",
    "Join_Path"                     :   "join_path",
    "Keep_Files"                    :   "keep_files",   
    "Mail_Points"                   :   "mail_points",  
    "mtime"                         :   "mtime",   
    "Output_Path"                   :   "output_path",  
    "Priority"                      :   "priority", 
    "qtime"                         :   "qtime",
    "Rerunable"                     :   "rerunable", 
    "Resource_List.cput"            :   "resource_list_cput",
    "Resource_List.mem"             :   "resource_list_mem", 
    "Resource_List.nodect"          :   "resource_list_nodect", 
    "Resource_List.nodes"           :   "resource_list_nodes", 
    "Resource_List.vmem"            :   "resource_list_vmem",
    "Resource_List.walltime"        :   "resource_list_walltime", 
    "session_id"                    :   "session_id",   
    "PBS_O_QUEUE"                   :   "PBS_O_QUEUE", 
    "PBS_O_HOME"                    :   "PBS_O_HOME", 
    "PBS_O_LOGNAME"                 :   "PBS_O_LOGNAME",
    "PBS_O_PATH"                    :   "PBS_O_PATH",  
    "PBS_O_MAIL"                    :   "PBS_O_MAIL",   
    "PBS_O_SHELL"                   :   "PBS_O_MAIL",   
    "PBS_O_LANG"                    :   "PBS_O_LANG",  
    "PBS_O_SUBMIT_FILTER"           :   "PBS_O_SUBMIT_FILTER",  
    "PBS_O_WORKDIR"                 :   "PBS_O_WORKDIR",
    "PBS_O_HOST"                    :   "PBS_O_HOST",  
    "PBS_O_SERVER"                  :   "PBS_O_SERVER",   
    "euser"                         :   "euser",
    "egroup"                        :   "egroup",
    "queue_type"                    :   "queue_type",  
    "etime"                         :   "etime",
    "submit_args"                   :   "submit_hostargs",
    "start_time"                    :   "start_time",
    "Walltime.Remaining"            :   "walltime_remaining",  
    "start_count"                   :   "start_count",  
    "fault_tolerant"                :   "fault_tolerant",  
    "job_radix"                     :   "job_radix", 
    "exit_status"                   :   "exit_status",
    "submit_host"                   :   "submit_host"
}

"""
===============================================================================

===============================================================================
"""

class QstatData(object):

    def __init__(self,job_id=None,name=None,user=None,time_use=None,
            state=None,queue=None):
        # Simple qstat information 
        self.job_id = job_id
        self.name = name
        self.user = user
        self.time_use = time_use

        # Full qstat information
        self.job_state = None
        self.resources_used_cput = None
        self.resources_used_energy_used = None
        self.resources_used_mem = None
        self.resources_used_vmem = None
        self.resources_used_walltime = None
        self.server = None
        self.checkpoint = None
        self.ctime = None
        self.error_path = None
        self.exec_host = None
        self.hold_types = None
        self.join_path = None
        self.keep_files = None
        self.mail_points = None
        self.mtime = None
        self.output_path = None
        self.priority = None
        self.qtime = None
        self.rerunable = None
        self.resource_list_cput = None
        self.resource_list_mem = None
        self.resource_list_nodect = None
        self.resource_list_nodes = None
        self.resource_list_vmem = None
        self.resource_list_walltime = None
        self.session_id = None
        self.PBS_O_QUEUE=None
        self.PBS_O_HOME=None
        self.PBS_O_LOGNAME=None
        self.PBS_O_PATH = None
        self.PBS_O_MAIL=None
        self.PBS_O_SHELL=None
        self.PBS_O_LANG=None
        self.PBS_O_SUBMIT_FILTER=None
        self.PBS_O_WORKDIR=None
        self.PBS_O_HOST=None
        self.PBS_O_SERVER=None
        self.euser = None
        self.egroup = None
        self.queue_type = None
        self.etime = None
        self.submit_args = None
        self.start_time = None
        self.walltime_remaining = None
        self.start_count = None
        self.fault_tolerant = None
        self.job_radix = None
        self.submit_host = None



"""
===============================================================================

===============================================================================
"""

class Qstat():

    def __init__(self):
        self.ssh_interface = ssh.SSH(config.USERNAME)

    #--------------------------------------------------------------------------

    def login(self,address):
        if not isinstance(address,str):
            raise UserWarning("Invalid address arg type: {}".format(
                type(address).__name__))
        self.ssh_interface = ssh.SSH(address)

    #--------------------------------------------------------------------------

    def process_simple_qstat(self):
        jobs = []
        qstat_data = self.ssh_interface.send_command('qstat')

        if len(qstat_data):
            data = qstat_data[2:]

            for n in data:
                n = [z for z in n.split(' ') if z != '']

                job_id,name,user,time_use,state,queue = n
                job_id = job_id.split('.')[0]

                job_data = QstatData(job_id=job_id,name=name,user=name,
                    time_use=time_use,state=state,queue=queue)
                jobs.append(job_data)

        return jobs

    #--------------------------------------------------------------------------

    def cvrt_time(self,data):
        c = [3600,60,1]
        return sum([int(A)*int(B) for A,B in zip(data.split(':'),c)])


    #--------------------------------------------------------------------------

    def cvrt_datetime(self,data):
        day   = data[:3]
        month = data[3:6]
        date  = data[6:8]
        year  = data[-4:]
        _time = data[8:-4]

        dt = datetime.datetime.strptime('{} {} {}'.format(year,month,date),
            '%Y %b %d')

        unixtime = time.mktime(dt.timetuple())
        unixtime += self.cvrt_time(_time)

        return unixtime

    #--------------------------------------------------------------------------

    def process_full_qstat(self):
        jobs = []
        qstat_data = self.ssh_interface.send_command('qstat -f')

        qstat_data = '\n'.join(qstat_data)
        qstat_data = qstat_data.split('Job Id:')[1:]
        print(len(qstat_data))

        for n in qstat_data:
            job = QstatData()

            n = ''.join([z for z in n if z != ' ']).split('\n')

            job.job_id = n[0].split('.')[0]

            for z in n:
                if not 'Variable_List' in z:
                    z = (z.split('='))
                    if not len(z):
                        pass
                        
                    elif len(z) == 2:
                        key,value = z
                        if "\t" in key:
                            key = key[1:]
                        job.__dict__[exchange[key]] = value

                    elif len(z) == 3:
                        if not 'PBS' in z[0]:
                            key = z[0]

                            if "\t" in key:
                                key = key[1:]
                            value = z[1:]
                            value = ''.join(value)

                            if ',' in value:
                                value = value[:-1]

                            job.__dict__[exchange[key]] = value
                        else:
                            key1 = z[0]
                            value1,key2 = z[1].split(',')
                            value2 = z[2]

                            if "\t" in key1:
                                key1 = key1[1:]

                            job.__dict__[exchange[key1]] = value1
                            job.__dict__[exchange[key2]] = value2

                    elif len(z) == 4:
                        for i in range(3):
                            key,value = z[i],z[i+1]
                            if ',' in key:
                                key = key.split(',')[1]
                            if ',' in value:
                                value = value.split(',')[0]

                            if "\t" in key:
                                key = key[1:]

                            job.__dict__[exchange[key]] = value
                else:
                    z = z.split('Variable_List=')[1]
                    for x in z.split(','):
                        x = x.split('=')
                        if len(x) == 2:
                            key,value = x

                            job.__dict__[exchange[key]] = value

            job.user = job.user.split('@')[0]

            if not job.resources_used_walltime == None:
                job.resources_used_cput = self.cvrt_time(
                    job.resources_used_cput)
                job.resources_used_walltime = self.cvrt_time(
                    job.resources_used_walltime)
            else:
                job.resources_used_cput = 0
                job.resources_used_walltime = 0

            job.resource_list_cput = self.cvrt_time(
                job.resource_list_cput)
            job.resource_list_walltime = self.cvrt_time(
                job.resource_list_walltime)

            job.ctime = self.cvrt_datetime(job.ctime)
            job.etime = self.cvrt_datetime(job.etime)
            job.mtime = self.cvrt_datetime(job.mtime)
            job.qtime = self.cvrt_datetime(job.qtime)

            job.start_time = self.cvrt_datetime(job.start_time)

            job.time_use = job.resources_used_walltime

            jobs.append(job)
            
        return jobs

    #--------------------------------------------------------------------------

    def process_id(self,job_id):
        jobs = self.process_full_qstat()
        print(jobs)
        for n in jobs:
            print(n.job_id,'\t',job_id)
            if n.job_id == job_id:
                return n
        return None

def main():
    q = Qstat()
    jobs = q.process_full_qstat()
    #q.cvrt_datetime('WedOct3114:01:092018')


if __name__ == "__main__":
    main()