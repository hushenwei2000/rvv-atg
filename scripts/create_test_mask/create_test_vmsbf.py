import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vmsbf'


def generate_macros_vmsbf(f, vsew, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    # generate the macro， test rs1 = v1~v31
    print("#define TEST_VSFMB_OP_rs2_8( testnum, inst, result, src1_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        vle%d.v v16, (x1); \\\n\
        vmseq.vi v8, v16, 1; \\\n\
        inst v14, v8; \\\n\
        VSET_VSEW \\\n\
    )"%vsew, file=f)
    print("#define TEST_VSFMB_OP_rs2_14( testnum, inst, result, src1_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v5, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        vle%d.v v8, (x1); \\\n\
        vmseq.vi v14, v8, 1; \\\n\
        inst v5, v14; \\\n\
        VSET_VSEW \\\n\
    )"%vsew, file=f)
    for n in range(1, 32):
        # no overlap: (v8 + lmul - 1 < rd) or (rd + lmul - 1 < 8)
        if n == 8 or n == 14 or (8 + lmul - 1 >= n and n + lmul - 1 >= 8):
            continue
        print("#define TEST_VSFMB_OP_rs2_%d( testnum, inst, result, src1_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle%d.v v8, (x1); \\\n\
            vmseq.vi v%d, v8, 1; \\\n\
            inst v14, v%d; \\\n\
            VSET_VSEW \\\n\
        )" % (n, vsew, n, n), file=f)
    # generate the macro， test rd = v1~v31
    print("#define TEST_VSFMB_OP_rd_1( testnum, inst, result, src1_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v1, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle%d.v v8, (x1); \\\n\
            vmseq.vi v2, v8, 1; \\\n\
            inst v1, v2; \\\n\
            VSET_VSEW \\\n\
        )"%vsew, file=f)
    for n in range(2, 32):
        print("#define TEST_VSFMB_OP_rd_%d( testnum, inst, result, src1_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v%d, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle%d.v v8, (x1); \\\n\
            vmseq.vi v1, v8, 1; \\\n\
            inst v%d, v1; \\\n\
            VSET_VSEW \\\n\
        )" % (n, n, vsew, n), file=f)


def generate_tests_vmsbf(instr, f, vlen, vsew, lmul):
    # lmul = 1 if lmul < 1 else int(lmul)
    num_test = 1
    num_elem = int(vlen * lmul / vsew)
    num_elem_plus = num_elem + 1
    ####################vmsbf#######################################################################################################
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    for i in range(0, num_elem_plus):
        print("TEST_VSFMB_OP( %d,  %s.m,  5201314, walking_ones_dat%d );" %
              (num_test, instr, i), file=f)
        num_test = num_test + 1
        print("TEST_VSFMB_OP( %d,  %s.m,  5201314, walking_zeros_dat%d);" %
              (num_test, instr, i), file=f)
        num_test = num_test + 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)


    for i in range(1, 32):
        # Ensure is_aligned(insn.rd(), vemul), vemul = veew / (vsew * vflmul); ,veew always = sew in this test generation
        if i % (lmul) != 0:
            continue
        print("TEST_VSFMB_OP_rd_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, instr, i % num_elem_plus), file=f)
        num_test = num_test + 1
    for i in range(1, 32):
        if 8 + lmul - 1 < i or i + lmul - 1 < 8: # rs2 and rd no overlap each other
            print("TEST_VSFMB_OP_rs2_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
                i, num_test, instr, i % num_elem_plus), file=f)
            num_test = num_test + 1

    ####################vmsif#######################################################################################################
    print("  #-------------------------------------------------------------", file=f)
    print("  # vmsif tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    for i in range(0, num_elem_plus):
        print("TEST_VSFMB_OP( %d,  %s.m,  5201314, walking_ones_dat%d );" %
              (num_test, "vmsif", i), file=f)
        num_test = num_test + 1
        print("TEST_VSFMB_OP( %d,  %s.m,  5201314, walking_zeros_dat%d);" %
              (num_test, "vmsif", i), file=f)
        num_test = num_test + 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # vmsif Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)


    for i in range(1, 32):
        print("TEST_VSFMB_OP_rd_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, "vmsif", i % num_elem_plus), file=f)
        num_test = num_test + 1
    for i in range(1, 32):
        if 8 + lmul - 1 < i or i + lmul - 1 < 8: # rs2 and rd no overlap each other
            print("TEST_VSFMB_OP_rs2_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
                i, num_test, "vmsif", i % num_elem_plus), file=f)
            num_test = num_test + 1

    ####################vmsof#######################################################################################################
    print("  #-------------------------------------------------------------", file=f)
    print("  # vmsof tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    for i in range(0, num_elem_plus):
        print("TEST_VSFMB_OP( %d,  %s.m,  5201314, walking_ones_dat%d );" %
              (num_test, "vmsof", i), file=f)
        num_test = num_test + 1
        print("TEST_VSFMB_OP( %d,  %s.m,  5201314, walking_zeros_dat%d);" %
              (num_test, "vmsof", i), file=f)
        num_test = num_test + 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # vmsof Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)


    for i in range(1, 32):
        print("TEST_VSFMB_OP_rd_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, "vmsof", i % num_elem_plus), file=f)
        num_test = num_test + 1
    for i in range(1, 32):
        if 8 + lmul - 1 < i or i + lmul - 1 < 8: # rs2 and rd no overlap each other
            print("TEST_VSFMB_OP_rs2_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
                i, num_test, "vmsof", i % num_elem_plus), file=f)
            num_test = num_test + 1
            
    return num_test


def create_empty_test_vmsbf(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vmsbf(f, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_vmsbf(instr, f, vlen, vsew, lmul)

    # Common const information
    print_ending_common(vlen, vsew, lmul, f, n)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
