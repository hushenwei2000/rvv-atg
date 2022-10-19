import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsse
from scripts.test_common_info import *
import re

instr = 'vsse32'
instr1 = 'vlse32'

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 32 / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"4"+", "+"4 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"8"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"4"+", "+"12 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"4100"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"-4100"+", "+"0 + tdat15"+");", file=f)
   
    for i in range(100):     
        k = i%30+1
        if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul):
            n+=1
            print("  TEST_VSSE_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"0"+", "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VSSE_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0aa00"+", "+"0"+", "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vsse32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print(" TEST_VSSE_OP( 18, vlse32.v, vsse32.v, 32, 0x00aa00aa, 4, 0  + tdat ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vsse32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vsse(f)

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
