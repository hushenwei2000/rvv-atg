import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vlxei
from scripts.test_common_info import *
import re

instr = 'vluxei8'


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 8 / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
       

    for i in range(100):     
        k = i%31+1
        if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul):
            n+=1
            print("  TEST_VLXEI_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0x0ff00ff0"+", "+"0xf00ff00f"+" , "+"-8 + tdat4"+", "+"idx8dat"+" );",file=f)
        
        k = i%30+2
        if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul):
            n +=1
            print("  TEST_VLXEI_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+" , "+"0 + tdat"+", "+"idx8dat"+" );",file=f)
    


def create_empty_test_vluxei8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print(" TEST_VLXEI_OP( 2, vluxei8.v, 8, 0x00ff00ff, 0xff00ff00, 0  + tdat , idx8dat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vluxei8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlxei(f, vsew, lmul)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_loaddword_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
