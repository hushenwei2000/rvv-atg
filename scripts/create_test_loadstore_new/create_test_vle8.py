import logging
import os
from scripts.create_test_loadstore_new.create_test_common import generate_macros_load_vx_offset,generate_macros_load_vx_Nregs, print_load_ending_new, generate_results_load_vlsseg_Nregs
from scripts.test_common_info import *
import re

name = 'vle8'



def generate_tests(f, vsew, lmul):
    emul = 8 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1):

        for n in range(1,32):
            if emul <= 8 and n + emul <= 32 and n % emul == 0:
                print("  TEST_LOAD_V%dX7_offset( " %(n)+str(n)+",  vle8.v );", file=f)
        for n in range(1,32):
            if emul <= 8 and n + emul <= 32 and n % emul == 0:      
                print("  TEST_LOAD_V%dXFF_offset( " %(n)+str(n+32)+",  vle8ff.v );", file=f)
        for n in range(5,31):
            if emul <= 8 and 2 + emul <= 32 and 2 % emul == 0 and n != 7:
                print("  TEST_LOAD_V2X%d_offset( " %(n)+str(n+64)+",  vle8.v );", file=f)

        


    
def create_empty_test_vle8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Generate macros to test diffrent register
    for i in range(1,32):
        generate_macros_load_vx_offset(f, 8, 0, i, 7); 
    for i in range(5,31):
        generate_macros_load_vx_offset(f, 8, 0, 2, i); 

    # Generate tests
    generate_tests(f, vsew, lmul)

    print_load_ending_new(f, 8, 1, is_vx = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
