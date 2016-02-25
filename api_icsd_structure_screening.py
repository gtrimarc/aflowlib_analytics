#!/u r/bin/python3 # python3
import json # preamble
import multiprocessing
import re
import os
import csv

from collections import defaultdict
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

def execute_job(args):
    aflow_entry = args[0]
    keys = args[1]
    try:
        with open(aflow_entry, 'r') as f:
            entry =  json.load(f)
            data_entry = {}
            for key in keys:
                print(entry[key])
                data_entry[key] = entry[key] 
            status = 'Valid'
    except ValueError:
        data_entry=None
        status = ValueError
    return (aflow_entry,data_entry,status)

if __name__ == '__main__':

    NPROCESS =32
    
#    ibravais = 1
#    bravais_type = BRAVAIS[ibravais]

    for bravais_type in BRAVAIS:
        print('Bravais system : ',bravais_type)

        compound_list = os.listdir(bravais_type)

        keys = ['prototype','compound','natoms',\
                'nspecies','spacegroup_relax',\
                'geometry','positions_fractional',\
                'ldau_TLUJ','species_pp',\
                'species_pp_version',\
                'density','valence_cell_std',\
                'dft_type','Egap','Egap_fit','Egap_type',\
                'spin_cell','scintillation_attenuation_length','aurl']

        writer = csv.writer(open('structure_info_bravais_'+bravais_type+'.csv', 'w'))
        writer.writerow(keys)

        pool = multiprocessing.Pool(processes=NPROCESS)

        buffer = []
        buffer_job = []
        for c in compound_list:
            compound_file = str(bravais_type+'/'+c)
            buffer_job.append((compound_file,keys))
            print(c,compound_file)
            if len(buffer_job)==NPROCESS:
                print('start processing')
                buffer = pool.map(execute_job,buffer_job)
    #           pool.close()
    #           pool.join() # this makes the script wait here until all jobs are done
                print('end processing')
                for (aflow_entry,b,status) in buffer:
                    if status == 'Valid': 
                       properties = []
                       for key in keys:
                           if key in b:
                              properties.append(b[key])
                           else:
                              print(aflow_entry,' Problem: empty record ')
                       writer.writerow(properties)
                    else:
                       print(aflow_entry,' Problem ')
                buffer = []
                buffer_job = []

        if len(buffer_job)!=0:
            print('start processing')
            buffer = pool.map(execute_job,buffer_job)
            print('end processing')
            for (aflow_entry,b,status) in buffer:
                if status == 'Valid':
                    properties = []
                    for key in keys:
                        if key in b:
                            properties.append(b[key])
                        else:
                            print(aflow_entry,' Problem: empty record ')
                    writer.writerow(properties)
                else:
                    print(aflow_entry,' Problem ')
            buffer = []
            buffer_job = []

