import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsuxei
from scripts.test_common_info import *
import re

instr = 'vsuxei8'
instr1 = 'vluxei8'


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 8 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("  TEST_VSXEI_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0x00ff00ff"+",  "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        
    for i in range(100):     
        k = i%30+1
        if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16, 24] and not is_overlap(k, lmul, 8, emul) and k!= 12 and k != 20 and k !=24:
            n+=1
            print("  TEST_VSXEI_OP_rd%d( "%k+str(n)+",  %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0x00ff00ff"+",  "+"0 + tdat"+", "+"idx8dat"+" );",file=f)
    
        k = i%30+2
        if(k == 31 or k == 12 or k == 20 or k == 24):
            continue;
        n +=1
        print("  TEST_VSXEI_OP_1%d( "%k+str(n)+",  %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0x00ff00ff"+", "+"-12 + tdat4"+", "+"idx8dat"+" );",file=f)



def create_empty_test_vsuxei8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print(" TEST_VSXEI_OP( 2, vluxei8.v, vsuxei8.v, 8, 0x00aa00aa, 0  + tdat , idx8dat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vsuxei8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vsuxei(f)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
