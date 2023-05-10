import logging
import os
from scripts.create_test_floating.create_test_common import rs1_val, rs2_val
from scripts.create_test_random.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vadd'

def create_first_test_war(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    generate_init_vregs(f)

    # Generate tests
    print("TEST_CASE_LOOP(1, v2, rd_data, \\\n\
    vsub.vv v24, v8, v16, v0.t; \\\n\
        li x28, 2345; \\\n\
        vmul.vx v25, v24, x28; \\\n\
        vadd.vv v2, v25, v24; \\\n\
    )", file=f)

    # Common const information
    print_common_ending_random(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
