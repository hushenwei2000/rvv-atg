import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vse
from scripts.test_common_info import *
import re

instr = 'vse16'
instr1 = 'vle16'

def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    n = 1
    emul = 16 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    emul = 1 if emul < 1 else int(emul)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("  TEST_VSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+" 8 "+", "+"0xff"+",  "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+" 8 "+", "+"0xff"+",  "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+" 8 "+", "+"0xff"+",  "+"4100 + tdat"+" );", file=f)
    for i in range(100):     
        k = i%30+1
        if k != 8 and k != 16 and k % emul == 0 and k!= 12 and k != 20 and k !=24:
            n+=1
            print("  TEST_VSE_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xaa"+",  "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31  or k == 12 or k == 20 or k == 24):
            continue;
        n +=1
        print("  TEST_VSE_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0x00"+",  "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vse16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vse16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vse(f, lmul, vsew, 16)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, lmul, vsew)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
