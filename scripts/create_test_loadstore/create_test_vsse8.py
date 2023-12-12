import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsse
from scripts.test_common_info import *
import re

instr = 'vsse8'
instr1 = 'vlse8'

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 8 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"1 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"1 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"1 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"1 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"3 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"3 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"3 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"3 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"4096"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"-4096"+", "+"0 + tdat15"+");", file=f)
        
    for i in range(100):     
        k = i%30+1
        if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul) and k!= 12 and k != 20 and k !=24 and k!= 29 and k != 30:
            n+=1
            print("  TEST_VSSE_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31  or k == 12 or k == 20 or k == 24 or k == 29 or k == 30):
            continue;
        n +=1
        print("  TEST_VSSE_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0x0a"+", "+"3"+", "+"-8 + tdat8"+" );",file=f)
    return n



def create_empty_test_vsse8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information

    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vsse8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
    n = generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information

    # Load const information
    print_load_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
