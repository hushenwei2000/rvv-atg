from glob import glob
import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'vfslide'
f_val = ['0x80000001', '0xBF800000', '0x807FFFFE', '0x3F800000', '0xFF7FFFFF', '0x807FFFFF', '0x00800000', '0x00000002',
         '0x007FFFFF', '0x00000001', '0x00000000', '0x80000000', '0x80855555', '0x7F7FFFFF', '0x80800000', '0x00800001']  # 16
f_rd_val=['0x40400000', '0x41F8CCCC', '0x43031999', '0x40799999', '0x415E6666', '0x4303E666', '0xBF03126E', '0xBFC18937', '0xC05D2F1A', '0xC205D2F1', '0xC3A6BA5E', '0xC511D74B', '0xC0154FDF', '0x458E92A9', '0x49001125', '0x474CE800'] # 16
vma = False  # False to turn to undisturb
num_elem = 0
num_group_f = 0
f_val_grouped = []


def generate_macros_vfslide(f, vlen, vsew):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#define TEST_VSLIDE_VF_OP(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_base, \\\n\
            VSET_VSEW_4AVL \\\n\
            %s \
            la  x1, base; \\\n\
            vle%d.v v8, (x1); \\\n\
            la  x1, rd_base; \\\n\
            vle%d.v v16, (x1); \\\n\
            la x1, f_rs1_base; \\\n\
            fl%s f1, 0(x1); \\\n\
            inst v16, v8, f1%s; \\\n\
        )"%(("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else ""), vsew, vsew, ("w" if vsew == 32 else "d"), (", v0.t" if masked else "")), file=f)
    for i in range(1, 32):
        if i == 8 or i == 16 or i == 15 or i == 31:
            continue;
        print(" #define TEST_VSLIDE_VF_OP_rd_%d(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
            TEST_CASE_LOOP( testnum, v%d, result_base, \\\n\
                VSET_VSEW_4AVL \\\n\
                %s \
                la  x1, base; \\\n\
                vle%d.v v8, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la x1, f_rs1_base; \\\n\
                fl%s f1, 0(x1); \\\n\
                inst v%d, v8, f1%s; \\\n\
            )"%(i, i, ("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else ""), vsew, vsew, i, ("w" if vsew == 32 else "d"), i, (", v0.t" if masked else "")), file=f)
        print(" #define TEST_VSLIDE_VF_OP_rs2_%d(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
            TEST_CASE_LOOP( testnum, v16, result_base, \\\n\
                VSET_VSEW_4AVL \\\n\
                %s \
                la  x1, base; \\\n\
                vle%d.v v%d, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v16, (x1); \\\n\
                la x1, f_rs1_base; \\\n\
                fl%s f1, 0(x1); \\\n\
                inst v16, v%d, f1%s; \\\n\
            )"%(i, ("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else ""), vsew, i, vsew, ("w" if vsew == 32 else "d"), i, (", v0.t" if masked else "")), file=f)
    for i in range(1, 32):
        print(" #define TEST_VSLIDE_VF_OP_rs1_%d(testnum, inst, flags, result_base, rd_base, f_rs1_base, base ) \\\n\
            TEST_CASE_LOOP( testnum, v16, result_base, \\\n\
                VSET_VSEW_4AVL \\\n\
                %s \
                la  x1, base; \\\n\
                vle%d.v v8, (x1); \\\n\
                la  x1, rd_base; \\\n\
                vle%d.v v16, (x1); \\\n\
                la x1, f_rs1_base; \\\n\
                fl%s f%d, 0(x1); \\\n\
                inst v16, v8, f%d%s; \\\n\
            )"%(i, ("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else ""), vsew, vsew, ("w" if vsew == 32 else "d"), i, i, (", v0.t" if masked else "")), file=f)

def generate_tests_vfslide(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    n=1
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfslideup/down.vx/vf Test    ------------------------------------------",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(num_group_f):
        print("  TEST_VSLIDE_VF_OP( " + str(n) + ", vfslide1up.vf, 0, f_data_slide1upans%d, "%i + "f_rd_data, " + "f_rd_data0" + ", f_data%d );"%i, file=f)
        n +=1
        print("  TEST_VSLIDE_VF_OP( " + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%i + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%i, file=f)
        n +=1

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfslideup/down.vx/vf Test    ------------------------------------------",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)",file=f)
    for i in range(1, 32):
        if i != 8 and i != 16 and i != 15  and i != 31 and i % lmul == 0:
            print("  TEST_VSLIDE_VF_OP_rd_%d( "%i + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%(i%num_group_f) + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%(i%num_group_f), file=f)
            n +=1
            print("  TEST_VSLIDE_VF_OP_rs2_%d( "%i + str(n) + ", vfslide1up.vf, 0, f_data_slide1upans%d, "%(i%num_group_f) + "f_rd_data, " + "f_rd_data0" + ", f_data%d );"%(i%num_group_f), file=f)
            n +=1
        if i != 1 and i != 7:
            print("  TEST_VSLIDE_VF_OP_rs1_%d( "%i + str(n) + ", vfslide1down.vf, 0, f_data_slide1downans%d, "%(i%num_group_f) + "f_rd_data, " + "f_rd_data%d"%(num_elem-1) + ", f_data%d );"%(i%num_group_f), file=f)
            n +=1



def generate_fdat_seg_vfslide(f, vsew):
    global rd_val
    global vma
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("f_rd_data:", file=f)
    for i in range(num_elem):
        print("f_rd_data%d:\t"%i, file=f)
        print_data_width_prefix(f, vsew)
        print("%s"%(f_rd_val[i]), file=f)
    print("",file=f)
    for i in range(num_group_f):
        # generate data
        print("f_data%d:"%i, file=f)
        for j in range(num_elem):
            print_data_width_prefix(f, vsew)
            print("%s"%f_val_grouped[i][j], file=f)
        print("", file=f)
        # generate answer for vfslideup
        print("f_data_slide1upans%d:"%i, file=f)
        for j in range(num_elem):
            if j == 0:
                print_data_width_prefix(f, vsew)
                print("%s"%(f_rd_val[j] if (masked and get_mask_bit(j) == 0) else f_rd_val[0]), file=f)
            else:
                print_data_width_prefix(f, vsew)
                print("%s"%(f_rd_val[j] if (masked and get_mask_bit(j) == 0) else f_val_grouped[i][j-1]), file=f)
        print("", file=f)
        # generate answer for vfslideup
        print("f_data_slide1downans%d:"%i, file=f)
        for j in range(num_elem):
            if j == num_elem - 1:
                print_data_width_prefix(f, vsew)
                print("%s"%(f_rd_val[j] if (masked and get_mask_bit(j) == 0) else f_rd_val[num_elem - 1]), file=f)
            else:
                print_data_width_prefix(f, vsew)
                print("%s"%(f_rd_val[j] if (masked and get_mask_bit(j) == 0) else f_val_grouped[i][j+1]), file=f)
        print("", file=f)


def print_ending_vslide(f, vlen, vsew):
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
        \n\
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)\n\
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

    generate_fdat_seg_vfslide(f, vsew)
    print_mask_origin_data_ending(f)

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


def create_empty_test_vfslide(xlen, vlen, vsew, lmul, vta, _vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))
    global num_elem
    global num_group_walking
    global num_group_f
    global walking_val_grouped
    global f_val_grouped
    global vma
    global f_val
    global f_rd_val
    num_elem = int(vlen * lmul / vsew)
    for i in range(int(num_elem / 16) + 1):
        f_val = f_val + f_val
        f_rd_val = f_rd_val + f_rd_val
    num_group_f = int(len(f_val) / num_elem)
    vma = _vma
    for i in range(num_group_f):
        temp = []
        for j in range(num_elem):
            temp.append(f_val[i*num_elem+j])
        f_val_grouped.append(temp)

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_vfslide(f, vlen, vsew)

    # Common header files
    print_common_header(instr, f)

    generate_tests_vfslide(f, lmul)

    # Common const information
    print_ending_vslide(f, vlen, vsew)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
