import os
from scripts.constants import *

vsews = [8, 16, 32, 64]
data_types = {8:".byte", 16:".hword", 32:".word", 64:".dword"}
lmuls = [0.125, 0.25, 0.5, 1, 2, 4, 8]
lmul_nums = {0.125:"0125", 0.25:"025", 0.5:"05", 1:"1", 2:"2", 4:"4", 8:"8"}

include = '#include "model_test.h"\n\
#include "arch_test.h"\n\
#include "riscv_test.h"\n\
#include "test_macros_vector.h"\n'

prolog = 'RVTEST_ISA("RV64RV64IMAFDCVZicsr")\n\
    .section .text.init\n\
    .globl rvtest_entry_point\n\
    rvtest_entry_point:\n\
    \n\
    #ifdef TEST_CASE_1\n\
    \n\
    RVTEST_CASE(0,"//check ISA:=regex(.*64.*);check ISA:=regex(.*V.*);def TEST_CASE_1=True;",vadd)\n\
    \n\
    RVTEST_RV64UV\n\
    RVMODEL_BOOT\n\
    RVTEST_CODE_BEGIN\n\
    VSET_VSEW_4AVL\n\
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)\n'

before_data = '    TEST_PASSFAIL\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n'

epilog = '    signature_x12_0:\n\
        .fill 0,4,0xdeadbeef\n\
    \n\
    signature_x12_1:\n\
        .fill 32,4,0xdeadbeef\n\
    \n\
    signature_x20_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    signature_x20_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    signature_x20_2:\n\
        .fill 376,4,0xdeadbeef\n\
    \n\
    #ifdef rvtest_mtrap_routine\n\
    \n\
    mtrap_sigptr:\n\
        .fill 128,4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    #ifdef rvtest_gpr_save\n\
    \n\
    gpr_save:\n\
        .fill 32*(XLEN/32),4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    RVTEST_DATA_END'

def test_generator(cwd, xlen, flen, vlen, elen, vsew, lmul, output_dir):
    if (vsew > elen * lmul):
        print("Error parameters!")
        return
    
    mask = xlen - vsew
    data_type = data_types[vsew]
    lmul_num = lmul_nums[lmul]
    
    suffix = "vsew" + str(vsew) + "_lmul" + lmul_num
    print(suffix)
    asspath = output_dir + "/" + suffix + ".S"
    elfpath = output_dir + "/" + suffix + ".elf"
    logpath = output_dir + "/" + suffix + ".log"

    elenum = int(vlen * lmul / vsew)
    dmax = (elenum << 1) - 1

    with open(asspath, 'w') as f:
        print(include, file=f)
        print(prolog, file=f)

        # generate test assembly code
        print("la x7, rs1_data", file=f)
        print("vle{}.v v8, (x7) // get first vector".format(vsew), file=f)
        print("\n", file=f)
        print("li x8, 0x4", file=f)
        print("vmul.vx v16, v8, x8 // RAW", file=f)
        print("vsub.vv v24, v16, v8 // RAW", file=f)
        print("\n", file=f)

        for k in range(0, elenum):
            t = ((dmax - k) * 3) & ((1 << vsew) - 1) # mask
            if(k != 0):
                print("vslidedown.vi  v24, v24, 1 // vd[i] = vs[i+1]", file=f)
            print("vmv.x.s x5, v24 // x[rd] = vs[0]", file=f)
            print("slli x5, x5, {:#X} // mask".format(mask), file=f)
            print("srli x5, x5, {:#X} // mask".format(mask), file=f)
            print("li x6, {:#X}".format(t), file=f)
            print("bne x5, x6, fail", file=f)

        print("\n", file=f)
        print("la x7, rs1_data", file=f)
        print("vle{}.v v8, (x7) // get first vector".format(vsew), file=f)
        print("la x7, rs2_data", file=f)
        print("vle{}.v v16, (x7) // get second vector".format(vsew), file=f)
        print("\n", file=f)
        print("vsll.vi v24, v16, 2 // RAW", file=f)
        print("vadd.vv v16, v8, v8 // WAR", file=f)
        print("vadd.vv v16, v8, v24 // WAW", file=f)
        print("\n", file=f)

        for k in range(0, elenum):
            t = ((k << 2) + (dmax - k)) & ((1 << vsew) - 1) # mask
            if(k != 0):
                print("vslidedown.vi v16, v16, 1", file=f)
            print("vmv.x.s x5, v16", file=f)
            print("slli x5, x5, {:#X}".format(mask), file=f)
            print("srli x5, x5, {:#X}".format(mask), file=f)
            print("li x6, {:#X}".format(t), file=f)
            print("bne x5, x6, fail", file=f)

        print("\n", file=f)
        print(before_data, file=f)
        # data
        print(".align {}".format(int(vsew/8)), file=f)
        print("rs1_data:", file=f)
        for k in range(dmax, (elenum - 1), -1):
            print("{}	{:#X}".format(data_type, k), file=f)
        print("rs2_data:", file=f)
        for k in range(0, elenum):
            print("{}	{:#X}".format(data_type, k), file=f)

        print("\n", file=f)
        print(epilog, file=f)

    # run test
    gcc = GCC_CONST
    use_fail_macro = False
    gcc_string = "%s -march=rv64gv    -w     -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles         -T %s/env/p/link.ld         -I %s/env/macros/vsew%d_lmul%s%s         -I %s/env/p         -I %s/env         -I %s/env/sail_cSim -mabi=lp64  %s -o %s -DTEST_CASE_1=True -DXLEN=%d -DFLEN=%d;" %(gcc, cwd, cwd, vsew, lmul_num, ("" if use_fail_macro else "_nofail"), cwd, cwd, cwd, asspath, elfpath, xlen, flen)
    print(gcc_string)
    re = os.system(gcc_string)
    print(re)
    spike_string = "spike --isa rv64gcv_zfh -l --log-commits --varch=vlen:%d,elen:%d %s > %s 2>&1;" %(vlen, elen, elfpath, logpath)
    print(spike_string)
    re = os.system(spike_string)
    print(re)


# test all
def ctest_all(cwd, xlen, flen, vlen, elen, output):
    for i in range (0, len(vsews)):
        for j in range (0, len(lmuls)):
            if (vsews[i] > elen * lmuls[j]):
                continue
            test_generator(cwd, xlen, flen, vlen, elen, vsews[i], lmuls[j], output)
