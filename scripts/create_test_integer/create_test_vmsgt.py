import logging
import os
from scripts.test_common_info import *
import re

instr = 'vmsgt'


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        print("#define TEST_VXM_OP_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE_MASK( testnum, v24, result,  \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7;  \\\n\
            li x%d, MASK_XLEN(val2);"%n + " \\\n\
            inst v24, v8, x%d; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        print("#define TEST_VXM_OP_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE_MASK( testnum, v%d, result, "%n + "\\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x1, MASK_XLEN(val2); \\\n\
            inst v%d, v8, x1; "%n + " \\\n\
        ) ", file=f)
    print("#define TEST_VXM_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK( testnum, v8, result, \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x1, MASK_XLEN(val2); \\\n\
            inst v8, v16, x1; \\\n\
        )", file=f)
    print("#define TEST_VXM_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK( testnum, v24, result, \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x1, MASK_XLEN(val2); \\\n\
            inst v24, v8, x1; \\\n\
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


def generate_tests(f, rs1_val, rs2_val, lmul, vsew):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k == 0 or k == 24 or k % (lmul * 2) != 0:
            continue
        n+=1
        print("  TEST_VXM_OP_rd%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0:
            continue
        n +=1
        print("  TEST_VXM_OP_1%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs1_val[i]+" , "+rs2_val[i]+");",file=f)

    if vsew == 8:
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 101, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 10, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 12, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -86);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 101);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 10);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 12);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -86, 3);", file=f)
    elif vsew == 16:
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 26213, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 180, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 182, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -21846);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 26213);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 180);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 182);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -21846, 3);", file=f)
    elif vsew == 32:
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 1717986917, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 46339, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 46341, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -1431655766);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 1717986917);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 46339);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 46341);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -1431655766, 3);", file=f)
    elif vsew == 64:
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3037000498, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3037000500, 3);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 7378697629483820645);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 3037000498);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 3037000500);", file=f)
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -6148914691236517206, 3);", file=f)

    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
              instr+"5201314"+", "+rs1_val[i]+", "+" 4 "+" );", file=f)
        


def create_empty_test_vmsgt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VXM_OP( 1, vmsgt.vx, 2, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vmsgt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val, lmul, vsew)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
