import os
from datetime import date
dirs = os.listdir('.')
if not os.path.isdir('generate_all'):
    os.makedirs('generate_all')
for d in dirs:
    if d.startswith(str(date.today())[5:]):
        instr = d.split('-')[2]
        instr_index = d.find(instr)
        full_instr = d[instr_index:]
        log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
        if os.system("grep pass %s"%(log)) != 0:
            print("Generated file is WRONG or not exist! : %s"%d)
            os.system('cp %s ./generate_all'%log)
            continue
        elf = "%s/%s"%(d, 'ref_final.elf')
        os.system('cp %s ./generate_all/%s.elf'%(elf, full_instr))