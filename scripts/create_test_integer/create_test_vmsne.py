import logging
import os
from scripts.test_common_info import *
import re

instr = 'vmsne'


def generate_macros(f):
    for n in range(2, 32):
        print("#define TEST_VVM_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_MASK( testnum, v14, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v2, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"%n + " \\\n\
            inst v14, v2, v%d; "%n + " \\\n\
        )", file=f)
    for n in range(3, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VVM_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
        TEST_CASE_MASK( testnum, v%d, result, "%n + "\\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v2, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v14, x7; \\\n\
            inst v%d, v2, v14; "%n + " \\\n\
        ) ", file=f)
    print("#define TEST_VVM_OP_rd1( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_MASK( testnum, v1, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v4, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v2, x7; \\\n\
            inst v1, v4, v2; \\\n\
        )", file=f)
    print("#define TEST_VVM_OP_rd2( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_MASK( testnum, v2, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v4, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v6, x7; \\\n\
            inst v2, v4, v6; \\\n\
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
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        n+=1
        # if(k==1 or k==2):
        #     continue;
        print("  TEST_VVM_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
        
        k = i%30+2
        # if(k==14):
        #     continue;
        n +=1
        print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n +=1
        print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
              instr+"5201314"+", "+rs1_val[i]+", "+"0x01"+" );", file=f)
   
    print("  #-------------------------------------------------------------", file=f)
  
    


def create_empty_test_vmsne(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("TEST_VVM_OP( 1, vmsne.vv, 5201314, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vmsne(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
