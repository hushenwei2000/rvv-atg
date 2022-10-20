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
        log = "%s/%s"%(d, 'spike_%s_final.log'%instr) 
        if os.system("grep FAIL %s"%(log)) == 0:
            print("Generated file is WRONG! : %s"%d)
        report = "%s/coverage_final.rpt"%d
        try:
            f = open(report, 'r')
            lines = f.readlines()
            flag = False
            for line in lines:
                if flag:
                    print(line, file=out)
                    if 'coverage' in line:
                        Flag = False
                        break
                if 'mnemonics' in line:
                    flag = True
            f.close()
        except FileNotFoundError:
            print ("File is not found: %s."%report, file=out)