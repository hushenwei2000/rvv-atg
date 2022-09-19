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
          18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
vma = False  # False to turn to undisturb
num_elem = 0
num_group_walking = 0
num_group_f = 0
walking_val_grouped = []
f_val_grouped = []


def generate_macros_vslide(f, vlen, vsew):
    for i in range(1, 32):
        if i == 5 or i == 14 or i == 15:
            continue
        print("#define TEST_VSLIDE_VX_OP_rd_%d( testnum, inst, result_base, rd_base, offset, base ) \\\n\
            TEST_CASE_LOOP( testnum, v%d, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x7, result_base; \\\n\
                li x1, offset; \\\n\
                inst v%d, v5, x1; \\\n\
            )" % (i, i, vsew, vsew, i, i), file=f)

    for i in range(1, 32):
        if i == 5 or i == 14 or i == 15:
            continue
        print("#define TEST_VSLIDE_VX_OP_rs2_%d( testnum, inst, result_base, rd_base, offset, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la  x7, result_base; \\\n\
                li x1, offset; \\\n\
                inst v14, v%d, x1; \\\n\
            )" % (i, vsew, i,vsew, i), file=f)

    for i in range(1, 32):
        if i == 1 or i == 7:
            continue
        print("#define TEST_VSLIDE_VX_OP_rs1_%d( testnum, inst, result_base, rd_base, offset, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la  x7, result_base; \\\n\
                li x%d, offset; \\\n\
                inst v14, v5, x%d; \\\n\
            )" % (i, vsew, vsew, i, i), file=f)

    for i in range(1, 32):
        if i == 5 or i == 14 or i == 15:
            continue
        print("#define TEST_VSLIDE_VI_OP_rd_%d( testnum, inst, result_base, rd_base, offset_imm, base ) \\\n\
            TEST_CASE_LOOP( testnum, v%d, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v5, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x7, result_base; \\\n\
                inst v%d, v5, offset_imm; \\\n\
            )" % (i, i, vsew, vsew, i, i), file=f)

    for i in range(1, 32):
        if i == 5 or i == 14 or i == 15:
            continue
        print("#define TEST_VSLIDE_VI_OP_rs2_%d( testnum, inst, result_base, rd_base, offset_imm, base ) \\\n\
            TEST_CASE_LOOP( testnum, v14, x7, \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v14, (x1); \\\n\
                la  x7, result_base; \\\n\
                inst v14, v%d, offset_imm; \\\n\
            )" % (i, vsew, i, vsew, i), file=f)


def generate_tests_vslide(f):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # vslideup.vx/vi Test    ------------------------------------------", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(num_group_walking):
        for k in range(num_elem + 1):
            print("  TEST_VSLIDE_VX_OP( " + str(n) + ", vslideup.vx, walking_data%d_slideupans_offset_%d, " %
                  (i, k) + "rd_data, " + str(k) + ", walking_data%d );" % i, file=f)
            n += 1
            print("  TEST_VSLIDE_VI_OP( " + str(n) + ", vslideup.vi, walking_data%d_slideupans_offset_%d, " %
                  (i, k) + "rd_data, " + str(k) + ", walking_data%d );" % i, file=f)
            n += 1
            print("  TEST_VSLIDE_VX_OP( " + str(n) + ", vslidedown.vx, walking_data%d_slidedownans_offset_%d, " %
                  (i, k) + "rd_data, " + str(k) + ", walking_data%d );" % i, file=f)
            n += 1
            print("  TEST_VSLIDE_VI_OP( " + str(n) + ", vslidedown.vi, walking_data%d_slidedownans_offset_%d, " %
                  (i, k) + "rd_data, " + str(k) + ", walking_data%d );" % i, file=f)
            n += 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # vslideup.vx/vi Test  (Different Registers)  ------------------------------------------", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_2)", file=f)

    for i in range(1, 32):
        if i != 5 and i != 14 and i != 15:
            print("  TEST_VSLIDE_VX_OP_rd_%d( " % i + str(n) + ", vslideup.vx, walking_data%d_slideupans_offset_%d, " % (i % num_group_walking,
                  i % (num_elem+1)) + "rd_data, " + str(i % (num_elem+1)) + ", walking_data%d );" % (i % num_group_walking), file=f)
            n += 1
            print("  TEST_VSLIDE_VI_OP_rd_%d( " % i + str(n) + ", vslideup.vi, walking_data%d_slideupans_offset_%d, " % (i % num_group_walking,
                  i % (num_elem+1)) + "rd_data, " + str(i % (num_elem+1)) + ", walking_data%d );" % (i % num_group_walking), file=f)
            n += 1
            print("  TEST_VSLIDE_VX_OP_rs2_%d( " % i + str(n) + ", vslideup.vx, walking_data%d_slideupans_offset_%d, " % (i %
                  num_group_walking, i % (num_elem+1)) + "rd_data, " + str(i % (num_elem+1)) + ", walking_data%d );" % (i % num_group_walking), file=f)
            n += 1
            print("  TEST_VSLIDE_VI_OP_rs2_%d( " % i + str(n) + ", vslideup.vi, walking_data%d_slideupans_offset_%d, " % (i %
                  num_group_walking, i % (num_elem+1)) + "rd_data, " + str(i % (num_elem+1)) + ", walking_data%d );" % (i % num_group_walking), file=f)
            n += 1
        if i != 1 and i != 7:
            print("  TEST_VSLIDE_VX_OP_rs1_%d( " % i + str(n) + ", vslideup.vx, walking_data%d_slideupans_offset_%d, " % (i %
                  num_group_walking, i % (num_elem+1)) + "rd_data, " + str(i % (num_elem+1)) + ", walking_data%d );" % (i % num_group_walking), file=f)
            n += 1


