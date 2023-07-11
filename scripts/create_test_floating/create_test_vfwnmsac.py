import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *

instr = 'vfwnmsac'

def generate_tests(f, lmul):
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # VV Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_VV_OP_NEGRESULT( "+str(n)+",  %s.vv, fmul.d, 0xff100, "%instr+rs1_val[i]+", "+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # VF Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_W_FP_VF_OP_RV_NEGRESULT( "+str(n)+",  %s.vf, fmul.d, 0xff100, "%instr+rs1_val[i]+", "+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(rs2_val)):
        k = i % 31 + 1
        if k % lmul != 0: continue
        n += 1
        print("  TEST_W_FP_VV_OP_NEGRESULT_2%d( "%k+str(n)+",  %s.vv, fmul.d, "%instr+"0xff100, "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)

        if k % (2*lmul) != 0: continue
        n += 1
        print("  TEST_W_FP_VV_OP_NEGRESULT_rd%d( "%k+str(n)+",  %s.vv, fmul.d, "%instr+"0xff100, "+rs1_val[i]+", "+rs2_val[i]+" );",file=f)


def create_empty_test_vfwnmsac(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_W_FP_VV_OP_NEGRESULT( 1,  %s.vv, fmul.d, 0, 1, 1);"%instr, file=f)

    # Common const information
    print_ending(f, generate_data=False)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfwnmsac(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros_vfwmacc(f, vsew, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vfwmacc(instr, f, vsew, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_wvwf(rs1_val, rs2_val, num_tests_tuple, vsew, f, generate_wvwf = False)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
