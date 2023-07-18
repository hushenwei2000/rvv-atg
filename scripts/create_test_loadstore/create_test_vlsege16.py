import logging
import os
from scripts.create_test_loadstore.create_test_common import extract_operands, generate_macros_vlseg
from scripts.test_common_info import *
import re

name = 'vlsege16'

instr = 'vlseg2e16'
instr1 = 'vlseg3e16'
instr2 = 'vlseg4e16'
instr3 = 'vlseg5e16'
instr4 = 'vlseg6e16'
instr5 = 'vlseg7e16'
instr6 = 'vlseg8e16'


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 16 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG1_OP( "+str(n)+",  %s.v, " %instr+" 16 "+", "+"0x00ff"+", "+"0 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSEG1_OP( "+str(n)+",  %s.v, " %instr+" 16 "+", "+"0x00ff"+", "+"2 + tdat"+" );", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 16 "+", "+"0x00ff"+", "+"0x00ff"+", "+"0xff00"+", "+"0 + tdat"+" );", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr2+" 16 "+", "+"0x0ff0"+", "+"0x0ff0"+", "+"0xf00f"+", "+"8 + tdat"+" );", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr3+" 16 "+", "+"0x00ff"+", "+"0x00ff"+", "+"0xff00"+", "+"-12 + tdat4"+" );", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr4+" 16 "+", "+"0x00ff"+", "+"0x00ff"+", "+"0xff00"+", "+"0 + tdat"+" );", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr5+" 16 "+", "+"0x00ff"+", "+"0x00ff"+", "+"0xff00"+", "+"0 + tdat"+" );", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 16 "+", "+"0x00ff"+", "+"0x00ff"+", "+"0xff00"+", "+"0 + tdat"+" );", file=f)
        

    if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32 and k!= 12 and k != 20 and k !=24: # (insn.rd() + nf * emul) <= NVPR
                n+=1
                print("  TEST_VLSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 16 "+", "+"0x00ff"+", "+"0 + tdat"+" );",file=f)
            
            k = i%30+2
            if(k == 31  or k == 12 or k == 20 or k == 24):
                continue;
            n +=1
            print("  TEST_VLSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 16 "+", "+"0xff00"+", "+"4 + tdat"+" );",file=f)
    


def create_empty_test_vlsege16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vlsege16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlseg(f, lmul, vsew=vsew, eew=16)

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
