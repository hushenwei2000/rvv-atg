import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *

instr = 'vfredosum'

def generate_tests(f, vsew, lmul):
    if vsew == 32:
        rs1_val = rs1_val
        rs2_val = rs2_val
    elif vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # VV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_FP_VV_OP( "+str(n)+",  %s.vs, 0xff100, 5201314, "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):     
        k = i % 31 + 1
        if k % lmul != 0 or k == 12 or k == 20 or k == 24: continue
        n += 1
        print("  TEST_FP_VV_OP_rd%d( "%k+str(n)+",  %s.vs, 0xff100, 5201314, "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

        n += 1
        print("  TEST_FP_VV_OP_1%d( "%k+str(n)+",  %s.vs, 0xff100, 5201314, "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)


def create_empty_test_vfredosum(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfredosum(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros_vfred(f, vsew, lmul, test_vv = True, test_vf = False)

    # Generate tests
    n = generate_tests_vfred(instr, f, vsew, lmul, suffix="vs", test_vv = True, test_vf = False)

    # Common const information
    print_ending(f, test_tuples=(0,n,0))

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
