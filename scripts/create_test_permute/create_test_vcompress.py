from glob import glob
import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vcompress'
walking_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -
               17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]  # 66
rd_val = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
          33, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 47,
          48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
          61, 67, 71, 73, 79, 83, 89, 97, 101]
vma = False  # False to turn to undisturb
num_elem = 0
num_group_walking = 0
walking_val_grouped = []
mask_val = []  # size: 2 * num_elem + 2


def generate_maskval():
    global num_elem
    global mask_val
    # Generate walking ones
    print(num_elem)
    for i in range(num_elem + 1):
        val = ''
        for j in range(num_elem):
            val = val + ("1" if i == j + 1 else "0")
        mask_val.append(val)
    print(mask_val)
    # Generate walking zeros
    for i in range(num_elem + 1):
        val = ''
        for j in range(num_elem):
            val = val + ("0" if i == j + 1 else "1")
        mask_val.append(val)
    print(mask_val)


def generate_walking_mask_seg(f, vlen):
    # Generate walking ones
    for i in range(num_elem + 1):
        print("walking_mask_dat%d:"%i, file=f)
        for j in range(num_elem):
            print("\t", end="", file=f)
            element_width = vlen / num_elem
            if element_width == 8:
                print(".byte", end=" 0x", file=f)
            elif element_width == 16:
                print(".hword", end=" 0x", file=f)
            elif element_width == 32:
                print(".word", end=" 0x", file=f)
            elif element_width == 64:
                print(".dword", end=" 0x", file=f)
            print("1" if i == j + 1 else "0", file=f)
        print("", file=f)
    
    # Generate walking zeros
    for i in range(num_elem + 1):
        print("walking_mask_dat%d:"%(num_elem + 1 + i), file=f)
        for j in range(num_elem):
            print("\t", end="", file=f)
            element_width = vlen / num_elem
            if element_width == 8:
                print(".byte", end=" 0x", file=f)
            elif element_width == 16:
                print(".hword", end=" 0x", file=f)
            elif element_width == 32:
                print(".word", end=" 0x", file=f)
            elif element_width == 64:
                print(".dword", end=" 0x", file=f)
            print("0" if i == j + 1 else "1", file=f)
        print("", file=f)

def generate_dat_seg_vcompress(f):
    global walking_val_grouped
    global num_elem
    global mask_val
    # Generate rd
    print("rd_data:", file=f)
    for i in range(num_elem):
        print(".word\t%d" % rd_val[i], file=f)
    print("", file=f)
    # Generate each group data
    for i in range(num_group_walking):
        # generate data
        print("walking_data%d:" % i, file=f)
        for j in range(num_elem):
            print(".word\t%d" % walking_val_grouped[i][j], file=f)
        print("", file=f)
        # generate answer
        for k in range(len(mask_val)):
            # Each Mask has a answer
            print("walking_data%d_ans_mask%d:" % (i, k), file=f)
            index = 0
            for p in range(num_elem):
                if mask_val[k][p] == '1':
                    print(".word\t%d" % walking_val_grouped[i][p], file=f)
                    index = index + 1
                else:
                    continue
            for p in range(index, num_elem):
                print(".word\t%d" % (0 if vma else rd_val[p]), file=f)
            print("", file=f)


