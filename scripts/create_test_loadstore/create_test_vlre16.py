import logging
import os
from scripts.create_test_loadstore.create_test_common import *
from scripts.test_common_info import *
import re
import numpy as np

name = 'vlre16'


def create_empty_test_vlre16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Common const information

    # Load const information
    print_loadlr_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlre16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Generate macros to test diffrent register
    generate_vlre_macro(f, lmul)

    # Generate tests
    n =  generate_tests_vlre(f, vsew, 16, lmul)

    # Common const information

    # Load const information
    print_loadlr_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
