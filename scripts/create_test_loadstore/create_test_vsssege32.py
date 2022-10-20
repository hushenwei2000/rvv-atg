import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vssseg
from scripts.test_common_info import *
import re

name = 'vsssege32'

instr = 'vssseg2e32'
instr1 = 'vlsseg2e32'
instr2 = 'vssseg3e32' 
instr2l = 'vlsseg3e32'
instr3 = 'vssseg4e32' 
instr3l = 'vlsseg4e32'
instr4 = 'vssseg5e32' 
instr4l = 'vlsseg5e32'
instr5 = 'vssseg6e32' 
instr5l = 'vlsseg6e32'
instr6 = 'vssseg7e32' 
instr6l = 'vlsseg7e32'
instr7 = 'vssseg8e32' 
instr7l = 'vlsseg8e32' 

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 32 / vsew * lmul
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
        if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"4100"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"-4100"+", "+"0 + tdat15"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"0"+", "+"4 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"4"+", "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"4"+", "+"4 + tdat"+");", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        
        
    if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul) and k + 2 * emul <= 32: # (insn.rd() + nf * emul) <= NVPR
                n+=1
                print("   TEST_VSSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"0"+",  "+"0 + tdat"+");",file=f)
        
            k = i%30+2
            if(k == 31):
                continue;
            n +=1
            print("    TEST_VSSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"32"+",  "+"0 + tdat"+");",file=f)



def create_empty_test_vsssege32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vsssege32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vssseg(f, lmul, vsew ,32)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
