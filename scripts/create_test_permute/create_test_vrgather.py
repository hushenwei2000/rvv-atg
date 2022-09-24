import logging
import os
from scripts.test_common_info import *
import re

instr = 'vrgather'
rs1_val = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647, 2147483648, 2863311530, 4294967294, 4294967293, 4294967291, 4294967287, 4294967279, 4294967263, 4294967231, 4294967167, 4294967039, 4294966783, 4294966271, 4294965247, 4294963199, 4294959103, 4294950911, 4294934527, 4294901759, 4294836223, 4294705151, 4294443007, 4293918719, 4292870143, 4290772991, 4286578687, 4278190079, 4261412863, 4227858431, 4160749567, 4026531839, 3758096383, 3221225471]
rs2_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]


def generate_macros(f):
    for n in range(2,32):
        if n == 14:
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v1, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"%n + " \\\n\
            inst v14, v1, v%d;"%n+" \\\n\
        )",file=f)

    print("#define TEST_VV_OP_114( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v13, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v1, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v14, x7; \\\n\
            inst v13, v1, v14; \\\n\
        )",file=f)

    for n in range(3,32):
        print("#define TEST_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result,"%n + " \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v1, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v2, x7; \\\n\
            inst v%d, v1, v2;"%n+" \\\n\
        ) ",file=f)

    print("#define TEST_VV_OP_rd1( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v1, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v3, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v4, x7; \\\n\
            inst v1, v3, v4; \\\n\
        )",file=f)
    print("#define TEST_VV_OP_rd2( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v2, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v3, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v4, x7; \\\n\
            inst v2, v3, v4; \\\n\
        )",file=f)


def extract_operands(f):
    global rs1_val
    global rs2_val
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # VV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VV_OP( "+str(n)+",  %s.vv, "%instr+"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VX Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs1_val)):
        n += 1
        print( "  TEST_VX_OP( "+str(n)+",  %s.vx, "%instr +"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VI Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs1_val)):
        n += 1
        print( "  TEST_VI_OP( "+str(n)+",  %s.vi, "%instr +"5201314"+", "+str(rs2_val[i])+", 15 );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VV Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs1_val)):     
        k = i % 31 + 1
        n += 1
        print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)
        
        k = i % 30 + 2
        n += 1
        print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+str(rs2_val[i])+", "+str(rs1_val[i])+" );",file=f)


def create_empty_test_vrgather(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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
    generate_tests(f, rs1_val, rs2_val)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
