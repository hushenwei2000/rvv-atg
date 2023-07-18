import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsseg
from scripts.test_common_info import *
import re

name = 'vssege8'

instr = 'vsseg2e8'
instr1 = 'vlseg2e8'
instr2 = 'vsseg3e8' 
instr2l = 'vlseg3e8'
instr3 = 'vsseg4e8' 
instr3l = 'vlseg4e8'
instr4 = 'vsseg5e8' 
instr4l = 'vlseg5e8'
instr5 = 'vsseg6e8' 
instr5l = 'vlseg6e8'
instr6 = 'vsseg7e8' 
instr6l = 'vlseg7e8'
instr7 = 'vsseg8e8' 
instr7l = 'vlseg8e8' 


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
        if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+",  "+"0 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+",  "+"1 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+",  "+"2 + tdat"+");", file=f)
            n += 1
            print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+",  "+"3 + tdat"+");", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+",  "+"0 + tdat"+");", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+",  "+"0 + tdat"+");", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+",  "+"0 + tdat"+");", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+",  "+"0 + tdat"+");", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+",  "+"0 + tdat"+");", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"8"+", "+"0xa0"+",  "+"0xa0"+",  "+"0xa0"+",  "+"0 + tdat"+");", file=f)
        
        
    if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k % emul == 0 and k % lmul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul) and k + 2 * emul <= 32 and k!= 12 and k != 20 and k !=24: # (insn.rd() + nf * emul) <= NVPR
                n+=1
                print("  TEST_VSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+",  "+"0 + tdat"+" );",file=f)
        
            k = i%30+2
            if(k == 31 or k == 12 or k == 20 or k == 24):
                continue;
            n +=1
            print("   TEST_VSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xa0"+", "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)


    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vsseg(f, lmul, vsew, 8)

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
