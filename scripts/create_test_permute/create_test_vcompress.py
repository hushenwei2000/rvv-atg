from glob import glob
import logging
import os
from random import randint
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
from scripts.create_test_permute.const_data import *
import re

instr = 'vcompress'
walking_val = []
rd_val = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
          33, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 47,
          48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
          61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 105, 107, 109, 111, 113, 115] # 66

num_elem = 0
num_group_walking = 0
walking_val_grouped = []
mask_val = []  # size: 2 * num_elem + 2


def generate_maskval():
    global num_elem
    global mask_val
    # Generate walking ones
    for i in range(num_elem + 1):
        val = ''
        for j in range(num_elem):
            val = val + ("1" if i == j + 1 else "0")
        mask_val.append(val)
    # Generate walking zeros
    for i in range(num_elem + 1):
        val = ''
        for j in range(num_elem):
            val = val + ("0" if i == j + 1 else "1")
        mask_val.append(val)


def generate_walking_mask_seg(f, vlen, vsew):
    # Generate walking ones
    for i in range(num_elem + 1):
        print("walking_mask_dat%d:"%i, file=f)
        for j in range(num_elem):
            print("\t", end="", file=f)
            if vsew == 8:
                print(".byte", end=" 0x", file=f)
            elif vsew == 16:
                print(".hword", end=" 0x", file=f)
            elif vsew == 32:
                print(".word", end=" 0x", file=f)
            elif vsew == 64:
                print(".dword", end=" 0x", file=f)
            print("1" if i == j + 1 else "0", file=f)
        print("", file=f)
    
    # Generate walking zeros
    for i in range(num_elem + 1):
        print("walking_mask_dat%d:"%(num_elem + 1 + i), file=f)
        for j in range(num_elem):
            print("\t", end="", file=f)
            if vsew == 8:
                print(".byte", end=" 0x", file=f)
            elif vsew == 16:
                print(".hword", end=" 0x", file=f)
            elif vsew == 32:
                print(".word", end=" 0x", file=f)
            elif vsew == 64:
                print(".dword", end=" 0x", file=f)
            print("0" if i == j + 1 else "1", file=f)
        print("", file=f)

def generate_dat_seg_vcompress(f, vsew):
    vma = os.environ["RVV_ATG_VMA"]
    vma = True if vma == "True" else False;
    agnostic_type = int(os.environ['RVV_ATG_AGNOSTIC_TYPE'])
    global walking_val_grouped
    global num_elem
    global mask_val
    # Generate rd
    print("rd_data:", file=f)
    for i in range(num_elem):
        print_data_width_prefix(f, vsew)
        print("%d" % rd_val[i], file=f)
    print("", file=f)
    # Generate each group data
    for i in range(num_group_walking):
        # generate data
        print("walking_data%d:" % i, file=f)
        for j in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%d" % walking_val_grouped[i][j], file=f)
        print("", file=f)
        # generate answer
        for k in range(len(mask_val)):
            # Each Mask has a answer
            print("walking_data%d_ans_mask%d:" % (i, k), file=f)
            index = 0
            for p in range(num_elem):
                if mask_val[k][p] == '1':
                    print_data_width_prefix(f, vsew)
                    print("%d" % walking_val_grouped[i][p], file=f)
                    index = index + 1
                else:
                    continue
            for p in range(index, num_elem):
                print_data_width_prefix(f, vsew)
                print("%d" % (1 if (vma and agnostic_type == 1) else rd_val[p]), file=f)
            print("", file=f)


