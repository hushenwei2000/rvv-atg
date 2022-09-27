import logging
import os
from scripts.test_common_info import *
import re

instr = 'vlse16'


def generate_macros(f):
    for n in range(2, 30):
        print("#define TEST_VLSE_OP_1%d( testnum, inst, eew, result1, result2, stride, base )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v14, eew, result1, result2, \\\n\
                la  x%d, base; "%n + "\\\n\
                li  x30, stride; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v14, (x%d), x30; "%n + "\\\n\
                VSET_VSEW \\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLSE_OP_rd%d( testnum, inst, eew, result1, result2, stride, base )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v%d, eew, result1, result2, "%n + "\\\n\
                la  x1, base; \\\n\
                li  x2, stride; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v%d, (x1), x2; "%n + "\\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    print("#define TEST_VLSE_OP_130( testnum, inst, eew, result1, result2, stride, base ) \\\n\
            TEST_CASE_LOAD( testnum, v14, eew, result1, result2, \\\n\
                la  x30, base; \\\n\
                li  x2, stride; \\\n\
                vsetivli x31, 4, MK_EEW(eew), tu, mu; \\\n\
                inst v14, (x30), x2; \\\n\
                VSET_VSEW \\\n\
        )", file=f)


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


def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
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
              instr+" 16 "+", "+"0x00ff"+", "+"0xff00"+" , "+"4100"+" , "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSE_OP( "+str(n)+",  %s.v, " %
              instr+" 16 "+", "+"0xff00"+", "+"0x0000"+" , "+"-4100"+" , "+"0 + tsdat7"+" );", file=f)

    for i in range(100):     
        k = i%31+1
        n+=1
        print("  TEST_VLSE_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 16 "+", "+"0xf00f"+", "+"0x0ff0"+" , "+" -4 "+" , "+"2 + tdat4"+");",file=f)
        
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VLSE_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 16 "+", "+"0x00ff"+", "+"0x00ff"+" , "+" 2 "+" , "+"0 + tdat"+");",file=f)
    


def create_empty_test_vlse16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print(" TEST_VLSE_OP( 10, vlse16.v, 16, 0x00ff, 0x00ff, 2, 0  + tdat );", file=f)

    # Common const information
    #print_common_ending(f)
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
    generate_tests(f, rs1_val, rs2_val)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_loadls_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
