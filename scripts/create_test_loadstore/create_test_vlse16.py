import logging
import os
from scripts.test_common_info import *
import re

instr = 'vlse16'


def generate_macros(f):
    for n in range(2, 30):
        if n == 12 or n == 20 or n == 24 or n == 30: # signature base registers
            continue
        print("#define TEST_VLSE_OP_1%d( testnum, inst, eew, result1, result2, stride, base )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v16, x0,  \\\n\
                la  x%d, base; "%n + "\\\n\
                li  x30, stride; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v16, (x%d), x30; "%n + "\\\n\
                VSET_VSEW \\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLSE_OP_rd%d( testnum, inst, eew, result1, result2, stride, base )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, x0, "%n + "\\\n\
                la  x1, base; \\\n\
                li  x2, stride; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v%d, (x1), x2; "%n + "\\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    print("#define TEST_VLSE_OP_130( testnum, inst, eew, result1, result2, stride, base ) \\\n\
            TEST_CASE_LOOP( testnum, v16, x0,  \\\n\
                la  x30, base; \\\n\
                li  x2, stride; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v16, (x30), x2; \\\n\
                VSET_VSEW \\\n\
        )", file=f)



def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    emul = 16 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return 0
    emul = 1 if emul < 1 else int(emul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  %s.v, " %
              instr+" 16 "+", "+"0x00ff"+", "+"0x00ff"+" , "+"2"+" , "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  %s.v, " %
              instr+" 16 "+", "+"0x00ff"+", "+"0xff00"+" , "+"2"+" , "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  %s.v, " %
              instr+" 16 "+", "+"0xf00f"+", "+"0xf00f"+" , "+"0"+" , "+"2 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  %s.v, " %
              instr+" 16 "+", "+"0x00ff"+", "+"0xff00"+" , "+"4096"+" , "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  %s.v, " %
              instr+" 16 "+", "+"0xff00"+", "+"0x0000"+" , "+"-4096"+" , "+"0 + tsdat7"+" );", file=f)

    for i in range(100):     
        k = i%31+1
        n+=1
        if( k % lmul == 0 and k % emul == 0 and k % lmul == 0 and k != 31 and k != 12 and k != 20 and k != 24):
            print("  TEST_VLSE_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 16 "+", "+"0xf00f"+", "+"0x0ff0"+" , "+" -4 "+" , "+"2 + tdat4"+");",file=f)
        
        k = i%30+2
        if(k == 31  or k == 12 or k == 20 or k == 24):
            continue;
        n +=1
        print("  TEST_VLSE_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 16 "+", "+"0x00ff"+", "+"0x00ff"+" , "+" 2 "+" , "+"0 + tdat"+");",file=f)
    return n


def create_empty_test_vlse16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information

    # Load const information
    print_loadls_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vlse16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    n = generate_tests(f, rs1_val, rs2_val, lmul, vsew)

    # Common const information

    # Load const information
    print_loadls_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
