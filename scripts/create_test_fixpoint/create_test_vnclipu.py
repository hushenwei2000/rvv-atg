import logging
import os
from scripts.test_common_info import *
import re

instr = 'vnclipu'


def generate_macros(f):
    for n in range(1, 32):
            print("#define TEST_W_AVG_WV_OP_1%d( testnum, inst, result00, result01, result10, result11, val2, val1 ) "%n + " \\\n\
            TEST_CASE_AVG_VV( testnum, inst, v%d, v14, result00, result01, result10, result11, "%n + " \\\n\
                li x7, MASK_DOUBLE_VSEW(val2); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v2, x7; \\\n\
                VSET_VSEW  \\\n\
                li x7, val1; \\\n\
                vmv.v.x v1, x7; \\\n\
            )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_W_AVG_WV_OP_rd%d( testnum, inst, result00, result01, result10, result11, val2, val1 ) "%n + " \\\n\
            TEST_CASE_AVG_VV( testnum, inst, v4, v%d, result00, result01, result10, result11, "%n + " \\\n\
                li x7, MASK_DOUBLE_VSEW(val2); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v2, x7; \\\n\
                VSET_VSEW  \\\n\
                li x7, val1; \\\n\
                vmv.v.x v1, x7; \\\n\
        ) ", file=f)



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
    print("  # WV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_AVG_WV_OP( "+str(n)+",  %s.wv, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        n+=1
        print("  TEST_W_AVG_WV_OP_rd%d( "%k+str(n)+",  %s.wv, "%instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        # if(k==14):
        #     continue;
        n +=1
        print("  TEST_W_AVG_WV_OP_1%d( "%k+str(n)+",  %s.wv, "%instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # WX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_AVG_WX_OP( "+str(n)+",  %s.wx, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # WI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_AVG_WI_OP( "+str(n)+",  %s.wi, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+" 4 "+" );", file=f)
  


def create_empty_test_vnclipu(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_W_AVG_WV_OP( 1,  vnclipu.wv, 0x0, 0x0, 0x0000, 0x000, 0x00, 0x00 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vnclipu(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