def generate_macros_vcompress(f, vsew, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    print("#define TEST_VCOMPRESS_OP( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle%d.v v8, (x3); \\\n\
            vmseq.vi v0, v8, 1; \\\n\
            vle%d.v v8, (x1); \\\n\
            vle%d.v v16, (x2); \\\n\
            inst v16, v8, v0; \\\n\
        )" % ( vsew, vsew, vsew), file=f)
    
    for i in range(32):
        # no overlap: (v0 < rd) or (rd + lmul - 1 < v0)
        if i == 0 or i == 8 or i == 16 or i == 15 or i % lmul != 0 or (0 >= i and i + lmul - 1 >= 0):  # 15 is used for TEST_CASE_LOOP
            continue
        print("#define TEST_VCOMPRESS_OP_rd_%d( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v%d, result_addr, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle%d.v v8, (x3); \\\n\
            vmseq.vi v0, v8, 1; \\\n\
            vle%d.v v8, (x1); \\\n\
            vle%d.v v%d, (x2); \\\n\
            inst v%d, v8, v0; \\\n\
        )" % (i, i, vsew, vsew, vsew, i, i), file=f)

    for i in range(32):
        if i == 0 or i == 8 or i == 16 or i == 15 or (8 + lmul - 1 >= i and i + lmul - 1 >= 8) or (i >= 16 and 16 + lmul - 1 >= i):  # 15 is used for TEST_CASE_LOOP; require_noover for vmseq and vcompress
            continue
        print("#define TEST_VCOMPRESS_OP_rs1_%d( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle%d.v v8, (x3); \\\n\
            vmseq.vi v%d, v8, 1; \\\n\
            vle%d.v v8, (x1); \\\n\
            vle%d.v v16, (x2); \\\n\
            inst v16, v8, v%d; \\\n\
        )" % (i, vsew, i, vsew, vsew, i), file=f)

    for i in range(32):
        if i == 0 or i == 8 or i == 16 or i == 15 or i % lmul != 0:  # 15 is used for TEST_CASE_LOOP
            continue
        print("#define TEST_VCOMPRESS_OP_rs2_%d( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle%d.v v8, (x3); \\\n\
            vmseq.vi v0, v8, 1; \\\n\
            vle%d.v v%d, (x1); \\\n\
            vle%d.v v16, (x2); \\\n\
            inst v16, v%d, v0; \\\n\
        )" % (i, vsew, vsew, i, vsew, i), file=f)


def generate_tests_vcompress(f, vlen, vsew, lmul):
    if num_group_walking == 0:
        return 0
    lmul = 1 if lmul < 1 else int(lmul)
    global mask_val
    vemul = int(vsew / vsew * lmul)
    if vemul == 0:
        vemul = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    no = 1
    for i in range(num_group_walking):
        for j in range(len(mask_val)):
            print("TEST_VCOMPRESS_OP( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
                no, instr, i, j, i, j), file=f)
            no = no + 1

    #################################################################################################################################
    # generate registers
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)


    for i in range(32):
        if i == 0 or i == 8 or i == 16 or i == 15 or (0 >= i and i + lmul - 1 >= 0 or i == 12 or i == 20 or i == 24):  # 15 is used for TEST_CASE_LOOP
            continue
        if i % vemul != 0: # guarantee is_aligned(insn.rd(), vemul)
            continue
        print("TEST_VCOMPRESS_OP_rd_%d( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
            i, no, instr, i % num_group_walking, j % len(mask_val), i % num_group_walking, j % len(mask_val)), file=f)
        no = no + 1

    for i in range(32):
        if i == 0 or i == 8 or i == 16 or i == 15 or (8 + lmul - 1 >= i and i + lmul - 1 >= 8) or (i >= 16 and 16 + lmul - 1 >= i) or i == 12 or i == 20 or i == 24:  # 15 is used for TEST_CASE_LOOP
            continue
        print("TEST_VCOMPRESS_OP_rs1_%d( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
            i, no, instr, i % num_group_walking, j % len(mask_val), i % num_group_walking, j % len(mask_val)), file=f)
        no = no + 1

    for i in range(32):
        if i == 0 or i == 8 or i == 16 or i == 15 or i % lmul != 0 or i == 12 or i == 20 or i == 24:  # 15 is used for TEST_CASE_LOOP
            continue
        print("TEST_VCOMPRESS_OP_rs2_%d( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
            i, no, instr, i % num_group_walking, j % len(mask_val), i % num_group_walking, j % len(mask_val)), file=f)
        no = no + 1
        
    return no


def print_ending_vcompress(vlen, vsew, lmul, f, n):
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

    generate_walking_mask_seg(f, vlen, int(vsew))
    generate_walking_data_seg_common(int(vlen * lmul/vsew), int(vlen), int(vsew), f)
    generate_dat_seg_vcompress(f, vsew)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)


def create_empty_test_vcompress(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global walking_val_grouped
    global walking_val
    num_elem = int(vlen * lmul / vsew)
    if vsew == 8 or vsew == 16:
        walking_val = coverpoints_16
    elif vsew == 32:
        walking_val = coverpoints_32
    else:
        walking_val = coverpoints_64
    # Add walking_val_grouped values, need at least num_elem
    for i in range(num_elem - - min(len(walking_val), len(rd_val)) + 2):
        walking_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
        rd_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
    if num_elem != 0:
        num_group_walking = int(len(walking_val) / num_elem)
    for i in range(num_group_walking):
        temp = []
        for j in range(num_elem):
            temp.append(walking_val[i*num_elem+j])
        walking_val_grouped.append(temp)
    generate_maskval()

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vcompress(f, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_vcompress(f, vlen, vsew, lmul)

    # Common const information
    print_ending_vcompress(vlen, vsew, lmul, f, n)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
