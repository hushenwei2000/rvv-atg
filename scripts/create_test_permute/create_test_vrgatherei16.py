import logging
import os
from random import randint
from scripts.test_common_info import *
import re

instr = 'vrgatherei16'
rs1_val = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647, 2147483648, 2863311530, 4294967294, 4294967293, 4294967291, 4294967287, 4294967279, 4294967263, 4294967231, 4294967167, 4294967039, 4294966783, 4294966271, 4294965247, 4294963199, 4294959103, 4294950911, 4294934527, 4294901759, 4294836223, 4294705151, 4294443007, 4293918719, 4292870143, 4290772991, 4286578687, 4278190079, 4261412863, 4227858431, 4160749567, 4026531839, 3758096383, 3221225471]
rs2_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]


def generate_macros(f, lmul, vsew):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    rs1lmul = 2 if vsew == 8 else lmul # rs1_emul = (16 / vsew) * lmul
    for n in range(1,32):
        # no overlap: (rs1 + rs1lmul - 1 < rd) or (rs1 > rd + lmul - 1)
        if n == 24 or n == 16 or n == 8 or n % rs1lmul != 0 or (not (n + rs1lmul - 1 < 24 or n > 24 + lmul - 1)): # last condition is:(not( rs1 no overlap rd))
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v24, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"%n + " \\\n\
            inst v24, v16, v%d;"%n+" \\\n\
        )",file=f)

    print("#define TEST_VV_OP_124( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v16, v8, v24; \\\n\
        )",file=f)

    for n in range(1,32):
        if n == 24 or n == 16 or n == 8 or n % lmul != 0:
            continue
        if 16 + rs1lmul - 1 < n or 16 > n + lmul - 1:
            print("#define TEST_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE( testnum, v%d, result,"%n + " \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v16, x7; \\\n\
                inst v%d, v8, v16;"%n+" \\\n\
            ) ",file=f)

    print("#define TEST_VV_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v8, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v8, v16, v24; \\\n\
        )",file=f)
    print("#define TEST_VV_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v16, v8, v24; \\\n\
        )",file=f)


def extract_operands(f):
    global rs1_val
    global rs2_val
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    rs1lmul = (16 / vsew) * lmul
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VV_OP( "+str(n)+",  %s.vv, "%instr+"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):     
        k = i % 31 + 1
        if k != 8 and k != 16 and k != 24 and k % lmul == 0 and (16 + rs1lmul - 1 < k or 16 > k + lmul - 1):
            n += 1
            print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)
        
        k = i % 30 + 2
        if k != 24 and k != 16 and k != 8 and k % rs1lmul == 0 and (k + rs1lmul - 1 < 24 or k > 24 + lmul - 1):
            n += 1
            print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)


def create_empty_test_vrgatherei16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f)

    num_elem = int(vlen * lmul / vsew)
    # Add walking_val_grouped values, need at least num_elem
    for i in range(num_elem - len(rs2_val)):
        rs1_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
        rs2_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))

    # Generate macros to test diffrent register
    generate_macros(f, lmul, vsew)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, lmul, vsew)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
