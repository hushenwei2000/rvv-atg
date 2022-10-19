from datetime import date
import os
import multiprocessing
import subprocess

from scripts.lib import setup_logging

categories = ["integer", "mask", "floatingpoint", "permute", "fixpoint", "loadstore"]

integer = ['vadc', 'vadd', 'vand', 'vdiv', 'vdivu', 'vmax', 'vmaxu', 'vmin', 'vminu', 'vmadc', 'vmseq', 'vwredsumu', 'vmul', 'vmulh', 'vmulhsu', 'vmulhu', 'vnsra', 'vnsrl', 'vor', 'vmacc', 'vmadd', 'vredxor', 'vrem', 'vremu', 'vrsub', 'vsadd', 'vsaddu', 'vsbc', 'vsll', 'vsra', 'vsrl', 'vssub', 'vssubu', 'vsub', 'vwadd', 'vwaddu', 'vwmacc', 'vwmaccsu', 'vwmaccu', 'vwmul', 'vwmulsu', 'vwmulu', 'vwsub', 'vwsubu', 'vxor', 'vmsgt', 'vmsgtu', 'vmsle', 'vmsleu', 'vmslt', 'vmsltu', 'vmsne', 'vnmsac', 'vnmsub', 'vredand', 'vredmax', 'vredmaxu', 'vredmin', 'vredminu', 'vredor', 'vredsum', 'vwmaccus', 'vmsbc', 'vwredsum']

mask = ['vfirst', 'vid', 'viota', 'vmand', 'vmandnot', 'vmnand', 'vmor', 'vmornot', 'vmsbf', 'vmxnor', 'vmxor', 'vpopc']

floatingpoint = ['vfmv', 'vfnmsac', 'vfnmsub', 'vfrdiv', 'vfredmax', 'vfredmin', 'vfwadd', 'vfwcvt', 'vfwmacc', 'vfwmul', 'vfwsub', 'vfmacc', 'vfrec', 'vfredosum', 'vfrsqrt7', 'vfsgnj', 'vfsgnjx', 'vfsub', 'vfmadd', 'vfmerge', 'vfmsac', 'vfmul', 'vfnmadd', 'vfwnmacc', 'vfadd', 'vfdiv', 'vfncvt', 'vfwredsum', 'vfclass', 'vfredusum', 'vfrsub', 'vfsgnjn', 'vfsqrt', 'vfcvt', 'vfmax', 'vfmin', 'vfmsub', 'vfnmacc', 'vfwmsac', 'vfwnmsac']

permute = ['vmre', 'vslide1', 'vmv', 'vrgather', 'vrgatherei16', 'vfslide', 'vcompress', 'vslide']

fixpoint = ['vaadd', 'vaaddu', 'vasub', 'vasubu', 'vnclip', 'vnclipu', 'vsmul', 'vssra', 'vssrl']

loadstore = ['vle16', 'vle32', 'vle64', 'vle8', 'vluxei16', 'vluxei32', 'vluxei8', 'vluxsegei16', 'vluxsegei32', 'vluxsegei8', 'vlre16', 'vlre32', 'vlre8', 'vlse16', 'vlse32', 'vlse64', 'vlse8', 'vlssege32', 'vlssege8', 'vlsege16', 'vlsege32', 'vlsege8', 'vlssege16', 'vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vssege16', 'vssege32', 'vssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxei32', 'vsuxei8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8',  'vsuxei16']

all = dict(integer=integer, mask=mask, floatingpoint=floatingpoint, permute=permute, fixpoint=fixpoint, loadstore=loadstore)

# Modify here if you want to test different VSEW, VLEN, LMUL ect..
def runcommand_integer(ins):
    os.system('python run.py -t i -i %s' % ins)

def runcommand_fixpoint(ins):
    os.system('python run.py -t x -i %s' % ins)

def runcommand_permute(ins):
    os.system('python run.py -t p -i %s' % ins)

def runcommand_floatingpoint(ins):
    os.system('python run.py -t f -i %s' % ins)

def runcommand_loadstore(ins):
    os.system('python run.py -t l -i %s' % ins)

def runcommand_mask(ins):
    os.system('python run.py -t m -i %s' % ins)

def run_integer():
    pool = multiprocessing.Pool(30)
    pool.map(runcommand_integer, integer)
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):
            instr = d.split('-')[2]
            log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log) == 0:
                print("Generated file is WRONG! : %s"%instr)
                os.system('cp %s ./generate_all'%log)
            elf = "%s/%s"%(d, 'ref_final.elf')
            os.system('cp %s ./generate_all/%s.elf'%(elf, instr))

def run_fixpoint():
    pool = multiprocessing.Pool(30)
    pool.map(runcommand_fixpoint, fixpoint)
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):
            instr = d.split('-')[2]
            log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log) == 0:
                print("Generated file is WRONG! : %s"%instr)
                os.system('cp %s ./generate_all'%log)
            elf = "%s/%s"%(d, 'ref_final.elf')
            os.system('cp %s ./generate_all/%s.elf'%(elf, instr))

def run_permute():
    pool = multiprocessing.Pool(30)
    pool.map(runcommand_permute, permute)
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):
            instr = d.split('-')[2]
            log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log) == 0:
                print("Generated file is WRONG! : %s"%instr)
                os.system('cp %s ./generate_all'%log)
            elf = "%s/%s"%(d, 'ref_final.elf')
            os.system('cp %s ./generate_all/%s.elf'%(elf, instr))

def run_floatingpoint():
    pool = multiprocessing.Pool(30)
    pool.map(runcommand_floatingpoint, floatingpoint)
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):
            instr = d.split('-')[2]
            log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log) == 0:
                print("Generated file is WRONG! : %s"%instr)
                os.system('cp %s ./generate_all'%log)
            elf = "%s/%s"%(d, 'ref_final.elf')
            os.system('cp %s ./generate_all/%s.elf'%(elf, instr))

def run_mask():
    pool = multiprocessing.Pool(30)
    pool.map(runcommand_mask, mask)
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):
            instr = d.split('-')[2]
            log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log) == 0:
                print("Generated file is WRONG! : %s"%instr)
                os.system('cp %s ./generate_all'%log)
            elf = "%s/%s"%(d, 'ref_final.elf')
            os.system('cp %s ./generate_all/%s.elf'%(elf, instr))

def run_loadstore():
    pool = multiprocessing.Pool(30)
    pool.map(runcommand_loadstore, loadstore)
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):
            instr = d.split('-')[2]
            log = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log) == 0:
                print("Generated file is WRONG! : %s"%instr)
                os.system('cp %s ./generate_all'%log)
            elf = "%s/%s"%(d, 'ref_final.elf')
            os.system('cp %s ./generate_all/%s.elf'%(elf, instr))

# Generate all and Put final ELF to a directory
def main():
    subprocess.run(["mkdir", "-p", 'generate_all'])
    setup_logging(True)
    # Modify here to choose which categories you want to generate
    run_integer()
    # run_mask()
    # run_floatingpoint()
    # run_fixpoint()
    # run_permute()
    run_loadstore()


if __name__ == "__main__":
    main()