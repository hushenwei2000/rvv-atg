from glob import glob
import logging
import os
from scripts.test_common_info import *
import re

instr = 'vmv'
rs1_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -
               17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]
rs2_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -
               17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]


def generate_macros(f):
    for n in range(1,32):
        print("#define TEST_VMV_OP_rs2_%d( testnum, result )"%n + " \\\n\
            li TESTNUM, testnum; \\\n\
            li x7, MASK_VSEW(result);" + " \\\n\
            li x8, 0; \\\n\
            vmv.s.x v%d, x7; "%n + " \\\n\
            vmv.x.s x8, v%d;"%n + " \\\n\
            li x2, VSEW_MASK_BITS; \\\n\
            and x8, x8, x2;",
        file=f)


def extract_operands(f):
    global rs1_val
    global rs2_val
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_VMV_OP( "+str(n)+",  "+str(rs2_val[i])+" );", file=f)

    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VMV_OP( "+str(n)+",  "+str(rs1_val[i])+" );", file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # VMV Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs2_val)):     
        k = i % 31 + 1
        n += 1
        print("  TEST_VMV_OP_rs2_%d( "%k+str(n)+", "+str(rs2_val[i])+" );",file=f)
    return n


def create_empty_test_vmv(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f)

    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    n = generate_tests(f, rs1_val, rs2_val)

    # Common const information
    print_common_ending(f, arr=[0,n,0])
    
    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
