from datetime import date
import os
import multiprocessing
import subprocess

from scripts.lib import setup_logging

# IMPORTANT!
# If you use `python3` not `python`, you should replace all `python` in this file to `python3`
# Please Read this file roughly before running it.
# It is recommended to not to run too many instructions at once, because it will take a long time to finish and may hard to debug when have bugs. 

categories = ["integer", "mask", "floatingpoint", "permute", "fixpoint", "loadstore"]

integer = ['vadc', 'vadd', 'vand', 'vdiv', 'vdivu', 'vmax', 'vmaxu', 'vmin', 'vminu', 'vmadc', 'vmseq', 'vwredsumu', 'vmul', 'vmulh', 'vmulhsu', 'vmulhu', 'vnsra', 'vnsrl', 'vor', 'vmacc', 'vmadd', 'vredxor', 'vrem', 'vremu', 'vrsub', 'vsadd', 'vsaddu', 'vsbc', 'vsll', 'vsra', 'vsrl', 'vssub', 'vssubu', 'vsub', 'vwadd', 'vwaddu', 'vwmacc', 'vwmaccsu', 'vwmaccu', 'vwmul', 'vwmulsu', 'vwmulu', 'vwsub', 'vwsubu', 'vxor', 'vmsgt', 'vmsgtu', 'vmsle', 'vmsleu', 'vmslt', 'vmsltu', 'vmsne', 'vnmsac', 'vnmsub', 'vredand', 'vredmax', 'vredmaxu', 'vredmin', 'vredminu', 'vredor', 'vredsum', 'vwmaccus', 'vmsbc', 'vwredsum', 'vzext', 'vsext']
# For fast tests
integer_short = ['vadd', 'vzext', 'vadc', 'vmadc', 'vsll', 'vmsgt', 'vredand']
integer_widen_short = ['vwadd', 'vwaddu', 'vnsrl', 'vwredsumu']

mask = ['vfirst', 'vid', 'viota', 'vmand', 'vmandnot', 'vmnand', 'vmor', 'vmornot', 'vmsbf', 'vmxnor', 'vmxor', 'vpopc']

floatingpoint = ['vfadd', 'vfclass', 'vfdiv', 'vfmacc', 'vfmadd', 'vfmax', 'vfmerge', 'vfmin', 'vfmsac', 'vfmsub', 'vfmul', 'vfmv', 'vfnmacc', 'vfnmadd', 'vfnmsac', 'vfnmsub', 'vfrdiv', 'vfrec7', 'vfredmax', 'vfredmin', 'vfredosum', 'vfredusum', 'vfrsqrt7', 'vfrsub', 'vfsgnj', 'vfsgnjn', 'vfsgnjx', 'vfsqrt', 'vfsub', 'vfwadd', 'vfwmacc', 'vfwmsac', 'vfwmul', 'vfwnmacc', 'vfwnmsac', 'vfwredsum', 'vfwsub', 'vfncvt', 'vfwcvt', 'vmfeq', 'vmfne', 'vmflt', 'vmfle', 'vmfgt', 'vmfge']
# For fast tests
floatingpoint_short = ['vfadd', 'vfmacc', 'vfmerge', 'vfmv', 'vfcvt', 'vfredosum']
floatingpoint_widen_short = ['vfwadd', 'vfwnmacc', 'vfwredsum']

permute = ['vmre', 'vmv', 'vrgather', 'vrgatherei16',  'vcompress', 'vfslide', 'vslide', 'vslide1']

fixpoint = ['vaadd', 'vaaddu', 'vasub', 'vasubu', 'vnclip', 'vnclipu', 'vsmul', 'vssra', 'vssrl']
# For fast tests
fixpoint_short = ['vaadd', 'vnclip', 'vsmul', 'vssra']

loadstore = ['vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vssege16', 'vssege32', 'vssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxei32', 'vsuxei8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8',  'vsuxei16']


all = dict(integer=integer, mask=mask, floatingpoint=floatingpoint, permute=permute, fixpoint=fixpoint, loadstore=loadstore)

# Modify here if you want to test different VSEW, VLEN, LMUL ect..
def runcommand_integer(ins):
    os.system('python run.py -t i -i %s --vsew 32 --lmul 2' % ins)


def runcommand_fixpoint(ins):
    os.system('python run.py -t x -i %s' % ins)

def runcommand_permute(ins):
    os.system('python run.py -t p -i %s' % ins)


def runcommand_floatingpoint(ins):
    os.system('python run.py -t f -i %s --vlen 512 --vsew 32 --lmul 1' % ins)

def runcommand_loadstore(ins):
    os.system('python run.py -t l -i %s' % ins)

def runcommand_mask(ins):
    # passed 32
    os.system('python run.py -t m -i %s' % ins)
    

def run_integer():
    pool = multiprocessing.Pool(2)
    pool.map(runcommand_integer, integer)

def run_fixpoint():
    pool = multiprocessing.Pool(2)
    pool.map(runcommand_fixpoint, fixpoint)
    dirs = os.listdir('.')

def run_permute():
    pool = multiprocessing.Pool(2)
    pool.map(runcommand_permute, permute)
    dirs = os.listdir('.')

def run_floatingpoint():
    pool = multiprocessing.Pool(2)
    pool.map(runcommand_floatingpoint, floatingpoint)


def run_mask():
    pool = multiprocessing.Pool(2)
    pool.map(runcommand_mask, mask)
    dirs = os.listdir('.')

def run_loadstore():
    pool = multiprocessing.Pool(2)
    pool.map(runcommand_loadstore, loadstore)
    dirs = os.listdir('.')

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
    # run_loadstore()


if __name__ == "__main__":
    main()