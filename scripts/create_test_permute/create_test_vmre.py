from glob import glob
import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vmre'
walking_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -
               17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647,
               ]  # 66
random_val = [-27638, 31380, -1706, 16860, 290, 11167, 1163, 9601, 30738, 2716, -3235, 22869, 10574, 31612, -22835, -32244, -10700, 21057, -1284, -15492, 18507, -5316, 13671, -10242, 7510, 24839, 23255, 12069, 1159, -11875, 14735, 28926, 9422, -8316, 12800, -669, -20647, 23675, -31930, -11842, 10331, 31463, 9984, 29467, 8191, 13985, -22552, 16163, -14600, 20609, -6356, -5132, 5225, -31914, 9822, -6743, 16895, 8525, 12604, -29640,] # 60 Random val in [-32768, 32767]
walking_val = walking_val + random_val
vma = False  # False to turn to undisturb
num_elem = 0
num_group_walking = 0
num_group_f = 0
walking_val_grouped = []
f_val_grouped = []


def generate_macros_vmre(f, vlen, vsew):
    return 0


def generate_tests_vmre(f):
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s tests" % instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    no = 1
    for i in range(num_group_walking - 9):
        # vmv1r test rd, vmv2r test rd+1, vmv4r test rd+3, vmv8r test rd+7 (all test the last register be influenced)
        print("TEST_VMRE1_OP( %d,  vmv1r.v, walking_data%d, walking_data%d );" % (no, i, i),file=f)
        no = no + 1
        print("TEST_VMRE2_OP( %d,  vmv2r.v, walking_data%d, walking_data%d, walking_data%d );" % (no, i, i+1, i),file=f)
        no = no + 1
        print("TEST_VMRE4_OP( %d,  vmv4r.v, walking_data%d, walking_data%d, walking_data%d );" % (no, i, i+3, i),file=f)
        no = no + 1
        print("TEST_VMRE8_OP( %d,  vmv8r.v, walking_data%d, walking_data%d, walking_data%d );" % (no, i, i+7, i),file=f)
        no = no + 1

def generate_dat_seg_vmre(f, vlen, vsew):
    num_elem = int(vlen / vsew)
    # Generate each group data
    for i in range(num_group_walking):
        # generate data
        print("walking_data%d:"%i, file=f)
        for j in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%d"%walking_val_grouped[i][j], file=f)
        print("", file=f)

def print_ending_vmre(f, vlen, vsew):
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
    \n\
    ", file=f)

    generate_dat_seg_vmre(f, vlen, vsew)

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


def create_empty_test_vmre(xlen, vlen, vsew, lmul, vta, _vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global walking_val_grouped
    global vma
    num_elem = int(vlen / vsew)
    num_group_walking = int(len(walking_val) / num_elem)
    vma = _vma
    for i in range(num_group_walking):
        temp = []
        for j in range(num_elem):
            temp.append(walking_val[i*num_elem+j])
        walking_val_grouped.append(temp)
    
    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vmre(f, vlen, vsew)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vmre(f)

    # Common const information
    print_ending_vmre(f, vlen, vsew)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
