from datetime import date
import os
import multiprocessing
import subprocess

from scripts.lib import setup_logging

# IMPORTANT!
# If you use `python3` not `python`, you should replace all `python` in this file to `python3`
# Please Read this file roughly before running it.



categories = ["integer", "mask", "floatingpoint", "permute", "fixpoint", "loadstore"]

integer = ['vadc', 'vadd', 'vand', 'vdiv', 'vdivu', 'vmax', 'vmaxu', 'vmin', 'vminu', 'vmadc', 'vmseq', 'vwredsumu', 'vmul', 'vmulh', 'vmulhsu', 'vmulhu', 'vnsra', 'vnsrl', 'vor', 'vmacc', 'vmadd', 'vredxor', 'vrem', 'vremu', 'vrsub', 'vsadd', 'vsaddu', 'vsbc', 'vsll', 'vsra', 'vsrl', 'vssub', 'vssubu', 'vsub', 'vwadd', 'vwaddu', 'vwmacc', 'vwmaccsu', 'vwmaccu', 'vwmul', 'vwmulsu', 'vwmulu', 'vwsub', 'vwsubu', 'vxor', 'vmsgt', 'vmsgtu', 'vmsle', 'vmsleu', 'vmslt', 'vmsltu', 'vmsne', 'vnmsac', 'vnmsub', 'vredand', 'vredmax', 'vredmaxu', 'vredmin', 'vredminu', 'vredor', 'vredsum', 'vwmaccus', 'vmsbc', 'vwredsum', 'vzext', 'vsext']
# For fast tests
integer_short = ['vadd', 'vzext', 'vadc', 'vmadc', 'vsll', 'vmsgt', 'vredand']
integer_widen_short = ['vwadd', 'vwaddu', 'vnsrl', 'vwredsumu']

mask = ['vfirst', 'vid', 'viota', 'vmand', 'vmandnot', 'vmnand', 'vmor', 'vmornot', 'vmsbf', 'vmxnor', 'vmxor', 'vpopc']

floatingpoint = ['vfadd', 'vfclass', 'vfdiv', 'vfmacc', 'vfmadd', 'vfmax', 'vfmerge', 'vfmin', 'vfmsac', 'vfmsub', 'vfmul', 'vfmv', 'vfnmacc', 'vfnmadd', 'vfnmsac', 'vfnmsub', 'vfrdiv', 'vfrec7', 'vfredmax', 'vfredmin', 'vfredosum', 'vfredusum', 'vfrsqrt7', 'vfrsub', 'vfsgnj', 'vfsgnjn', 'vfsgnjx', 'vfsqrt', 'vfsub', 'vfwadd', 'vfwmacc', 'vfwmsac', 'vfwmul', 'vfwnmacc', 'vfwnmsac', 'vfwredsum', 'vfwsub', 'vfncvt', 'vfwcvt', 'vmfeq', 'vmfne', 'vmflt', 'vmfle', 'vmfgt', 'vmfge']
# For fast tests
floatingpoint_short = ['vfadd', 'vfmacc', 'vfmerge', 'vfmv', 'vfcvt', 'vfredosum',  'vfwadd', 'vfwnmacc', 'vfwredsum']
floatingpoint_widen_short = ['vfwadd', 'vfwnmacc', 'vfwredsum']

permute = ['vmre', 'vmv', 'vrgather', 'vrgatherei16',  'vcompress', 'vfslide', 'vslide', 'vslide1']

fixpoint = ['vaadd', 'vaaddu', 'vasub', 'vasubu', 'vnclip', 'vnclipu', 'vsmul', 'vssra', 'vssrl']
# For fast tests
fixpoint_short = ['vaadd', 'vnclip', 'vsmul', 'vssra']

