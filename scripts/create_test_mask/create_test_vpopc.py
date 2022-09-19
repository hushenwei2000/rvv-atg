import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vpopc'
num_elem = 0


def generate_walking_data_seg_vpopc(f):
    # Generate walking ones
    n = 0
    for i in range(num_elem + 1):
        print("walking_ones_dat_vpopc%d:"%n, file=f)
        print(".word\t0b", end="", file=f)
        print(i * "0", end="", file=f)
        print("1", end="", file=f)
        print((num_elem - i - 1) * "0", end="", file=f)
        print("", file=f)
        print(".word\t0x0\n.word\t0x0\n.word\t0x0\n", file=f)
        n = n + 1

    for j in range(num_elem):
        print("walking_zeros_dat_vpopc%d:"%n, file=f)
        print(".word\t0b", end="", file=f)
        print(i * "1", end="", file=f)
        print("0", end="", file=f)
        print((num_elem - i - 1) * "1", end="", file=f)
        print("", file=f)
        print(".word\t0x0\n.word\t0x0\n.word\t0x0\n", file=f)
        n = n + 1


def generate_macros_vpopc(f, vsew):
    # generate the macro， 测试v1-v32源寄存器
    print("#define TEST_VPOPC_OP_rs2_1( testnum, inst, result, vm_addr ) \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x2, vm_addr; \\\n\
        vle%d.v v1, (x2); \\\n\
        li x7, result; \\\n\
        li TESTNUM, testnum; \\\n\
        inst x14, v1; \\\n\
        VSET_VSEW \\\n\
        bne x14, x7, fail;"%vsew, file=f)

    for n in range(2,32):
        print("#define TEST_VPOPC_OP_rs2_%d( testnum, inst, result, vm_addr ) \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x2, vm_addr; \\\n\
            vle%d.v v%d, (x2); \\\n\
            li x7, result; \\\n\
            li TESTNUM, testnum; \\\n\
            inst x14, v%d; \\\n\
            VSET_VSEW \\\n\
            bne x14, x7, fail;" % (n, vsew, n, n), file=f)

    for n in range(1,31):
        print("#define TEST_VPOPC_OP_rd_%d( testnum, inst, result, vm_addr ) \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x2, vm_addr; \\\n\
            vle%d.v v14, (x2); \\\n\
            li x7, result; \\\n\
            li TESTNUM, testnum; \\\n\
            inst x%d, v14; \\\n\
            VSET_VSEW \\\n\
            bne x%d, x7, fail;" % (n, vsew, n, n), file=f)

    print("#define TEST_VPOPC_OP_rd_31( testnum, inst, result, vm_addr ) \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x2, vm_addr; \\\n\
            vle%d.v v14, (x2); \\\n\
            li x7, result; \\\n\
            li TESTNUM, testnum; \\\n\
            inst x31, v14; \\\n\
            vsetivli x30, 1, e32, tu, mu; \\\n\
            bne x31, x7, fail;"%vsew, file=f)


def generate_tests_vpopc(f, num_elem):
    num_test = 1
    ########################vmpopc#################################################################################################
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s tests" % isa,file=f)
    print("  #-------------------------------------------------------------",file=f)
    for i in range(0, 2 * num_elem + 2):
        print("TEST_VPOPC_OP( %d, vpopc.m, 5201314, walking_dat_vpopc%d );" % (num_test, i), file=f)
        num_test = num_test + 1


    #generate registers，覆盖不同寄存器
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)" % isa,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    for i in range(1, 32):
        print("TEST_VPOPC_OP_rd_%d( %d, vpopc.m, 5201314, walking_dat_vpopc%d );" % (i, num_test, (i % (2 * num_elem + 2))), file=f)
        num_test = num_test + 1
    print()
    for i in range(1, 32):
        print("TEST_VPOPC_OP_rs2_%d( %d, vpopc.m, 5201314, walking_dat_vpopc%d );" % (i, num_test, (i % (2 * num_elem + 2))), file=f)
        num_test = num_test + 1
        
    #########################vfirst####################################################################################################
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfirst tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    for i in range(0, 2 * num_elem + 2):
        print("TEST_VPOPC_OP( %d, vfirst.m, 5201314, walking_dat_vpopc%d );" % (num_test, i), file=f)
        num_test = num_test + 1

    #generate registers，覆盖不同寄存器
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfirst Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    for i in range(1, 32):
        print("TEST_VPOPC_OP_rd_%d( %d, vfirst.m, 5201314, walking_dat_vpopc%d );" % (i, num_test, (i % (2 * num_elem + 2))), file=f)
        num_test = num_test + 1
    print()
    for i in range(2, 32):
        print("TEST_VPOPC_OP_rs2_%d( %d, vfirst.m, 5201314, walking_dat_vpopc%d );" % (i, num_test, (i % (2 * num_elem + 2))), file=f)
        num_test = num_test + 1



def print_ending_vpopc(vlen, vsew, f):
    # generate const information
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
        \n\
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
    ", file=f)

    generate_walking_data_seg_vpopc(f)

    print("signature_x12_0:\n\
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


def create_empty_test_vpopc(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    global num_elem
    num_elem = int(vlen / vsew)
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vpopc(f)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vpopc(instr, f, vlen, vsew)

    # Common const information
    print_ending_vpopc(vlen, vsew, f)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
