import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macro_vssseg, generate_macros_vsseg
from scripts.test_common_info import *
import re

name = 'vsssege8'

instr = 'vssseg2e8'
instr1 = 'vlsseg2e8'
instr2 = 'vssseg3e8' 
instr2l = 'vlsseg3e8'
instr3 = 'vssseg4e8' 
instr3l = 'vlsseg4e8'
instr4 = 'vssseg5e8' 
instr4l = 'vlsseg5e8'
instr5 = 'vssseg6e8' 
instr5l = 'vlsseg6e8'
instr6 = 'vssseg7e8' 
instr6l = 'vlsseg7e8'
instr7 = 'vssseg8e8' 
instr7l = 'vlsseg8e8' 

def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    emul = 8 / vsew * lmul
    emul = 1 if emul < 1 else int(emul) 
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        if 2 * emul <= 8 and 2 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"4100"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"-4100"+", "+"0 + tdat15"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"1 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"1 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"1 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"1 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"2 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"2 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"2 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"2 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+", "+"3 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"1"+", "+"3 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"2"+", "+"3 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"3"+", "+"3 + tdat"+");", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        
        
    for i in range(100):     
        k = i%30+1
        if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32: # (insn.rd() + nf * emul) <= NVPR
            n+=1
            print("   TEST_VSSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"0"+",  "+"0 + tdat"+");",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("    TEST_VSSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"8"+",  "+"0 + tdat"+");",file=f)



def create_empty_test_vsssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print("  TEST_VSSSEG1_OP( 3, vlsseg2e8.v, vssseg2e8.v, 8, 0x0f, 1,  12 + tdat  ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vsssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macro_vssseg(f, lmul, vsew, 8)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, lmul, vsew)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
