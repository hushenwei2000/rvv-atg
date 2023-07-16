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
        elf = "%s/%s_first.S"%(d, instr)
        if not os.path.isfile(elf):
            print("No first.S for %s"%full_instr)
            elf = "%s/%s_empty.S"%(d, instr)
        if os.system("cat %s | grep RVMODEL_DATA_END"%elf):
            print("No RVMODEL_DATA_END for %s"%full_instr)
        os.system('cp %s ./generate_all/%s.S'%(elf, instr))