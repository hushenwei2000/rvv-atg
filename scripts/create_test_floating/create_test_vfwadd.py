import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *

instr = 'vfwadd'

def generate_tests(f, lmul):
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # VV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_FP_VV_OP( "+str(n)+",  %s.vv,  "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VF Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_FP_VF_OP( "+str(n)+",  %s.vf,  "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # WV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_FP_WV_OP( "+str(n)+",  %s.wv,  "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # WF Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_FP_WF_OP( "+str(n)+",  %s.wf,  "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 12 or k == 20 or k == 24: continue
        n += 1
        print("  TEST_W_FP_VV_OP_1%d( "%k+str(n)+",  %s.vv,  "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

        if k % (2*lmul) != 0 or k == 12 or k == 20 or k == 24: continue
        n += 1
        print("  TEST_W_FP_VV_OP_rd%d( "%k+str(n)+",  %s.vv,  "%instr+rs2_val[i]+", "+rs1_val[i]+" );",file=f)


def create_empty_test_vfwadd(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending(f, generate_data=False)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfwadd(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros_widen(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_widen(instr, f, vsew, lmul, test_wvwf = True)

    # Common const information
    print_common_ending_rs1rs2rd_wvwf(rs1_val, rs2_val, num_tests_tuple, vsew, f, generate_wvwf = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
