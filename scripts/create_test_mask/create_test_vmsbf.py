import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vmsbf'


def generate_macros_vmsbf(f):
    # generate the macro， test rs1 = v1~v31
    print("#define TEST_VSFMB_OP_rs2_5( testnum, inst, result, src1_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        vle32.v v6, (x1); \\\n\
        vmseq.vi v5, v6, 1; \\\n\
        inst v14, v5; \\\n\
        VSET_VSEW \\\n\
    )", file=f)
    print("#define TEST_VSFMB_OP_rs2_14( testnum, inst, result, src1_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v5, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        vle32.v v6, (x1); \\\n\
        vmseq.vi v14, v6, 1; \\\n\
        inst v5, v14; \\\n\
        VSET_VSEW \\\n\
    )", file=f)
    for n in range(1, 32):
        if n == 5 or n == 14:
            continue
        print("#define TEST_VSFMB_OP_rs2_%d( testnum, inst, result, src1_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle32.v v5, (x1); \\\n\
            vmseq.vi v%d, v5, 1; \\\n\
            inst v14, v%d; \\\n\
            VSET_VSEW \\\n\
        )" % (n, n, n), file=f)
    # generate the macro， test rd = v1~v31
    print("#define TEST_VSFMB_OP_rd_1( testnum, inst, result, src1_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v1, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle32.v v5, (x1); \\\n\
            vmseq.vi v2, v5, 1; \\\n\
            inst v1, v2; \\\n\
            VSET_VSEW \\\n\
        )", file=f)
    for n in range(2, 32):
        print("#define TEST_VSFMB_OP_rd_%d( testnum, inst, result, src1_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v%d, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle32.v v5, (x1); \\\n\
            vmseq.vi v1, v5, 1; \\\n\
            inst v%d, v1; \\\n\
            VSET_VSEW \\\n\
        )" % (n, n, n), file=f)


def generate_tests_vmsbf(instr, f, vlen, vsew):
    num_test = 1
    num_elem = int(vlen / vsew)
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

    for i in range(1, 32):
        print("TEST_VSFMB_OP_rd_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, instr, i % 5), file=f)
        num_test = num_test + 1
    for i in range(1, 32):
        print("TEST_VSFMB_OP_rs2_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, instr, i % 5), file=f)
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

    for i in range(1, 32):
        print("TEST_VSFMB_OP_rd_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, "vmsif", i % 5), file=f)
        num_test = num_test + 1
    for i in range(1, 32):
        print("TEST_VSFMB_OP_rs2_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, "vmsif", i % 5), file=f)
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

    for i in range(1, 32):
        print("TEST_VSFMB_OP_rd_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, "vmsof", i % 5), file=f)
        num_test = num_test + 1
    for i in range(1, 32):
        print("TEST_VSFMB_OP_rs2_%d( %d,  %s.m,  5201314, walking_zeros_dat%d );" % (
            i, num_test, "vmsof", i % 5), file=f)
        num_test = num_test + 1


def create_empty_test_vmsbf(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vmsbf(f)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vmsbf(instr, f, vlen, vsew)

    # Common const information
    print_ending_common(vlen, vsew, f)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
