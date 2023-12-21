from glob import glob
import logging
import os
from random import randint
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vmre'

vma = False  # False to turn to undisturb
num_elem = 0
num_group_walking = 0
num_group_f = 0
walking_val_grouped = []
f_val_grouped = []


def generate_macros_vmre(f, vlen, vsew, lmul):
    num_of_elements = vlen / vsew
    lmul_num = lmul
    if lmul >= 1:
        lmul = str(int(lmul))
    elif lmul == 0.5:
        lmul = 'f2'
    elif lmul == 0.25:
        lmul = 'f4'
    elif lmul == 0.125:
        lmul = 'f8'
    print("#define TEST_VMRE1_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            li x1, %d;"%(num_of_elements) + " \\\n\
            vsetvli x31, x1, e%d, m%s, tu, mu;"%(vsew, lmul) + " \\\n\
            la  x1, base; \\\n\
            vl8re%d.v v8, (x1); "%vsew + " \\\n\
            inst v16, v8; \\\n\
        ) ", file=f)
    
    print("#define TEST_VMRE2_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            li x1, %d;"%(num_of_elements*2) + " \\\n\
            vsetvli x31, x1, e%d, m%s, tu, mu;"%(vsew, lmul) + " \\\n\
            la  x1, base; \\\n\
            vl8re%d.v v8, (x1); "%vsew + " \\\n\
            inst v16, v8; \\\n\
        ) \\", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v17) \n" if lmul_num <= 1 else "", file=f)

    print('', file=f)
    print("#define TEST_VMRE4_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            li x1, %d;"%(num_of_elements*4) + " \\\n\
            vsetvli x31, x1, e%d, m%s, tu, mu;"%(vsew, lmul) + " \\\n\
            la  x1, base; \\\n\
            vl8re%d.v v8, (x1); "%vsew + " \\\n\
            inst v16, v8; \\\n\
        ) \\", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v17) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v18) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v19) \n" if lmul_num <= 1 else "", file=f)


    print('', file=f)
    print("#define TEST_VMRE8_OP( testnum, inst,  base ) \\\n\
        TEST_CASE_LOOP( testnum, v16,  \\\n\
            li x1, %d;"%(num_of_elements*8) + " \\\n\
            vsetvli x31, x1, e%d, m%s, tu, mu;"%(vsew, lmul) + " \\\n\
            la  x1, base; \\\n\
            vl8re%d.v v8, (x1); "%vsew + " \\\n\
            inst v16, v8; \\\n\
        ) \\", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v17) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v18) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v19) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v20) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v21) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v22) \\" if lmul_num <= 1 else "", file=f)
    print("        TEST_CASE_LOOP_CONTINUE( testnum, v23) \n" if lmul_num <= 1 else "", file=f)

    print('', file=f)
    return 0


def generate_tests_vmre(f):
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s tests" % instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    no = 1
    for i in range(num_group_walking - 9):
        # vmv1r test rd, vmv2r test rd+1, vmv4r test rd+3, vmv8r test rd+7 (all test the last register be influenced)
        # print("TEST_VMRE1_OP( %d,  vmv1r.v, walking_data%d, walking_data%d );" % (no, i, i),file=f)
        no = no + 1
        print("TEST_VMRE1_OP( %d,  vmv1r.v, walking_data%d);" % (no, i),file=f)
        no = no + 1
        print("TEST_VMRE2_OP( %d,  vmv2r.v, walking_data%d );" % (no, i),file=f)
        no = no + 1
        print("TEST_VMRE4_OP( %d,  vmv4r.v, walking_data%d );" % (no, i),file=f)
        no = no + 1
        print("TEST_VMRE8_OP( %d,  vmv8r.v, walking_data%d );" % (no, i),file=f)
    return no

def generate_dat_seg_vmre(f, vlen, lmul, vsew):
    lmul = 1 if lmul < 1 else int(lmul)
    num_elem = int(vlen * lmul / vsew)
    # Generate each group data
    for i in range(num_group_walking):
        # generate data
        print("walking_data%d:"%i, file=f)
        for j in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%d"%walking_val_grouped[i][j], file=f)
        print("", file=f)

def print_ending_vmre(f, vlen, lmul, vsew, n):
    print(" #endif\n\
    \n\
    RVTEST_CODE_END\n\
    RVMODEL_HALT\n\
    \n\
    .data\n\
    RVTEST_DATA_BEGIN\n\
    \n\
    TEST_DATA\n\
    \n\
    ", file=f)

    generate_dat_seg_vmre(f, vlen, lmul, vsew)

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)


def create_empty_test_vmre(xlen, vlen, vsew, lmul, vta, _vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global walking_val_grouped
    global vma
    lmul = 1 if lmul < 1 else int(lmul)
    num_elem = int(vlen * lmul/ vsew)
    walking_val_vmre = []
    for i in range(num_elem * 12):
        walking_val_vmre.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
    num_group_walking = int(len(walking_val_vmre) / num_elem)
    vma = _vma
    for i in range(num_group_walking):
        temp = []
        for j in range(num_elem):
            temp.append(walking_val_vmre[i*num_elem+j])
        walking_val_grouped.append(temp)
    
    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vmre(f, vlen, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    n = generate_tests_vmre(f)

    # Common const information
    print_ending_vmre(f, vlen, lmul, vsew, n)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