loadstore = ['vle16', 'vle32', 'vle64', 'vle8', 'vluxei16', 'vluxei32', 'vluxei8', 'vluxsegei16', 'vluxsegei32', 'vluxsegei8', 'vlre16', 'vlre32', 'vlre8', 'vlse16', 'vlse32', 'vlse64', 'vlse8', 'vlssege32', 'vlssege8', 'vlsege16', 'vlsege32', 'vlsege8', 'vlssege16', 'vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vssege16', 'vssege32', 'vssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxei32', 'vsuxei8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8',  'vsuxei16']
load = ['vle16', 'vle32', 'vle64', 'vle8', 'vluxei16', 'vluxei32', 'vluxei8', 'vluxsegei16', 'vluxsegei32', 'vluxsegei8', 'vlre16', 'vlre32', 'vlre8', 'vlse16', 'vlse32', 'vlse64', 'vlse8', 'vlssege32', 'vlssege8', 'vlsege16', 'vlsege32', 'vlsege8', 'vlssege16']
store = ['vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vssege16', 'vssege32', 'vssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxei32', 'vsuxei8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8',  'vsuxei16']
store_seg = ['vlssege16', 'vlssege32', 'vlssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8']
store_no_seg = ['vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vsuxei32', 'vsuxei8', 'vsuxei16' ]

all = dict(integer=integer, mask=mask, floatingpoint=floatingpoint, permute=permute, fixpoint=fixpoint, loadstore=loadstore)

def runcommand_integer(ins):
    if (vsew == 8 or vsew == 64 or lmul_str == "0.125" or lmul_str == "8") and (ins.startswith('vw') or ins.startswith('vn')):
        return
    os.system('python run.py -t i -i %s --vlen %d --vsew %d --lmul %s --elen %d' % (ins, vlen, vsew, lmul_str, elen))

def runcommand_fixpoint(ins):
    if (ins == "vnclip" or ins == "vnclipu") and (vsew == 8 or vsew == 64 or lmul_str == "0.125" or lmul_str == "8"):
        return
    os.system('python run.py -t x -i %s --vlen %d --vsew %d --lmul %s --elen %d' % (ins, vlen, vsew, lmul_str, elen))

def runcommand_permute(ins):
    if ins == "vfslide" and (vsew == 8 or vsew == 16):
        return
    if ins == "vrgatherei16" and ((vsew == 8 and lmul_str == "8") or (vsew == 32 and lmul_str == "0.125") or (vsew == 64 and lmul_str == "0.125") or (vsew == 64 and lmul_str == "0.25")):
        return
    os.system('python run.py -t p -i %s --vlen %d --vsew %d --lmul %s --elen %d' % (ins, vlen, vsew, lmul_str, elen))

def runcommand_floatingpoint(ins):
    if (vsew == 8 or vsew == 64 or lmul_str == "0.125" or lmul_str == "8") and (ins.startswith('vfw') or ins.startswith('vfn')):
        return
    if (vsew == 8 or vsew == 16):
        return
    os.system('python run.py -t f -i %s --vlen %d --vsew %d --lmul %s --elen %d' % (ins, vlen, vsew, lmul_str, elen))

def runcommand_loadstore(ins):
    os.system('python run.py -t l -i %s --vlen %d --vsew %d --lmul %s --elen %d' % (ins, vlen, vsew, lmul_str, elen))

def runcommand_mask(ins):
    os.system('python run.py -t m -i %s --vlen %d --vsew %d --lmul %s --elen %d' % (ins, vlen, vsew, lmul_str, elen))
    

def run_integer():
    pool = multiprocessing.Pool(1)
    pool.map(runcommand_integer, integer)

def run_fixpoint():
    pool = multiprocessing.Pool(1)
    pool.map(runcommand_fixpoint, fixpoint)

def run_permute():
    pool = multiprocessing.Pool(1)
    pool.map(runcommand_permute, permute)

def run_floatingpoint():
    pool = multiprocessing.Pool(1)
    pool.map(runcommand_floatingpoint, floatingpoint)

def run_mask():
    pool = multiprocessing.Pool(1)
    pool.map(runcommand_mask, mask)

def run_loadstore():
    pool = multiprocessing.Pool(1)
    pool.map(runcommand_loadstore, loadstore)

# Modify here to config
vlen = 512
vsew = 32
lmul_str = "0.25"  # "1", "2", "4", "8", "0.25", "0.5", "0.125"
elen = 64

# Generate all and Put final ELF to a directory
def main():
    subprocess.run(["mkdir", "-p", 'generate_all'])
    setup_logging(True)
    # Modify here to choose which categories you want to generate
    run_integer()
    run_floatingpoint()
    run_mask()
    run_fixpoint()
    run_permute()
    run_loadstore()


if __name__ == "__main__":
    main()