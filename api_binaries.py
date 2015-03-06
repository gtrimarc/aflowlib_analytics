#!/u r/bin/python3 # python3
import json # preamble
import re

from collections import defaultdict
from urllib.request import urlopen # preamble
SERVER='http://aflowlib.duke.edu' # server name
#
#PROJECT='AFLOWDATA/ICSD_WEB/' # project name

#
PROJECT='AFLOWDATA/LIB2_RAW/' # project name

#BRAVAIS = ['CUB','FCC','BCC','TET','BCT',\
#           'ORC','ORCF','ORCI','ORCC','HEX',\
#           'RHL','MCL','MCLC','TRI']

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

spec_Alk = ['Li','Na','K','Rb','Cs']
spec_Noble = ['Cu','Ag','Au']
spec_Ch = ['S','Se','Te']

spec_A = spec_Alk+spec_Noble
spec_B = spec_A
spec_X = spec_Ch

compound=[]
for sA in spec_A:
    for sB in spec_B:
        if sA != sB:
            for sX in spec_X:
                lst = [sA,sB,sX]
                lst.sort()
                compound.append(lst)

list_entries = defaultdict(list)

total_num = 0
URL=SERVER+'/'+PROJECT
entry=json.loads(urlopen(URL+'?aflowlib_entries&format=json').readall().decode('utf-8')) # load

for key in entry:
    if key == 'aflowlib_entries':
        total_num = total_num + len(entry[key])
        aflowlib_entries=entry[key]
        print(aflowlib_entries)
        for c in aflowlib_entries:
            
            lst = re.findall('[A-Z][^A-Z]*',c)
            #lst = lst[:len(lst)-1]
            lst.sort()
            
            t=tuple(lst)
            #list_entries[t].append(URL+aflowlib_entries[e])
            
            print(c,lst)

#for t in compound:
#    print(t, list_entries[tuple(t)])
#    lst = list_entries[tuple(t)]
#    for c in lst:
#        entry=json.loads(urlopen(c+'/'+'?format=json').readall().decode('utf-8'))
#        print(c,entry['enthalpy_cell'])

