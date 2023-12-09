import logging
import os
from scripts.create_test_loadstore.create_test_common import extract_operands, generate_macros_vlseg
from scripts.test_common_info import *
import re

name = 'vlsege32'

instr = 'vlseg2e32'
instr1 = 'vlseg3e32'
instr2 = 'vlseg4e32'
instr3 = 'vlseg5e32'
instr4 = 'vlseg6e32'
instr5 = 'vlseg7e32'
instr6 = 'vlseg8e32'


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 32 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG2_OP( "+str(n)+",  %s.v, " %instr+" 32 "+", "+"0 + tdat"+" );", file=f)
            n += 1
            print("  TEST_VLSEG2_OP( "+str(n)+",  %s.v, " %instr+" 32 "+", "+"4 + tdat"+" );", file=f)
        if 3 * emul <= 8 and 8 + 3 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 32 "+", "+"0 + tdat"+" );", file=f)
        if 4 * emul <= 8 and 8 + 4 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG4_OP( "+str(n)+",  %s.v, " %instr2+" 32 "+", "+"8 + tdat"+" );", file=f)
        if 5 * emul <= 8 and 8 + 5 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG5_OP( "+str(n)+",  %s.v, " %instr3+" 32 "+", "+"-12 + tdat4"+" );", file=f)
        if 6 * emul <= 8 and 8 + 6 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG6_OP( "+str(n)+",  %s.v, " %instr4+" 32 "+", "+"0 + tdat"+" );", file=f)
        if 7 * emul <= 8 and 8 + 7 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG7_OP( "+str(n)+",  %s.v, " %instr5+" 32 "+", "+"0 + tdat"+" );", file=f)
        if 8 * emul <= 8 and 8 + 8 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
            n += 1
            print("  TEST_VLSEG8_OP( "+str(n)+",  %s.v, " %instr6+" 32 "+", "+"0 + tdat"+" );", file=f)
        
    if 2 * emul <= 8 and 2 + 2 * emul <= 32: # (nf * emul) <= (NVPR / 4) &&  (insn.rd() + nf * emul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k != 8 and k != 16 and k % emul == 0 and k + 2 * emul <= 32 and k!= 12 and k != 20 and k !=24: # (insn.rd() + nf * emul) <= NVPR
                n+=1
                print("  TEST_VLSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+"0 + tdat"+" );",file=f)
            
            k = i%30+2
            if(k == 31 or k == 12 or k == 20 or k == 24):
                continue;
            n +=1
            print("  TEST_VLSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+"4 + tdat"+" );",file=f)
    return n
    


def create_empty_test_vlsege32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Common const information

    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlsege32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlseg(f, lmul, vsew, 32)

    # Generate tests
    n = generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information

    # Load const information
    print_load_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
