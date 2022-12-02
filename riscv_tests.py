'''
	Script to generate tests and compose them in a folder (rv64uv) according to riscv-tests format
	Last Modified: December 2, 2022 by Quswar Abid (quswar.abid@10xengineers.ai)
'''


from datetime import *
from datetime import date
import os
import multiprocessing
import subprocess

from scripts.lib import setup_logging

lmul = ['1.0', '2.0', '4.0', '8.0', '0.5', '0.25', '0.125']
sew = ['8', '16', '32', '64']
vlen = '4096'

categories = ["integer", "mask", "floatingpoint", "permute", "fixpoint", "loadstore"]

integer = ['vadd', 'vadc', 'vadd', 'vand', 'vdiv', 'vdivu', 'vmax', 'vmaxu', 'vmin', 'vminu', 'vmadc', 'vmseq', 'vwredsumu', 'vmul', 'vmulh', 'vmulhsu', 'vmulhu', 'vnsra', 'vnsrl', 'vor', 'vmacc', 'vmadd', 'vredxor', 'vrem', 'vremu', 'vrsub', 'vsadd', 'vsaddu', 'vsbc', 'vsll', 'vsra', 'vsrl', 'vssub', 'vssubu', 'vsub', 'vwadd', 'vwaddu', 'vwmacc', 'vwmaccsu', 'vwmaccu', 'vwmul', 'vwmulsu', 'vwmulu', 'vwsub', 'vwsubu', 'vxor', 'vmsgt', 'vmsgtu', 'vmsle', 'vmsleu', 'vmslt', 'vmsltu', 'vmsne', 'vnmsac', 'vnmsub', 'vredand', 'vredmax', 'vredmaxu', 'vredmin', 'vredminu', 'vredor', 'vredsum', 'vwmaccus', 'vmsbc', 'vwredsum']

mask = ['vfirst', 'vid', 'viota', 'vmand', 'vmandnot', 'vmnand', 'vmor', 'vmornot', 'vmsbf', 'vmxnor', 'vmxor', 'vpopc']

# Exclude 'vfncvt', 'vfwcvt', 'vfcvt', 
# floatingpoint = ['vfadd', 'vfclass', 'vfdiv', 'vfmacc', 'vfmadd', 'vfmax', 'vfmerge', 'vfmin', 'vfmsac', 'vfmsub', 'vfmul', 'vfmv', 'vfnmacc', 'vfnmadd', 'vfnmsac', 'vfnmsub', 'vfrdiv', 'vfrec7', 'vfredmax', 'vfredmin', 'vfredosum', 'vfredusum', 'vfrsqrt7', 'vfrsub', 'vfsgnj', 'vfsgnjn', 'vfsgnjx', 'vfsqrt', 'vfsub', 'vfwadd', 'vfwmacc', 'vfwmsac', 'vfwmul', 'vfwnmacc', 'vfwnmsac', 'vfwredsum', 'vfwsub']
floatingpoint = ['vfadd']

permute = ['vmre', 'vslide1', 'vmv', 'vrgather', 'vrgatherei16', 'vfslide', 'vcompress', 'vslide']

fixpoint = ['vaadd', 'vaaddu', 'vasub', 'vasubu', 'vnclip', 'vnclipu', 'vsmul', 'vssra', 'vssrl']

loadstore = ['vle16', 'vle32', 'vle64', 'vle8', 'vluxei16', 'vluxei32', 'vluxei8', 'vluxsegei16', 'vluxsegei32', 'vluxsegei8', 'vlre16', 'vlre32', 'vlre8', 'vlse16', 'vlse32', 'vlse64', 'vlse8', 'vlssege32', 'vlssege8', 'vlsege16', 'vlsege32', 'vlsege8', 'vlssege16', 'vs1r', 'vs2r', 'vs4r', 'vs8r', 'vse16', 'vse32', 'vse8', 'vsse16', 'vsse32', 'vsse8', 'vssege16', 'vssege32', 'vssege8', 'vsssege16', 'vsssege32', 'vsssege8', 'vsuxei32', 'vsuxei8', 'vsuxsegei16', 'vsuxsegei32', 'vsuxsegei8',  'vsuxei16']

all = dict(integer=integer, mask=mask, floatingpoint=floatingpoint, permute=permute, fixpoint=fixpoint, loadstore=loadstore)

###################################################################################################################################################
############################################# VECTOR FIXED-POINT ARITHMETIC INSTRUCTIONS ##########################################################
###################################################################################################################################################
def runcommand_fixpoint(ins):
    for i in lmul:
        for j in sew:
            print("---------------------------------------------------------------")
            print(ins,i,j)
            passing_string = 'python run.py -t x -i %s --vlen %s --lmul %s --vsew %s 1>generate_all_logs/%s_LMUL%s_SEW%s.log 2>&1' %(ins,vlen,i,j,ins,i,j)
            print("---------------------------------------------------------------")
            print(passing_string)
            print("---------------------------------------------------------------")
            os.system(passing_string)
            copy_this(ins,i,j)
