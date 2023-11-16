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
        assemb = "%s/%s_second.S"%(d, instr)
        elf = "%s/ref_final.elf"%(d)
        if not os.path.isfile(assemb):
            print("No second.S for %s"%full_instr)
            assemb = "%s/%s_first.S"%(d, instr)
            if not os.path.isfile(assemb):
                print("No first.S for %s"%full_instr)
            else:
                os.system('cp %s ./generate_all/%s.S'%(assemb, full_instr))
                os.system('cp %s ./generate_all_elf/%s.elf'%(elf, full_instr))
        else:
            os.system('cp %s ./generate_all/%s.S'%(assemb, full_instr))
            os.system('cp %s ./generate_all_elf/%s.elf'%(elf, full_instr))
