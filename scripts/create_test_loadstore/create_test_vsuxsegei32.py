import logging
import os
from scripts.create_test_loadstore.create_test_common import generate_macros_vsuxseg
from scripts.test_common_info import *
import re

name = 'vsuxsegei32'

instr = 'vsuxseg2ei32'
instr1 = 'vluxseg2ei32'
instr2 = 'vsuxseg3ei32' 
instr2l = 'vluxseg3ei32'
instr3 = 'vsuxseg4ei32' 
instr3l = 'vluxseg4ei32'
instr4 = 'vsuxseg5ei32' 
instr4l = 'vluxseg5ei32'
instr5 = 'vsuxseg6ei32' 
instr5l = 'vluxseg6ei32'
instr6 = 'vsuxseg7ei32' 
instr6l = 'vluxseg7ei32'
instr7 = 'vsuxseg8ei32' 
instr7l = 'vluxseg8ei32' 

def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 32 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        if 2 * lmul <= 8 and 2 + 2 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
        if 3 * lmul <= 8 and 8 + 3 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
        if 4 * lmul <= 8 and 8 + 4 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
        if 5 * lmul <= 8 and 8 + 5 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
        if 6 * lmul <= 8 and 8 + 6 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
        if 7 * lmul <= 8 and 8 + 7 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
        if 8 * lmul <= 8 and 8 + 8 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)
            n += 1
            print("   TEST_VSXSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"32"+", "+"32 + tdat"+", "+"idx32dat"+", rd_origin_data);", file=f)   
     
    if 2 * lmul <= 8 and 2 + 2 * lmul <= 32: # (nf * lmul) <= (NVPR / 4) &&  (insn.rd() + nf * lmul) <= NVPR);
        for i in range(100):     
            k = i%31+1
            if k == 8 or k == 16 or k == 24:
                n+=1
                print("   TEST_VSXSEG1_OP_rd%d( "%k+str(n)+",  %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0 + tdat"+", "+"idx32dat"+", rd_origin_data);",file=f)
        
            k = i%30+2
            if(k == 31 or k == 12 or k == 20 or k == 24):
                continue;
            n +=1
            print("    TEST_VSXSEG1_OP_1%d( "%k+str(n)+",  %s.v, %s.v, "%(instr1,instr)+"32"+", "+"-12 + tdat4"+", "+"idx32dat"+", rd_origin_data);",file=f)
    return n



def create_empty_test_vsuxsegei32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vsuxsegei32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vsuxseg(f, lmul, vsew, 8)

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
