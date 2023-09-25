import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vlxeiseg
from scripts.test_common_info import *
import re

name = 'vluxsegei8'

instr  = 'vluxseg2ei8'
instr1 = 'vluxseg3ei8'
instr2 = 'vluxseg4ei8'
instr3 = 'vluxseg5ei8'
instr4 = 'vluxseg6ei8'
instr5 = 'vluxseg7ei8'
instr6 = 'vluxseg8ei8'

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
        if 2 * lmul <= 8 and 2 + 3 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+"0 + tdat"+" , "+"idx8dat"+");", file=f)
        if 3 * lmul <= 8 and 8 + 3 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+("0x"+tdats[2*int(-vsew/4):int(-vsew/4)])+", "+("0x"+tdats[3*int(-vsew/4):2*int(-vsew/4)])+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        if 4 * lmul <= 8 and 8 + 4 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr2+" 8 "+", "+("0x"+tdats[int(-vsew/4)-32:-32])+", "+("0x"+tdats[2*int(-vsew/4)-32:int(-vsew/4)-32])+", "+("0x"+tdats[3*int(-vsew/4)-32:2*int(-vsew/4)-32])+", "+"16 + tdat"+", "+"idx8dat"+" );", file=f)
        if 5 * lmul <= 8 and 8 + 5 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr3+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+("0x"+tdats[2*int(-vsew/4):int(-vsew/4)])+", "+("0x"+tdats[3*int(-vsew/4):2*int(-vsew/4)])+","+"-12 + tdat4"+", "+"idx8dat"+" );", file=f)
        if 6 * lmul <= 8 and 8 + 6 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr4+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+("0x"+tdats[2*int(-vsew/4):int(-vsew/4)])+", "+("0x"+tdats[3*int(-vsew/4):2*int(-vsew/4)])+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        if 7 * lmul <= 8 and 8 + 7 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr5+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+("0x"+tdats[2*int(-vsew/4):int(-vsew/4)])+", "+("0x"+tdats[3*int(-vsew/4):2*int(-vsew/4)])+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        if 8 * lmul <= 8 and 8 + 8 * lmul <= 32:
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+("0x"+tdats[2*int(-vsew/4):int(-vsew/4)])+", "+("0x"+tdats[3*int(-vsew/4):2*int(-vsew/4)])+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
            n += 1
            print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+("0x"+tdats[int(-vsew/4):])+", "+("0x"+tdats[2*int(-vsew/4):int(-vsew/4)])+", "+("0x"+tdats[3*int(-vsew/4):2*int(-vsew/4)])+", "+"4100 + tdat"+", "+"idx8dat"+" );", file=f)
        

    if 2 * lmul <= 8 and 2 + 2 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
        for i in range(100):     
            k = i%30+1
            if k != 8 and k != 16 and k % lmul == 0 and k % emul == 0 and k + 2 * lmul <= 32 and not is_overlap(k, lmul*2, 8, emul) and k!= 12 and k != 20 and k !=24:
                n+=1
                print("   TEST_VLXSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+"8"+", "+("0x"+tdats[int(-vsew/4):])+", "+"0 + tdat"+", "+"idx8dat"+");",file=f)
            
            k = i%30+2
            if( k == 12 or k == 20 or k == 24):
                continue;
            n +=1
            print("  TEST_VLXSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+"8"+", "+("0x"+tdats[int(-vsew/4):])+", "+"0 + tdat"+", "+"idx8dat"+" );",file=f)
    


def create_empty_test_vluxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vluxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vlxeiseg(f, lmul, vsew, 8)

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