def run_fixpoint():
    pool = multiprocessing.Pool()
    pool.map(runcommand_fixpoint, fixpoint)

###################################################################################################################################################
############################################## VECTOR INTEGER ARITHMETIC INSTRUCTIONS #############################################################
###################################################################################################################################################
def runcommand_integer(ins):
    for i in lmul:
        for j in sew:
            print("---------------------------------------------------------------")
            print(ins,i,j)
            passing_string = 'python run.py -t i -i %s --vlen %s --lmul %s --vsew %s 1>generate_all_logs/%s_LMUL%s_SEW%s.log 2>&1' %(ins,vlen,i,j,ins,i,j)
            print("---------------------------------------------------------------")
            print(passing_string)
            print("---------------------------------------------------------------")
            os.system(passing_string)
            copy_this(ins,i,j)
def run_integer():
    pool = multiprocessing.Pool()
    pool.map(runcommand_integer, integer)

###################################################################################################################################################
################################################# VECTOR PERMUTATION INSTRUCTIONS #################################################################
###################################################################################################################################################
def runcommand_permute(ins):
    for i in lmul:
        for j in sew:
            print("---------------------------------------------------------------")
            print(ins,i,j)
            passing_string = 'python run.py -t p -i %s --vlen %s --lmul %s --vsew %s 1>generate_all_logs/%s_LMUL%s_SEW%s.log 2>&1' %(ins,vlen,i,j,ins,i,j)
            print("---------------------------------------------------------------")
            print(passing_string)
            print("---------------------------------------------------------------")
            os.system(passing_string)
            copy_this(ins,i,j)
def run_permute():
    pool = multiprocessing.Pool()
    pool.map(runcommand_permute, permute)

###################################################################################################################################################
################################################ VECTOR FLOATING POINT INSTRUCTIONS ###############################################################
###################################################################################################################################################
def runcommand_floatingpoint(ins):
    for i in lmul:
        for j in sew:
            print("---------------------------------------------------------------")
            print(ins,i,j)
            passing_string = 'python run.py -t f -i %s --vlen %s --lmul %s --vsew %s 1>generate_all_logs/%s_LMUL%s_SEW%s.log 2>&1' %(ins,vlen,i,j,ins,i,j)
            print("---------------------------------------------------------------")
            print(passing_string)
            print("---------------------------------------------------------------")
            os.system(passing_string)
            copy_this(ins,i,j)
def run_floatingpoint():
    pool = multiprocessing.Pool()
    pool.map(runcommand_floatingpoint, floatingpoint)

###################################################################################################################################################
################################################### VECTOR LOAD/STORE INSTRUCTIONS ################################################################
###################################################################################################################################################
def runcommand_loadstore(ins):
    for i in lmul:
        for j in sew:
            print("---------------------------------------------------------------")
            print(ins,i,j)
            passing_string = 'python run.py -t l -i %s --vlen %s --lmul %s --vsew %s 1>generate_all_logs/%s_LMUL%s_SEW%s.log 2>&1' %(ins,vlen,i,j,ins,i,j)
            print("---------------------------------------------------------------")
            print(passing_string)
            print("---------------------------------------------------------------")
            os.system(passing_string)
            copy_this_load_store(ins,i,j)
def run_loadstore():
    pool = multiprocessing.Pool()
    pool.map(runcommand_loadstore, loadstore)

###################################################################################################################################################
####################################################### VECTOR MASK INSTRUCTIONS ##################################################################
###################################################################################################################################################
def runcommand_mask(ins):
    for i in lmul:
        for j in sew:
            print("---------------------------------------------------------------")
            print(ins,i,j)
            passing_string = 'python run.py -t m -i %s --vlen %s --lmul %s --vsew %s 1>generate_all_logs/%s_LMUL%s_SEW%s.log 2>&1' %(ins,vlen,i,j,ins,i,j)
            print("---------------------------------------------------------------")
            print(passing_string)
            print("---------------------------------------------------------------")
            os.system(passing_string)
            copy_this(ins,i,j)

def run_mask():
    pool = multiprocessing.Pool()
    pool.map(runcommand_mask, mask)

###################################################################################################################################################
################################################### FILES MANIPULATION UTILITIES ##################################################################
###################################################################################################################################################

def copy_this(i,l,s):
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):# or str(date.today() - timedelta(days = 1) #for processing last day file (regressive gen. can take time longer than a day
            instr = d.split('-')[2]
            read_sew = d.split('-')[4]
            read_lmul = d.split('-')[5]
            read_sew = read_sew[4:None]
            read_lmul = read_lmul[4:None]
            if (i==instr and l==read_lmul and s==read_sew):
                log_path = "%s/%s"%(d, 'spike_%s_final.log'%instr)
                if os.system("grep FAIL %s"%log_path) == 0:
                    print("###################################################################################################################################################")
                    print("Generated file is WRONG! : %s"%instr)
                    print("###################################################################################################################################################")
                    os.system('cp %s ./rv64uv/%s_LMUL%s_SEW%s.log'%(log_path,i,read_lmul,read_sew))
                    os.system('rm -r %s' %d)
                else:
                    elf = "%s/%s"%(d, 'ref_final.elf')
                    test_file = "%s/%s%s"%(d,instr,'_second.S')
                    os.system('cp %s ./generate_all/%s_LMUL%s_SEW%s.elf'%(elf, instr,read_lmul,read_sew))
                    os.system('cp %s ./rv64uv/%s_LMUL%s_SEW%s.S'%(test_file, instr,read_lmul,read_sew))
                    os.system('rm -r %s' %d)
