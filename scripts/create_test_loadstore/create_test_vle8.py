import logging
import os
from scripts.test_common_info import *
import re

instr = 'vle8'


def generate_macros(f):
    for n in range(2, 31):
        if n == 12 or n == 20 or n == 24: # signature base registers
            continue
        print("#define TEST_VLE_OP_1%d( testnum, inst, eew, result1, result2, base )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v8, x0,   \\\n\
                la  x%d, base; "%n + "\\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v8, (x%d); "%n + "\\\n\
                VSET_VSEW \\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLE_OP_rd%d( testnum, inst, eew, result1, result2, base )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, x0,  "%n + "\\\n\
                la  x8, base; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v%d, (x8); "%n + "\\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    


def extract_operands(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    rs1_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs1_val_10]
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    rs2_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs2_val_10]
    f.close()
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    emul = 8 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    emul = 1 if emul < 1 else int(emul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0xff"+", "+"0x00"+" , "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0x00"+", "+"0xff"+" , "+"4 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0x00"+", "+"0xff"+" , "+"1 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0xff"+", "+"0x00"+" , "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0x00"+", "+"0x00"+" , "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %sff.v, " %
              instr+" 8 "+", "+"0xff"+", "+"0x00"+" , "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0xff"+", "+"0x00"+" , "+"4096 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLE_OP( "+str(n)+",  %s.v, " %
              instr+" 8 "+", "+"0xff"+", "+"0x00"+" , "+"-4096 + tdat10"+" );", file=f)     
        
    for i in range(100):     
        k = i%31+1
        n+=1
        if( k % lmul == 0 and k % emul == 0 and k != 12 and k != 20 and k != 24):
            print("  TEST_VLE_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0x00"+", "+"0xff"+" , "+"4 + tdat"+");",file=f)
        
        k = i%30+2
        if(k == 31 or k == 12 or k == 20 or k == 24):
            continue;
        n +=1
        print("  TEST_VLE_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0xff"+", "+"0x00"+" , "+"0 + tdat"+");",file=f)
    return n
    


def create_empty_test_vle8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vle8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
    print_load_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
