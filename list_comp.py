#!/usr/bin/python3 # python3
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
print(compound)


