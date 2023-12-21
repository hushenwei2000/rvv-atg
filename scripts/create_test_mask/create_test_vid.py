import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vid'


def generate_walking_answer_seg_vid(element_num, vlen, vsew, f):
    # Generate prefix-sum of 1 for WalkingOnes
    vma = os.environ["RVV_ATG_VMA"]
    agnostic_type = int(os.environ['RVV_ATG_AGNOSTIC_TYPE'])
    if vma == "True" and agnostic_type == 1:
        for i in range(element_num + 1):
            print("walking_ones_vid_ans%d:" % i, file=f)
            vid = 0
            for j in range(element_num):
                print("\t", end="", file=f)
                print_data_width_prefix(f, vsew)
                if i != j + 1:
                    print("0x1", file=f)  # print(vd[j])
                else:
                    print(j, file=f)
            print("", file=f)

        # Generate prefix-sum of 1 for WalkingZeros
        for i in range(element_num + 1):
            print("walking_zeros_vid_ans%d:" % i, file=f)
            vid = 0
            for j in range(element_num):
                print("\t", end="", file=f)
                print_data_width_prefix(f, vsew)
                if i == j + 1:
                    print("0x1", file=f)  # print(vd[j])
                else:
                    print(j, file=f)
            print("", file=f)
    else:
        for i in range(element_num + 1):
            print("walking_ones_vid_ans%d:" % i, file=f)
            vid = 0
            for j in range(element_num):
                print("\t", end="", file=f)
                print_data_width_prefix(f, vsew)
                if i != j + 1:
                    print("0x0", file=f)  # print(vd[j])
                else:
                    print(j, file=f)
            print("", file=f)
    
        # Generate prefix-sum of 1 for WalkingZeros
        for i in range(element_num + 1):
            print("walking_zeros_vid_ans%d:" % i, file=f)
            vid = 0
            for j in range(element_num):
                print("\t", end="", file=f)
                print_data_width_prefix(f, vsew)
                if i == j + 1:
                    print("0x0", file=f)  # print(vd[j])
                else:
                    print(j, file=f)
            print("", file=f)

def generate_macros_vid(f, vsew, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    # generate the macro， 测试v1-v32源寄存器
    for n in range(1, 32):
        if n == 16 or n % lmul != 0:
            continue
        print("#define TEST_VID_OP_rd_%d( testnum, inst,  src1_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v%d,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            vle%d.v v8, (x1); \\\n\
            vmseq.vi v0, v8, 1; \\\n\
            vmv.v.i v%d, 2;\\\n\
            inst v%d, v0.t; \\\n\
        )" % (n, n, vsew, n ,n), file=f)


def generate_tests_vid(instr, f, vlen, vsew, lmul):
    num_test = 1
    num_elem = int(vlen * lmul / vsew)
    lmul = 1 if lmul < 1 else int(lmul)
    num_elem_plus = num_elem + 1
    ####################vid######################################################################################################
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    for i in range(0, num_elem_plus):
        print("TEST_VID_OP( %d,  %s.v, walking_ones_dat%d );" % (
            num_test, instr, i), file=f)
        num_test = num_test + 1
        print("TEST_VID_OP( %d,  %s.v, walking_zeros_dat%d);" % (
            num_test, instr, i), file=f)
        num_test = num_test + 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1, 32):
        if i == 16 or i % lmul != 0:
            continue
        print("TEST_VID_OP_rd_%d( %d,  %s.v, walking_zeros_dat%d );" % (
            i, num_test, instr, i % num_elem_plus), file=f)
        num_test = num_test + 1
    return num_test


def print_ending_vid(vlen, vsew, lmul, f, n):
    # generate const information
    print(" #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    ", file=f)

    generate_walking_data_seg_common(int(vlen * lmul/vsew), int(vlen), int(vsew), f)
    generate_walking_answer_seg_vid(int(vlen * lmul/vsew), int(vlen), int(vsew), f)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)


def create_empty_test_vid(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vid(f, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_vid(instr, f, vlen, vsew, lmul)

    # Common const information
    print_ending_vid(vlen, vsew, lmul, f, n)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
