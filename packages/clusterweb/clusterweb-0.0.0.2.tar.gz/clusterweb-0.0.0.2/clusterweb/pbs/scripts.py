qscript = """
### Script for setting qsub configuration and calling Python script
### Set number of nodes: Set number of cores
#PBS -l nodes={}:ppn={}

### Set walltime
#PBS -l walltime={}

### Set amount of memory
#PBS -l mem={}

### Set CPU time ([[h:]m:]s).
#PBS -l cput={}

{}
"""

#------------------------------------------------------------------------------

pyscript = """
import subprocess

PYTHON_VERSION = {}

script = '''
import pickle
import shutil
import sys
import os

temp_dir = '{}'

try:
    with open(os.path.join(temp_dir,'fnc.pkl'),'rb') as f:
        fnc = pickle.loads(f.read())

    with open(os.path.join(temp_dir,'args.pkl'),'rb') as f:
        args = pickle.loads(f.read())
        
    output = fnc(args)
except Exception as e:
    output = e

with open(os.path.join(temp_dir,'result.pkl'),'wb') as f:
    f.write(pickle.dumps(output))
'''
if PYTHON_VERSION == 2:
    subprocess.call(["python2","-c",script])
else:
    subprocess.call(["python3","-c",script])

"""

#------------------------------------------------------------------------------

session_pyscript = """
#-*- encoding: utf-8 -*-
import subprocess
import threading
import time
import dill
import sys
import os

PYTHON_VERSION = {}

script = '''
import importlib
import threading
import pickle
import string
import dill
import time
import sys
import os                 

job_dir = \"{}\"

def run_job(func_file,args_file,num):

    with open(func_file,"rb") as f:
        fnc = pickle.load(f)

    with open(args_file,"rb") as f:
        print(args_file)
        myargs = pickle.load(f)
        if not isinstance(myargs,list):
            myargs = [myargs]
    try:
        output = fnc(*myargs)

    except Exception as e:
        output = e

    with open(os.path.join(job_dir,"res"+str(num)+".pkl"),"wb") as f:
        pickle.dump(output,f)

jobs = [n for n in os.listdir(job_dir) if 'fnc' in n]
print(jobs)
n_jobs = len(jobs)

for job in jobs:
    print(job)
    func_file = os.path.join(job_dir,job)
    
    num = int(job.split('.')[0][-1])
    args_file = os.path.join(job_dir,'args'+str(num)+'.pkl')

    thread = threading.Thread(target=run_job,args=(func_file,args_file,num))
    thread.daemon = False
    thread.start()

    while True:
        finished = True
        for i in range(num):
            if not os.path.exists(os.path.join(job_dir,"args"+str(num)+".pkl")):
                finished = False

        time.sleep(1e-1)

        if finished:
            break
'''
if PYTHON_VERSION == 2:
    subprocess.call(["python2","-c",script])
else:
    subprocess.call(["python3","-c",script])
"""