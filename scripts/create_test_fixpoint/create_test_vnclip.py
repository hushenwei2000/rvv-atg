import logging
import os
from scripts.test_common_info import *
from scripts.create_test_fixpoint.create_test_common import *
import re

instr = 'vnclip'


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
  


def create_empty_test_vnclip(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_W_AVG_WV_OP( 1,  vnclip.wv, 0x0, 0x0, 0x0000, 0x000, 0x00, 0x00 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vnclip(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vnclip(f, lmul)

    # Generate tests
    generate_tests_vnclip(f, rs1_val, rs2_val, instr, lmul)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
