import os
import re
from scripts.test_common_info import print_mask_origin_data_ending, print_data_width_prefix

def generate_init_vregs(f):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    lmul_double = lmul * 2
    lmul_double_1 = 1 if lmul_double < 1 else int(lmul_double)
    
    print("VSET_VSEW_4AVL \n", file=f)
    for i in range(1, 32, lmul_1):
        print("la x7, rd_origin_data+%d; \n  vle%d.v v%d, (x7); \n"%(i * 8, vsew, i), file=f)
    print("la x7, mask_data; \n  vle%d.v v0, (x7); \n  "%vsew, file=f)
    
            
def print_common_ending_random(f, rd_data_multiplier = 1):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
        \n\
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)\n\
    TEST_PASSFAIL\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    ", file=f)
    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)

    print("rd_data:", file=f)
    for i in range(num_elem_1):
        print_data_width_prefix(f, vsew)
        print("0x5201314", file=f)

    print_mask_origin_data_ending(f)

    print("\n\
    signature_x12_0:\n\
        .fill 0,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x12_1:\n\
        .fill 32,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
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
    RVTEST_DATA_END\n\
    ", file=f)
