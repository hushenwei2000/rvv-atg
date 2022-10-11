import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsseg
from scripts.test_common_info import *
import re

name = 'vssege32'

instr = 'vsseg2e32'
instr1 = 'vlseg2e32'
instr2 = 'vsseg3e32' 
instr2l = 'vlseg3e32'
instr3 = 'vsseg4e32' 
instr3l = 'vlseg4e32'
instr4 = 'vsseg5e32' 
instr4l = 'vlseg5e32'
instr5 = 'vsseg6e32' 
instr5l = 'vlseg6e32'
instr6 = 'vsseg7e32' 
instr6l = 'vlseg7e32'
instr7 = 'vsseg8e32' 
instr7l = 'vlseg8e32' 

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 32 / vsew * lmul
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        if 2 * emul <= 8 and 2 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0"+",  "+"4 + tdat"+");", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"32"+", "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"32"+", "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"32"+", "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"32"+", "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"32"+", "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1 
            print("  TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"32"+", "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0xa0a0a0"+",  "+"0 + tdat"+");", file=f)
        
        
    for i in range(100):     
        k = i%30+1
        if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32: # (insn.rd() + nf * emul) <= NVPR
            n+=1
            print("  TEST_VSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0"+",  "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("   TEST_VSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0"+", "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vssege32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print("  TEST_VSSEG1_OP(19, vlseg2e32.v, vsseg2e32.v, 32, 0x00ff00ff, 0  + tdat  ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vssege32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vsseg(f, lmul, vsew, 32)

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
