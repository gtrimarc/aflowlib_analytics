#!/u r/bin/python3 # python3
import json # preamble
import multiprocessing
import re
import os

from collections import defaultdict
from urllib.request import urlopen # preamble
SERVER='http://aflowlib.duke.edu' # server name
#
#PROJECT='AFLOWDATA/' # project name
#PROJECT='AFLOWDATA/ICSD_WEB/' # project name
#
#PROJECT='AFLOWDATA/LIB2_RAW/' # project name
PROJECT='AFLOWDATA/LIB1_RAW/' # project name

#BRAVAIS = ['CUB','FCC','BCC','TET','BCT',\
#           'ORC','ORCF','ORCI','ORCC','HEX',\
#           'RHL','MCL','MCLC','TRI']


def execute_job(aflow_entry):
    label = aflow_entry
    try:
        t=json.loads(urlopen(aflow_entry).readall().decode('utf-8')) 
        status = 'Valid'
    except ValueError:
        t=None
        status = ValueError
    return (label,t,status)

if __name__ == '__main__':


    root_path = os.getcwd() 

    NPROCESS = 32
    pool = multiprocessing.Pool(processes=NPROCESS)
    
    #binary = 'AsB_h'
    #binary = ['B_hP','B_hBi_d','B_hN']
    elements = ['Bi_d','Sb','P','As']
    
    URL=SERVER+'/'+PROJECT
    entry=json.loads(urlopen(URL+'?aflowlib_entries&format=json').readall().decode('utf-8')) # load

    aflowlib_entries=entry['aflowlib_entries']

    print(aflowlib_entries)
        
    for e in aflowlib_entries:

        print(e, e.split(':')[0])
        species_pp_aflow = e.split(':')[0]
        if species_pp_aflow in elements:
            print('element : ',species_pp_aflow,e)
            species_pp_dir = root_path+'/'+e
            os.mkdir(species_pp_dir)
            os.chdir(species_pp_dir)
            urlentry=URL+'/'+str(e)+'/'+'?format=json'
            (label,entry,status) = execute_job(urlentry)
            print(entry['aflowlib_entries'])
            
            buffer = []
            buffer_job = []

            l_entries_dict = type(entry['aflowlib_entries']) is dict

            for s in entry['aflowlib_entries']:
               if l_entries_dict:
                  urlentry=URL+'/'+str(e)+'/'+str(entry['aflowlib_entries'][s])+'/'+'?format=json'
               else:
                  urlentry=URL+'/'+str(e)+'/'+str(s)+'/'+'?format=json'
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
  
            os.chdir(root_path)
