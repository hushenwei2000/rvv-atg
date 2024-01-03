import logging
import os
import numpy as np
from scripts.create_test_loadstore.create_test_common import *
from scripts.test_common_info import *
import re


name = 'vlre8'
instr = 'vl1re8'
instr1 = 'vl2re8'
instr2 = 'vl4re8'
instr3 = 'vl8re8'
instr4 = 'vl2r'

def create_empty_test_vlre8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)


    # Common const information

    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlre8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)
     
    # Generate macros to test diffrent register
    generate_vlre_macro(f, lmul)
    
    # Generate tests
    n = generate_tests_vlre(f, vsew, 8, lmul)

    # Common const information

    # Load const information
    print_loadlr_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
