import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vlxeiseg
from scripts.test_common_info import *
import re

name = 'vluxsegei16'

instr  = 'vluxseg2ei16'
instr1 = 'vluxseg3ei16'
instr2 = 'vluxseg4ei16'
instr3 = 'vluxseg5ei16'
instr4 = 'vluxseg6ei16'
instr5 = 'vluxseg7ei16'
instr6 = 'vluxseg8ei16'

# tdat1:  .word 0x00ff00ff
# tdat2:  .word 0xff00ff00
# tdat3:  .word 0x0ff00ff0
# tdat4:  .word 0xf00ff00f
# tdat5:  .word 0x00ff00ff
# tdat6:  .word 0xff00ff00
# tdat7:  .word 0x0ff00ff0
# tdat8:  .word 0xf00ff00f
tdats = "f00ff00f0ff00ff0ff00ff0000ff00fff00ff00f0ff00ff0ff00ff0000ff00ff" # consequence: "87654321"

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 16 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        if 2 * lmul <= 8 and 2 + 3 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG2_OP( "+str(n)+",  %s.v, " %instr+" 16 "+", "+"0 + tdat"+" , "+"idx16dat"+");", file=f)
        if 3 * lmul <= 8 and 8 + 3 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 16 "+", "+"0 + tdat"+", "+"idx16dat"+" );", file=f)
        if 4 * lmul <= 8 and 8 + 4 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG4_OP( "+str(n)+",  %s.v, " %instr2+" 16 "+", "+"16 + tdat"+", "+"idx16dat"+" );", file=f)
        if 5 * lmul <= 8 and 8 + 5 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG5_OP( "+str(n)+",  %s.v, " %instr3+" 16 "+", "+"-12 + tdat4"+", "+"idx16dat"+" );", file=f)
        if 6 * lmul <= 8 and 8 + 6 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG6_OP( "+str(n)+",  %s.v, " %instr4+" 16 "+", "+"0 + tdat"+", "+"idx16dat"+" );", file=f)
        if 7 * lmul <= 8 and 8 + 7 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG7_OP( "+str(n)+",  %s.v, " %instr5+" 16 "+", "+"0 + tdat"+", "+"idx16dat"+" );", file=f)
        if 8 * lmul <= 8 and 8 + 8 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG8_OP( "+str(n)+",  %s.v, " %instr6+" 16 "+", "+"0 + tdat"+", "+"idx16dat"+" );", file=f)
            n += 1
            print("  TEST_VLXSEG8_OP( "+str(n)+",  %s.v, " %instr6+" 16 "+", "+"4096 + tdat"+", "+"idx16dat"+" );", file=f)
        

    if 2 * lmul <= 8 and 2 + 2 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k != 8 and k != 16 and k % lmul == 0 and k % emul == 0 and k % lmul == 0 and k + 2 * lmul <= 32 and not is_overlap(k, lmul*2, 8, emul) and k!= 12 and k != 20 and k !=24:
                n+=1
                print("   TEST_VLXSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+"16"+", "+"0 + tdat"+", "+"idx16dat"+");",file=f)
            
            k = i%30+2
            if(  k == 12 or k == 20 or k == 24):
                continue;
            n +=1
            print("  TEST_VLXSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+"16"+", "+"0 + tdat"+", "+"idx16dat"+" );",file=f)
    
    return n


def create_empty_test_vluxsegei16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vluxsegei16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlxeiseg(f, lmul, vsew, 16)

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
