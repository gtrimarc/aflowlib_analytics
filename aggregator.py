import json # preamble
import multiprocessing
import pandas as pd
#import re
import os
#import csv

NPROCESS = 8 
#pool = multiprocessing.Pool(processes=NPROCESS)

#BRAVAIS = ['CUB','FCC','BCC',\
#           'TET','BCT','ORC',\
#           'ORCF','ORCI','ORCC',\
#           'HEX','RHL','MCL',\
#           'MCLC','TRI']

BRAVAIS = ['CUB','FCC','BCC']


aflowlib_file_folder = '/home/gtrimarc/Dropbox/Current_Projects/Gamma_Ray/aflowlib_scan.dir/aflowlib_data.dir'

def return_df(json_file):
    print json_file 
    try:
        with open(json_file, 'r') as f:
            entry =  json.load(f)
            status = 'Valid'
    except ValueError:
        data_entry=None
        status = ValueError
    if status == 'Valid' : df = pd.read_json(json_file)
    return (status,df)

for bravais_type in BRAVAIS:
    folder = aflowlib_file_folder + '/' + bravais_type
    print bravais_type, folder
    frame = pd.DataFrame()
    file_list = os.listdir(folder)
    
    buffer_job = []
    for c in file_list:
        compound_file = str(folder+'/'+c)
        buffer_job.append(compound_file)
        if len(buffer_job)==NPROCESS:
            #print('start processing')
            #buffer = pool.map(return_df,buffer_job)
            buffer = map(return_df,buffer_job)
            #print type(df_buffer)
            df_buffer = []
            for (status,df) in buffer:
                if status == 'Valid':
                   df_buffer.append(df)
            frame0 = pd.concat(df_buffer)
            frame = pd.concat([frame,frame0])
            #print('end processing')
            buffer_job = []
            df_buffer = []
    
    if len(buffer_job)!=0:
        #print('start processing')
        #buffer = pool.map(return_df,buffer_job)
        buffer = map(return_df,buffer_job)
        for (status,df) in buffer:
            if status == 'Valid':
               df_buffer.append(df)
        frame0 = pd.concat(df_buffer)
        frame = pd.concat([frame,frame0])
        #print('end processing')
        
    file_data_set = 'aflow_icsd_' + bravais_type + '.csv'
    frame.to_csv(file_data_set)
