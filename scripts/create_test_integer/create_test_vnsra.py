import logging
import os
from scripts.test_common_info import *
import re

instr = 'vnsra'


def generate_macros(f):
    for n in range(2, 32):
        print("#define TEST_N_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE( testnum, v14, MASK_VSEW(result), \\\n\
            li x7, SEXT_DOUBLE_VSEW(val2); \\\n\
            vmv.v.x v2, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"% n + " \\\n\
            inst v14, v2, v%d; "%n + " \\\n\
        )", file=f)
    for n in range(3, 32):
        if n %2 == 0:
            print("#define TEST_N_VV_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE( testnum, v%d, MASK_VSEW(result),"%n + " \\\n\
                li x7, SEXT_DOUBLE_VSEW(val2); \\\n\
                vmv.v.x v1, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v2, x7; \\\n\
                inst v%d, v1, v2;"%n+" \\\n\
        ) ", file=f)
    
    print("#define TEST_N_VV_OP_rd2( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v2, MASK_VSEW(result), \\\n\
            li x7, SEXT_DOUBLE_VSEW(val2); \\\n\
            vmv.v.x v4, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v3, x7; \\\n\
            inst v2, v3, v4; \\\n\
        )", file=f)


def extract_operands(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    rs1_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs1_val_10]
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    rs2_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs2_val_10]
    f.close()
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_N_VV_OP( "+str(n)+",  %s.wv, " %
              instr+"0x5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        n+=1
        if k%2 == 0 or k == 2:
            print("  TEST_N_VV_OP_rd%d( "%k+str(n)+",  %s.wv, "%instr+"0x5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        # if(k==14):
        #     continue;
        n +=1
        print("  TEST_N_VV_OP_1%d( "%k+str(n)+",  %s.wv, "%instr+"0x5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_N_VX_OP( "+str(n)+",  %s.wx, " %
              instr+"0x5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_N_VI_OP( "+str(n)+",  %s.wi, " %
              instr+"0x5201314"+", "+rs1_val[i]+", "+" 4 "+" );", file=f)
    


def create_empty_test_vnsra(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_N_VV_OP( 1, vnsra.wv, 2, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vnsra(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

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