#!/u r/bin/python3 # python3
import json # preamble
import multiprocessing
import re
import os
import time

from collections import defaultdict
from urllib.request import urlopen # preamble
SERVER='http://aflowlib.duke.edu' # server name
#
PROJECT='AFLOWDATA/ICSD_WEB/' # project name

#
#PROJECT='AFLOWDATA/LIB2_RAW/' # project name

BRAVAIS = ['CUB','FCC','BCC','TET','BCT',\
           'ORC','ORCF','ORCI','ORCC','HEX',\
           'RHL','MCL','MCLC','TRI']


#PROJECT='AFLOWDATA/ICSD_WEB/'
#
#URL=SERVER+'/'+PROJECT # project-layer
#URL=SERVER+'/'+PROJECT+'AlCu_pvMn_pv/' # set-layer
#
#URL=SERVER+'/'+PROJECT+'Cu_pvS/'
#URL=SERVER+'/'+PROJECT
#
#URL='http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/BCT/Ag3Cu1S2_ICSD_163983/'
#
#entry=json.loads(urlopen(URL+'?format=json').readall().decode('utf-8')) # load
#print( entry )
#

def execute_job(aflow_entry):
    try:
        url_req=urlopen(aflow_entry).read().decode('utf-8')
        t=json.loads(url_req) 
        status = 'Valid'
    except ValueError:
        t=None
        status = ValueError
    time.sleep(0.2)
    return (aflow_entry,t,status)

if __name__ == '__main__':

    NPROCESS =32
    pool = multiprocessing.Pool(processes=NPROCESS)
    
    ibravais = 4
    print('Bravais system : ',ibravais,BRAVAIS[ibravais])

    os.mkdir(BRAVAIS[ibravais])
    os.chdir(BRAVAIS[ibravais])
    
    URL=SERVER+'/'+PROJECT+'/'+BRAVAIS[ibravais]
    url_req=urlopen(URL+'?aflowlib_entries&format=json').read().decode('utf-8')
    entry=json.loads(url_req) # load


    for key in entry:
        if key == 'aflowlib_entries':
            aflowlib_entries=entry[key]
            #print(aflowlib_entries)
        #print(aflowlib_entries)
    buffer = []
    buffer_job = []
    for c in aflowlib_entries:
        urlentry=URL+'/'+\
            str(aflowlib_entries[c])+'/'+\
            '?format=json'
        buffer_job.append(urlentry)
        print(c,aflowlib_entries[c],urlentry)
        if len(buffer_job)==NPROCESS:
            print('start query')
            buffer = pool.map(execute_job,buffer_job)

#            pool.close()
#            pool.join() # this makes the script wait here until all jobs are done
            print('end query')
            for (aflow_entry,b,status) in buffer:
                if status == 'Valid': 
                   if 'prototype' in b:
                       print(aflow_entry,b['prototype'])
                       with open(b['prototype']+'.json', 'w') as f:
                           f.write(json.dumps(b, indent=2))
                   else:
                       print(aflow_entry,' Problem: empty record ')
                else:
                   print(aflow_entry,' Problem ')
            buffer = []
            buffer_job = []

    if len(buffer_job)!=0:
        print('start query')
        buffer = pool.map(execute_job,buffer_job)
        print('end query')
        for (aflow_entry,b,status) in buffer:
            if status == 'Valid':
                print(aflow_entry,b['prototype'])
                with open(b['prototype']+'.json', 'w') as f:
                    f.write(json.dumps(b, indent=2))
            else:
                print(aflow_entry,' Problem ')
        buffer = []
        buffer_job = []
