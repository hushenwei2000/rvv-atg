import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macro_vssseg, generate_macros_vsseg
from scripts.test_common_info import *
import re

name = 'vsssege16'

instr = 'vssseg2e16'
instr1 = 'vlsseg2e16'
instr2 = 'vssseg3e16' 
instr2l = 'vlsseg3e16'
instr3 = 'vssseg4e16' 
instr3l = 'vlsseg4e16'
instr4 = 'vssseg5e16' 
instr4l = 'vlsseg5e16'
instr5 = 'vssseg6e16' 
instr5l = 'vlsseg6e16'
instr6 = 'vssseg7e16' 
instr6l = 'vlsseg7e16'
instr7 = 'vssseg8e16' 
instr7l = 'vlsseg8e16' 


def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    emul = 16 / vsew * lmul
    emul = 1 if emul < 1 else int(emul) 
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        if 2 * emul <= 8 and 2 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"4100"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"-4100"+", "+"0 + tdat15"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+", "+"2 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"2"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"2"+", "+"2 + tdat"+");", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        
        
    for i in range(100):     
        k = i%31+1
        if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32: # (insn.rd() + nf * emul) <= NVPR
            n+=1
            print("   TEST_VSSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+",  "+"0 + tdat"+");",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("    TEST_VSSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"16"+",  "+"0 + tdat"+");",file=f)



def create_empty_test_vsssege16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print("  TEST_VSSSEG1_OP(11, vlsseg2e16.v, vssseg2e16.v, 16, 0x0ff0, 2,  8  + tdat  ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vsssege16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macro_vssseg(f, lmul, vsew, 16)

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
