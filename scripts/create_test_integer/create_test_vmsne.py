import logging
import os
from scripts.create_test_integer.create_test_common import extract_operands, generate_macros_vvmvxmvim,  generate_tests_vvmvxmvim
from scripts.test_common_info import *
import re

instr = 'vmsne'

def create_empty_test_vmsne(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    

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
    generate_macros_vvmvxmvim(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vvmvxmvim(instr, f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vvvxvi(rs1_val, rs2_val, num_tests_tuple, vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