def copy_this_load_store(i,l,s):
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):# or str(date.today() - timedelta(days = 1) #for processing last day file (regressive gen. can take time longer than a day
            instr = d.split('-')[2]
            read_sew = d.split('-')[4]
            read_lmul = d.split('-')[5]
            read_sew = read_sew[4:None]
            read_lmul = read_lmul[4:None]
            if (i==instr and l==read_lmul and s==read_sew):
                log_path = "%s/%s"%(d, 'spike_%s_final.log'%instr)
                if os.system("grep FAIL %s"%log_path) == 0:
                    print("###################################################################################################################################################")
                    print("Generated file is WRONG! : %s"%instr)
                    print("###################################################################################################################################################")
                    os.system('cp %s ./rv64uv/%s_LMUL%s_SEW%s.log'%(log_path,i,read_lmul,read_sew))
                    os.system('rm -r %s' %d)
                else:
                    elf = "%s/%s"%(d, 'ref_final.elf')
                    test_file = "%s/%s%s"%(d,instr,'_first.S')
                    os.system('cp %s ./generate_all/%s_LMUL%s_SEW%s.elf'%(elf, instr,read_lmul,read_sew))
                    os.system('cp %s ./rv64uv/%s_LMUL%s_SEW%s.S'%(test_file, instr,read_lmul,read_sew))
                    os.system('rm -r %s' %d)

def copy_all():
    dirs = os.listdir('.')
    for d in dirs:
        if d.startswith(str(date.today())[5:]):# or str(date.today() - timedelta(days = 1) #for processing last day file (regressive gen. can take time longer than a day
            instr = d.split('-')[2]
            read_sew = d.split('-')[4]
            read_lmul = d.split('-')[5]
            read_sew = read_sew[4:None]
            read_lmul = read_lmul[4:None]
            log_path = "%s/%s"%(d, 'spike_%s_final.log'%instr)
            if os.system("grep FAIL %s"%log_path) == 0:
                print("###################################################################################################################################################")
                print("Generated file is WRONG! : %s"%instr)
                print("###################################################################################################################################################")
                os.system('cp %s ./generate_all/%s_LMUL%s_SEW%s.log'%(log_path,log,read_lmul,read_sew))
            else:
                elf = "%s/%s"%(d, 'ref_final.elf')
                test_file = "%s/%s%s"%(d,instr,'_second.S')
                os.system('cp %s ./generate_all/%s_LMUL%s_SEW%s.elf'%(elf, instr,read_lmul,read_sew))
                os.system('cp %s ./rv64uv/%s_LMUL%s_SEW%s.S'%(test_file, instr,read_lmul,read_sew))
                os.system('rm -r %s' %d)

def makefrag():
    rv64uv_path = './rv64uv'
    makefrag_path = '%s/makefrag' %rv64uv_path
    os.system('touch %s' %makefrag_path)
    os.system('echo "#=======================================================================" > %s' %(makefrag_path))
    os.system('echo "# Makefrag for rv64uv tests" >> %s' %(makefrag_path))
    os.system('echo "#-----------------------------------------------------------------------" >> %s' %(makefrag_path))
    os.system('echo "rv64uv_sc_tests = \ " >> %s' %(makefrag_path))
    os.system('ls rv64uv | grep "\.S">> %s' %(makefrag_path))
    os.system("sed 's/\.S/ quswarabid/g' -i %s" %(makefrag_path))
    os.system("sed 's/quswarabid/\\\\/g' -i %s" %(makefrag_path))
    os.system('echo "\n" >> %s >> %s'%(makefrag_path,makefrag_path))
    os.system('echo "rv64uv_p_tests = \$(addprefix rv64uv-p-, \$(rv64uv_sc_tests))" >> %s' %(makefrag_path))
    os.system('echo "spike_tests = \$(rv64uv_p_tests)" >> %s' %(makefrag_path))


###################################################################################################################################################
######################################################### MAIN/ENTRY FUNCTION #####################################################################
###################################################################################################################################################
# Generate all and Put final ELF to a directory
def main():
    subprocess.run(["mkdir", "-p", 'generate_all'])
    subprocess.run(["mkdir", "-p", 'generate_all_logs'])
    subprocess.run(["mkdir", "-p", 'rv64uv'])
    setup_logging(True)
    # Modify here to choose which categories you want to generate
    #run_integer()
    #run_mask()
    run_floatingpoint()
    #run_fixpoint()
    #run_permute()
    #run_loadstore()
    makefrag()


if __name__ == "__main__":
    main()
