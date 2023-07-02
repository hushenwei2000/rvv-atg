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
        log = "%s/%s"%(d, 'spike_%s_final.log'%instr) 
        if os.system("grep pass %s"%(log)) != 0:
            print("Generated file is WRONG or not exist! : %s"%d)
            continue
        report = "%s/coverage_final.rpt"%d
        try:
            f = open(report, 'r')
            lines = f.readlines()
            # Collect instruction's coverages
            flag = False
            for line in lines:
                if flag:
                    print(line, file=out)
                    if 'coverage' in line:
                        Flag = False
                        break
                if 'mnemonics' in line:
                    flag = True
            # Collect other coverage
            for line in lines:
                if ('rd:' in line) or ('rs1:' in line) or ('rs2:' in line) or ('val_comb:' in line) or ('coverage' in line):
                    print(line, file = out)
            # Collect configuration information
            print("{}, {}, {}".format(vlen, vsew, lmul), file = out)

            f.close()
        except FileNotFoundError:
            print ("File is not found: %s."%report, file=out)