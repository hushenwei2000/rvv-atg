from glob import glob
import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vslide'
f_val = ['0x80000001', '0xBF800000', '0x807FFFFE', '0x3F800000', '0xFF7FFFFF', '0x807FFFFF', '0x00800000', '0x00000002',
         '0x007FFFFF', '0x00000001', '0x00000000', '0x80000000', '0x80855555', '0x7F7FFFFF', '0x80800000', '0x00800001']  # 16
walking_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -
               17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]  # 66
rd_val = [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17,
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
          33, 35, 36, 37, 39, 40, 41, 42, 43, 44, 45, 47,
          48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
          61, 67, 71, 73, 79, 83, 89, 97, 101] # Random numbers
f_rd_val=['0x40400000', '0x41F8CCCC', '0x43031999', '0x40799999', '0x415E6666', '0x4303E666', '0xBF03126E', '0xBFC18937', '0xC05D2F1A', '0xC205D2F1', '0xC3A6BA5E', '0xC511D74B', '0xC0154FDF', '0x458E92A9', '0x49001125', '0x474CE800']
vma = False  # False to turn to undisturb
num_elem = 0
num_group_walking = 0
num_group_f = 0
walking_val_grouped = []
f_val_grouped = []


def generate_macros_vslide1(f, vlen, vsew):
    for i in range(1, 32):
        if i == 5 or i == 14 or i == 15:
            continue;
        print("#define TEST_VSLIDE1_VX_OP_rd_%d( testnum, inst, result_base, rd_base, rs1, base ) \\\n\
            TEST_CASE_LOOP( testnum, v%d, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x7, result_base; \\\n\
                li x1, rs1; \\\n\
                inst v%d, v5, x1; \\\n\
            )"%(i, i, vsew, vsew, i, i), file=f)
        print("#define TEST_VSLIDE1_VX_OP_rs2_%d( testnum, inst, result_base, rd_base, rs1, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la  x7, result_base; \\\n\
                li x1, rs1; \\\n\
                inst v14, v%d, x1; \\\n\
            )"%(i, vsew, i, vsew, i), file=f)
        print(" #define TEST_VSLIDE_VF_OP_rd_%d(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
            TEST_CASE_LOOP( testnum, v%d, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la x7, result_base; \\\n\
                la x1, f_rs1_base; \\\n\
                flw f1, 0(x1); \\\n\
                inst v%d, v5, f1; \\\n\
            )"%(i, i, vsew, vsew, i, i), file=f)
        print(" #define TEST_VSLIDE_VF_OP_rs2_%d(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la x7, result_base; \\\n\
                la x1, f_rs1_base; \\\n\
                flw f1, 0(x1); \\\n\
                inst v14, v%d, f1; \\\n\
            )"%(i, vsew, i, vsew, i), file=f)

    for i in range(1, 32):
        if i == 1 or i == 7:
            continue;
        print("#define TEST_VSLIDE1_VX_OP_rs1_%d( testnum, inst, result_base, rd_base, rs1, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la  x7, result_base; \\\n\
                li x%d, rs1; \\\n\
                inst v14, v5, x%d; \\\n\
            )"%(i, vsew, vsew, i, i), file=f)
        
    for i in range(1, 32):
        print(" #define TEST_VSLIDE_VF_OP_rs1_%d(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la x7, result_base; \\\n\
                la x1, f_rs1_base; \\\n\
                flw f%d, 0(x1); \\\n\
                inst v14, v5, f%d; \\\n\
            )"%(i, vsew, vsew, i, i), file=f)


def generate_tests_vslide1(f):
    n=1
    print("  #-------------------------------------------------------------",file=f)
    print("  # vslide1up/down.vx/vf Test    ------------------------------------------",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(num_group_walking):
        print("  TEST_VSLIDE1_VX_OP( " + str(n) + ", vslide1up.vx, walking_data_slide1upans%d, "%i + "rd_data, " + str(walking_val_grouped[i][0]) + ", walking_data%d );"%i, file=f)
        n +=1
        print("  TEST_VSLIDE1_VX_OP( " + str(n) + ", vslide1down.vx, walking_data_slide1downans%d, "%i + "rd_data, " + str(walking_val_grouped[i][0]) + ", walking_data%d );"%i, file=f)
        n +=1
    for i in range(num_group_f):
        print("  TEST_VSLIDE_VF_OP( " + str(n) + ", vfslide1up.vf, 0, f_data_slide1upans%d, "%i + "f_rd_data, " + "f_rd_data0" + ", f_data%d );"%i, file=f)
        n +=1
        print("  TEST_VSLIDE_VF_OP( " + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%i + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%i, file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vslide1up/down.vx/vf Test    ------------------------------------------",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)",file=f)
    for i in range(1, 32):
        if i != 5 and i != 14 and i != 15:
            print("  TEST_VSLIDE1_VX_OP_rd_%d( "%i + str(n) + ", vslide1up.vx, walking_data_slide1upans%d, "%(i%num_group_walking) + "rd_data, " + str(walking_val_grouped[i%num_group_walking][0]) + ", walking_data%d );"%(i%num_group_walking), file=f)
            n +=1
            print("  TEST_VSLIDE1_VX_OP_rs2_%d( "%i + str(n) + ", vslide1up.vx, walking_data_slide1upans%d, "%(i%num_group_walking) + "rd_data, " + str(walking_val_grouped[i%num_group_walking][0]) + ", walking_data%d );"%(i%num_group_walking), file=f)
            n +=1
            print("  TEST_VSLIDE_VF_OP_rd_%d( "%i + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%(i%num_group_f) + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%(i%num_group_f), file=f)
            n +=1
            print("  TEST_VSLIDE_VF_OP_rs2_%d( "%i + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%(i%num_group_f) + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%(i%num_group_f), file=f)
            n +=1
        if i != 1 and i != 7:
            print("  TEST_VSLIDE1_VX_OP_rs1_%d( "%i + str(n) + ", vslide1up.vx, walking_data_slide1upans%d, "%(i%num_group_walking) + "rd_data, " + str(walking_val_grouped[i%num_group_walking][0]) + ", walking_data%d );"%(i%num_group_walking), file=f)
            n +=1
        print("  TEST_VSLIDE_VF_OP_rs1_%d( "%i + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%(i%num_group_f) + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%(i%num_group_f), file=f)
        n +=1


def generate_dat_seg_vslide1(f, vsew):
    print("rd_data:", file=f)
    for i in range(num_elem):
        print(".word\t%d"%rd_val[i], file=f)
    print("",file=f)
    for i in range(num_group_walking):
        # generate data
        print("walking_data%d:"%i, file=f)
        for j in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%d"%walking_val_grouped[i][j], file=f)
        print("", file=f)
        # generate answer for vslide1up
        print("walking_data_slide1upans%d:"%i, file=f)
        for j in range(num_elem):
            if j == 0:
                print_data_width_prefix(f, vsew)
                print("%d"%(walking_val_grouped[i][0]), file=f)
            else:
                print_data_width_prefix(f, vsew)
                print("%d"%(walking_val_grouped[i][j-1]), file=f)
        print("", file=f)
        # generate answer for vslide1up
        print("walking_data_slide1downans%d:"%i, file=f)
        for j in range(num_elem):
            if j == num_elem - 1:
                print_data_width_prefix(f, vsew)
                print("%d"%(walking_val_grouped[i][0]), file=f)
            else:
                print_data_width_prefix(f, vsew)
                print("%d"%(walking_val_grouped[i][j+1]), file=f)
        print("", file=f)

def generate_fdat_seg_vslide1(f):
    print("f_rd_data:", file=f)
    for i in range(num_elem):
        print("f_rd_data%d:\t.word\t%s"%(i, f_rd_val[i]), file=f)
    print("",file=f)
    for i in range(num_group_f):
        # generate data
        print("f_data%d:"%i, file=f)
        for j in range(num_elem):
            print(".word\t%s"%f_val_grouped[i][j], file=f)
        print("", file=f)
        # generate answer for vslide1up
        print("f_data_slide1upans%d:"%i, file=f)
        for j in range(num_elem):
            if j == 0:
                print(".word\t%s"%(f_rd_val[0]), file=f)
            else:
                print(".word\t%s"%(f_val_grouped[i][j-1]), file=f)
        print("", file=f)
        # generate answer for vslide1up
        print("f_data_slide1downans%d:"%i, file=f)
        for j in range(num_elem):
            if j == num_elem - 1:
                print(".word\t%s"%(f_rd_val[num_elem - 1]), file=f)
            else:
                print(".word\t%s"%(f_val_grouped[i][j+1]), file=f)
        print("", file=f)


def print_ending_vslide(f, vlen, vsew):
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

    generate_dat_seg_vslide1(f, vsew)
    generate_fdat_seg_vslide1(f)

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


def create_empty_test_vslide1(xlen, vlen, vsew, lmul, vta, _vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global num_group_f
    global walking_val_grouped
    global f_val_grouped
    global vma
    num_elem = int(vlen / vsew)
    num_group_walking = int(len(walking_val) / num_elem)
    num_group_f = int(len(f_val) / num_elem)
    vma = _vma
    for i in range(num_group_walking):
        temp = []
        for j in range(num_elem):
            temp.append(walking_val[i*num_elem+j])
        walking_val_grouped.append(temp)
    for i in range(num_group_f):
        temp = []
        for j in range(num_elem):
            temp.append(f_val[i*num_elem+j])
        f_val_grouped.append(temp)

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vslide1(f, vlen, vsew)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vslide1(f)

    # Common const information
    print_ending_vslide(f, vlen, vsew)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
