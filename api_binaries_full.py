#!/u r/bin/python3 # python3
import json # preamble
import multiprocessing
import re
import os

from collections import defaultdict
from urllib.request import urlopen # preamble
SERVER='http://aflowlib.duke.edu' # server name
#
<<<<<<< HEAD
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
=======
#PROJECT='AFLOWDATA/' # project name
#PROJECT='AFLOWDATA/ICSD_WEB/' # project name
#
PROJECT='AFLOWDATA/LIB2_RAW/' # project name

#BRAVAIS = ['CUB','FCC','BCC','TET','BCT',\
#           'ORC','ORCF','ORCI','ORCC','HEX',\
#           'RHL','MCL','MCLC','TRI']


def execute_job(aflow_entry):
    label = aflow_entry
>>>>>>> d81e20d94444a5fdf92225b158b1888b71b8d526
    try:
        t=json.loads(urlopen(aflow_entry).readall().decode('utf-8')) 
        status = 'Valid'
    except ValueError:
        t=None
        status = ValueError
<<<<<<< HEAD
    return (aflow_entry,t,status)

if __name__ == '__main__':

    NPROCESS =32
    pool = multiprocessing.Pool(processes=NPROCESS)
    
    ibravais = 4
    print('Bravais system : ',ibravais,BRAVAIS[ibravais])

    os.mkdir(BRAVAIS[ibravais])
    os.chdir(BRAVAIS[ibravais])
    
    URL=SERVER+'/'+PROJECT+'/'+BRAVAIS[ibravais]
    entry=json.loads(urlopen(URL+'?aflowlib_entries&format=json').readall().decode('utf-8')) # load


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
=======
    return (label,t,status)

if __name__ == '__main__':

    NPROCESS = 32
    pool = multiprocessing.Pool(processes=NPROCESS)
    
    #binary = 'AsB_h'
    #binary = ['B_hP','B_hBi_d','B_hN']
    binary = ['B_hSb']
    
    URL=SERVER+'/'+PROJECT
    entry=json.loads(urlopen(URL+'?aflowlib_entries&format=json').readall().decode('utf-8')) # load

    aflowlib_entries=entry['aflowlib_entries']
        
    for alloy in aflowlib_entries:

        if alloy in binary:
            print('alloy : ',alloy)
            os.mkdir(alloy)
            os.chdir(alloy)
            urlentry=URL+'/'+str(alloy)+'/'+'?format=json'
            (label,entry,status) = execute_job(urlentry)
            print(entry['aflowlib_entries'])
            
            buffer = []
            buffer_job = []

            for s in entry['aflowlib_entries']:
               urlentry=URL+'/'+str(alloy)+'/'+str(entry['aflowlib_entries'][s])+'/'+'?format=json'
               print(urlentry)
               buffer_job.append(urlentry)
               if len(buffer_job)==NPROCESS:

                   print('start fetching batch')
                   buffer = pool.map(execute_job,buffer_job)
                   print('done fetching batch')
                   
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

                print('start fetching batch')
                buffer = pool.map(execute_job,buffer_job)
                print('done fetching batch')

                for (aflow_entry,b,status) in buffer:
                    if status == 'Valid':
                        print(aflow_entry,b['prototype'])
                        with open(b['prototype']+'.json', 'w') as f:
                            f.write(json.dumps(b, indent=2))
                    else:
                        print(aflow_entry,' Problem ')

                buffer = []
                buffer_job = []
  
            os.chdir('../')
>>>>>>> d81e20d94444a5fdf92225b158b1888b71b8d526
