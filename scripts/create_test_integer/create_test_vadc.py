import logging
import os
from scripts.test_common_info import *
from scripts.create_test_integer.create_test_common import extract_operands
import re

instr = 'vadc'


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_ADC_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v24, result, \\\n\
            li x7, 0; \\\n\
            vmv.v.x v8, x7; \\\n\
            vmsne.vi v0, v8, 0; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v%d, x7;"%n + " \\\n\
            inst v24, v8, v%d, v0; "%n + " \\\n\
        )", file=f)
    for n in range(3, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_ADC_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result,"%n + " \\\n\
            li x7, 0; \\\n\
            vmv.v.x v8, x7; \\\n\
            vmsne.vi v0, v8, 0; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            inst v%d, v8, v16, v0;"%n+" \\\n\
        ) ",file=f)
    print("#define TEST_ADC_VV_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE( testnum, v8, result, \\\n\
        li x7, 0; \\\n\
        vmv.v.x v8, x7; \\\n\
        vmsne.vi v0, v8, 0; \\\n\
        li x7, MASK_VSEW(val1); \\\n\
        vmv.v.x v16, x7; \\\n\
        li x7, MASK_VSEW(val2); \\\n\
        vmv.v.x v24, x7; \\\n\
        inst v8, v16, v24, v0; \\\n\
        )", file = f)
    print("#define TEST_ADC_VV_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE( testnum, v16, result, \\\n\
        li x7, 0; \\\n\
        vmv.v.x v16, x7; \\\n\
        vmsne.vi v0, v16, 0; \\\n\
        li x7, MASK_VSEW(val1); \\\n\
        vmv.v.x v8, x7; \\\n\
        li x7, MASK_VSEW(val2); \\\n\
        vmv.v.x v24, x7; \\\n\
        inst v16, v8, v24, v0; \\\n\
        )", file = f)


def generate_tests(f, rs1_val, rs2_val, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_ADC_VV_OP( "+str(n)+",  %s.vvm, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k == 24 or k % lmul != 0:
            continue
        n+=1
        print("  TEST_ADC_VV_OP_rd%d( "%k+str(n)+",  %s.vvm, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_ADC_VV_OP_1%d( "%k+str(n)+",  %s.vvm, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_ADC_VX_OP( "+str(n)+",  %s.vxm, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_ADC_VI_OP( "+str(n)+",  %s.vim, " %
              instr+"5201314"+", "+rs1_val[i]+", "+" 4 "+" );", file=f)
    


def create_empty_test_vadc(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_ADC_VV_OP( 1, vadc.vvm, 2, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    # os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vadc(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
    generate_tests(f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
