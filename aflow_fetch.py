import json
#import urllib 
from urllib.request import urlopen, urlretrieve
import time
import multiprocessing
import os

#from urllib.request import urlopen # preamble

SERVER='http://aflowlib.duke.edu' # server name
PROJECT='AFLOWDATA/ICSD_WEB' # project name

BRAVAIS = ['CUB','FCC','BCC','TET','BCT',
           'ORC','ORCF','ORCI','ORCC','HEX',
           'RHL','MCL','MCLC','TRI']

ibravais = 13

URL=SERVER+'/'+PROJECT+'/'+BRAVAIS[ibravais]


def fetch_files(url_root, compound, root_folder, lfiles):   
    folder = './'+root_folder+'/'+compound
    os.mkdir(folder)
    os.chdir(folder)
    print(lfiles)
    for f in lfiles:
        print(compound, url_root+'/'+compound+'/'+f)
        urlretrieve(url_root+'/'+compound+'/'+f,f)
    os.chdir('../../')
    
    time.sleep(1.0)
        
def process_entry(info_entry):
    (URL, root_folder, compound) = info_entry
    urlentry = URL+'/'+compound+'/'+'?format=json'
    try:
        aflow_entry=json.loads(urlopen(urlentry).readall().decode('utf-8'))
        lf = aflow_entry['files']
        lfiles = [ x for x in lf if "*" and "AECCAR" and "jvxl" not in x ]
        fetch_files(URL,compound, root_folder, lfiles)
        status = 'Valid'
    except ValueError:
        status = ValueError
    return (urlentry,status)

if __name__ == '__main__':

    NPROCESS =24
    pool = multiprocessing.Pool(processes=NPROCESS)

    url_entry_list = URL+'?aflowlib_entries&format=json'
    entry_json = urlopen(url_entry_list).readall().decode('utf-8')
    entry=json.loads(entry_json)
    
    root_folder = 'full_file_stack'+'_'+BRAVAIS[ibravais]
    os.mkdir(root_folder)
    #os.chdir(root_folder)
    aflowlib_entries = entry['aflowlib_entries']

    buffer = []
    buffer_job = []
    for index in aflowlib_entries:

        compound = aflowlib_entries[index]
        buffer_job.append((URL,root_folder,compound))
        print(index, aflowlib_entries[index])
        
        if len(buffer_job) == NPROCESS:
            
            print('processing of entry batch starts')
            buffer = pool.map(process_entry,buffer_job)
            print('processing of entry batch ends')
            
            for (aflow_entry,status) in buffer:
                if status == 'Valid':
                    print(aflow_entry,' valid, processing completed')
                else:
                    print(aflow_entry,' invalid')
            
            buffer = []
            buffer_job = []

    if len(buffer_job) != 0:

        print('processing of entry batch starts')
        buffer = pool.map(process_entry,buffer_job)
        print('processing of entry batch ends')
        
        for (aflow_entry,status) in buffer:
            if status == 'Valid':
                print(aflow_entry,' valid, processing completed')
            else:
                print(aflow_entry,' invalid')
                
        buffer = []
        buffer_job = []