def generate_dat_seg_vslide(f, vlen, vsew):
    print("rd_data:", file=f)
    for i in range(num_elem):
        if vsew == 8:
            print(".byte\t%d" % rd_val[i], file=f)
        elif vsew == 16:
            print(".hword\t%d" % rd_val[i], file=f)
        elif vsew == 32:
            print(".word\t%d" % rd_val[i], file=f)
        elif vsew == 64:
            print(".dword\t%d" % rd_val[i], file=f)
    print("", file=f)
    for i in range(num_group_walking):
        # generate data
        print("walking_data%d:" % i, file=f)
        for j in range(num_elem):
            if vsew == 8:
                print(".byte\t%d" % walking_val_grouped[i][j], file=f)
            elif vsew == 16:
                print(".hword\t%d" % walking_val_grouped[i][j], file=f)
            elif vsew == 32:
                print(".word\t%d" % walking_val_grouped[i][j], file=f)
            elif vsew == 64:
                print(".dword\t%d" % walking_val_grouped[i][j], file=f)
        print("", file=f)
        # generate answer
        for k in range(num_elem + 1):
            # Each Offset has a answer
            print("walking_data%d_slideupans_offset_%d:" % (i, k), file=f)
            for p in range(num_elem):
                if vsew == 8:
                    print(".byte\t%d" % (rd_val[p] if p < k else walking_val_grouped[i][p - k]), file=f)
                elif vsew == 16:
                    print(".hword\t%d" % (rd_val[p] if p < k else walking_val_grouped[i][p - k]), file=f)
                elif vsew == 32:
                    print(".word\t%d" % (rd_val[p] if p < k else walking_val_grouped[i][p - k]), file=f)
                elif vsew == 64:
                    print(".dword\t%d" % (rd_val[p] if p < k else walking_val_grouped[i][p - k]), file=f)
            print("", file=f)
        for k in range(num_elem + 1):
            # Each Offset has a answer
            print("walking_data%d_slidedownans_offset_%d:" % (i, k), file=f)
            for p in range(num_elem):
                if vsew == 8:
                    print(".byte\t%d" % (walking_val_grouped[i][p + k] if p + k < num_elem else (0 if vma else rd_val[p])), file=f)
                elif vsew == 16:
                    print(".hword\t%d" % (walking_val_grouped[i][p + k] if p + k < num_elem else (0 if vma else rd_val[p])), file=f)
                elif vsew == 32:
                    print(".word\t%d" % (walking_val_grouped[i][p + k] if p + k < num_elem else (0 if vma else rd_val[p])), file=f)
                elif vsew == 64:
                    print(".dword\t%d" % (walking_val_grouped[i][p + k] if p + k < num_elem else (0 if vma else rd_val[p])), file=f)
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

    generate_dat_seg_vslide(f, vlen, vsew)

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


def create_empty_test_vslide(xlen, vlen, vsew, lmul, vta, _vma, output_dir):
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

    generate_macros_vslide(f, vlen, vsew)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vslide(f)

    # Common const information
    print_ending_vslide(f, vlen, vsew)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
