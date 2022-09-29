import logging
import os
from scripts.test_common_info import *
import re

instr = 'vwmaccus'


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_W_VX_OP_RV_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE_W( testnum, v24, result, \\\n\
                li x7, 0; \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v24, x7; \\\n\
                VSET_VSEW \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x%d, MASK_XLEN(val1); "%n + " \\\n\
                inst v24, x%d, v8; "%n + " \\\n\
        )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % (lmul*2) != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_W_VX_OP_RV_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE_W( testnum, v%d, result, "%n + "\\\n\
            li x7, 0; \\\n\
            VSET_DOUBLE_VSEW \\\n\
            vmv.v.x v%d, x7; "%n + "\\\n\
            VSET_VSEW \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x1, MASK_XLEN(val1);  \\\n\
            inst v%d, x1, v8; "%n + " \\\n\
        )",file=f)
   



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


def generate_tests(f, rs1_val, rs2_val, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul*2) != 0:
            continue
        n+=1
        if k%2==0:
            print("  TEST_W_VX_OP_RV_rd%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_W_VX_OP_RV_1%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)



def create_empty_test_vwmaccus(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_W_VX_OP_RV( 1, vwmaccus.vx, 2, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vwmaccus(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
