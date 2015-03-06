#!/usr/bin/python3 # python3
import json # preamble
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

#URL='http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/BCT/Ag3Cu1S2_ICSD_163983/'

#entry=json.loads(urlopen(URL+'?format=json').readall().decode('utf-8')) # load

#print( entry )
for l1 in BRAVAIS:
    PROJECT1=PROJECT+l1+'/'
    URL=SERVER+'/'+PROJECT1
    entry=json.loads(urlopen(URL+'?format=json').readall().decode('utf-8')) # load
    for key in entry: # loop keys
        #print( key )
        if key == 'aflowlib_entries':
            total_entries = 
            print(len(entry[key]))
            #print( "{}={}".format(key, entry[key]) ) # print key
            

