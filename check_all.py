# Check all generated folders. Find out if test file FAIL and statistics of COVERAGE.
# Output will in 'check_all.out'
from datetime import date
import os
out = open('check_all.out', 'w+')
dirs = os.listdir('.')
for d in dirs:
    if d.startswith(str(date.today())[5:]):
        print("------------------", file=out)
        instr = d.split('-')[2]
        vlen = d.split('-')[3]
        vsew = d.split('-')[4]
        lmul = d.split('-')[5]
        ass = "%s/%s"%(d, '%s_first.S'%instr) 
        if os.system("test -e %s"%(ass)) != 0:
            print("Generated file is not exist! : %s"%d)
            continue