def generate_macros_vcompress(f):
    for i in range(32):
        if i == 0 or i == 5 or i == 6 or i == 15:  # 15 is used for TEST_CASE_LOOP
            continue
        print("#define TEST_VCOMPRESS_OP_rd_%d( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v%d, x7, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, result_addr; \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle32.v v5, (x3); \\\n\
            vmseq.vi v0, v5, 1; \\\n\
            vle32.v v5, (x1); \\\n\
            vle32.v v%d, (x2); \\\n\
            inst v%d, v5, v0; \\\n\
        )" % (i, i, i, i), file=f)

    for i in range(32):
        if i == 0 or i == 5 or i == 6 or i == 15:  # 15 is used for TEST_CASE_LOOP
            continue
        print("#define TEST_VCOMPRESS_OP_rs1_%d( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v6, x7, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, result_addr; \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle32.v v5, (x3); \\\n\
            vmseq.vi v%d, v5, 1; \\\n\
            vle32.v v5, (x1); \\\n\
            vle32.v v6, (x2); \\\n\
            inst v6, v5, v%d; \\\n\
        )" % (i, i, i), file=f)

    for i in range(32):
        if i == 0 or i == 5 or i == 6 or i == 15:  # 15 is used for TEST_CASE_LOOP
            continue
        print("#define TEST_VCOMPRESS_OP_rs2_%d( testnum, inst, result_addr, src_addr, rd_addr, vm_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v6, x7, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x7, result_addr; \\\n\
            la  x1, src_addr; \\\n\
            la  x2, rd_addr; \\\n\
            la  x3, vm_addr; \\\n\
            vle32.v v5, (x3); \\\n\
            vmseq.vi v0, v5, 1; \\\n\
            vle32.v v%d, (x1); \\\n\
            vle32.v v6, (x2); \\\n\
            inst v6, v%d, v0; \\\n\
        )" % (i, i, i), file=f)


def generate_tests_vcompress(f):
    global mask_val
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
    # generate registers，覆盖不同寄存器
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

    for i in range(32):
        if i == 0 or i == 5 or i == 6 or i == 15:  # 15 is used for TEST_CASE_LOOP
            continue
        print("TEST_VCOMPRESS_OP_rd_%d( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
            i, no, instr, i % num_group_walking, j % len(mask_val), i % num_group_walking, j % len(mask_val)), file=f)
        no = no + 1

    for i in range(32):
        if i == 0 or i == 5 or i == 6 or i == 15:  # 15 is used for TEST_CASE_LOOP
            continue
        print("TEST_VCOMPRESS_OP_rs1_%d( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
            i, no, instr, i % num_group_walking, j % len(mask_val), i % num_group_walking, j % len(mask_val)), file=f)
        no = no + 1

    for i in range(32):
        if i == 0 or i == 5 or i == 6 or i == 15:  # 15 is used for TEST_CASE_LOOP
            continue
        print("TEST_VCOMPRESS_OP_rs2_%d( %d,  %s.vm,  walking_data%d_ans_mask%d,  walking_data%d, rd_data, walking_mask_dat%d );" % (
            i, no, instr, i % num_group_walking, j % len(mask_val), i % num_group_walking, j % len(mask_val)), file=f)
        no = no + 1


def print_ending_vcompress(vlen, vsew, f):
    # generate const information
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
        \n\
    TEST_PASSFAIL\n\
    #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    ", file=f)

    generate_walking_mask_seg(f, vlen)
    generate_walking_data_seg_common(int(vlen/vsew), int(vlen), f)
    generate_dat_seg_vcompress(f)

    print("signature_x12_0:\n\
        .fill 0,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x12_1:\n\
        .fill 32,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x20_2:\n\
        .fill 376,4,0xdeadbeef\n\
    \n\
    #ifdef rvtest_mtrap_routine\n\
    \n\
    mtrap_sigptr:\n\
        .fill 128,4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    #ifdef rvtest_gpr_save\n\
    \n\
    gpr_save:\n\
        .fill 32*(XLEN/32),4,0xdeadbeef\n\
    \n\
    #endif\n\
    \n\
    RVTEST_DATA_END\n\
    ", file=f)


def create_empty_test_vcompress(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global walking_val_grouped
    num_elem = int(vlen / vsew)
    num_group_walking = int(len(walking_val) / num_elem)
    for i in range(num_group_walking):
        temp = []
        for j in range(num_elem):
            temp.append(walking_val[i*num_elem+j])
        walking_val_grouped.append(temp)
    generate_maskval()

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vcompress(f)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vcompress(f)

    # Common const information
    print_ending_vcompress(vlen, vsew, f)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
