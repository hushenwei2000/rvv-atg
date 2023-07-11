import logging
import os
from scripts.create_test_mask.create_test_common import *
from scripts.test_common_info import *
import re

instr = 'viota'


def generate_walking_answer_seg_viota(element_num, vlen, vsew, f):
    # mask_value_stripped = mask_data_ending[:int((element_num+1)/32)] # Each mask value is 32bits
    # mask_value_bitsvector = [] # 0,0,0,1,1,0, etc.
    # mask = 0b1
    # for i in range (element_num + 1):
    #     mask_value_bitsvector.append((int(mask_data_ending[int(i/32)], 16) & mask) >> i)
    #     mask = mask << 1
    # vma = int(float(os.environ['RVV_ATG_VMA']))
    # print(mask_value_bitsvector)
    # Generate prefix-sum of 1 for WalkingOnes
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    vma = os.environ["RVV_ATG_VMA"]
    agnostic_type = int(os.environ['RVV_ATG_AGNOSTIC_TYPE'])
    for i in range(element_num + 1):
        print("walking_ones_ans%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            print_data_width_prefix(f, vsew)
            if masked and get_mask_bit(j) == 0:
                print("0x%d"%(1 if (vma and agnostic_type == 1) else 2),file=f)
            else:
                if i == 0 or i == element_num:
                    print("0x0", file=f)
                else:
                    if j < i:
                        print("0x0", file=f)
                    else:
                        print("0x%d"%(0 if (masked and get_mask_bit(i-1) == 0) else 1), file=f)
        print("", file=f)

    # Generate prefix-sum of 1 for WalkingZeros
    for i in range(element_num + 1):
        print("walking_zeros_ans%d:" % i, file=f)
        prefix_sum = 0
        for j in range(element_num):
            print("\t", end="", file=f)
            print_data_width_prefix(f, vsew)
            if masked and get_mask_bit(j) == 0:
                print("0x%d"%(1 if (vma and agnostic_type == 1) else 2),file=f)
            else:
                print("%d"%prefix_sum, file=f)
                if i != j + 1:
                    prefix_sum = prefix_sum + 1
        print("", file=f)


def generate_macros_viota(f, vsew, lmul):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    lmul = 1 if lmul < 1 else int(lmul)
    print("#undef TEST_VIOTA_OP", file=f)
    print("#define TEST_VIOTA_OP( testnum, inst, result_addr, src1_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la  x1, src1_addr; \\\n\
        la  x7, result_addr; \\\n\
        vle%d.v v8, (x1);"%vsew +" \\\n\
        vmseq.vi v2, v8, 1; \\\n\
        vmv.v.i v16, 2;\\\n\
        inst v16, v2%s; \\\n\
        )"%(", v0.t" if masked else ""), file=f)
    # generate the macro， 测试v1-v32源寄存器
    print("#define TEST_VIOTA_OP_rs2_8( testnum, inst, result_addr, src1_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la  x1, src1_addr; \\\n\
        la  x7, result_addr; \\\n\
        vle%d.v v16, (x1); \\\n\
        vmseq.vi v8, v16, 1; \\\n\
        vmv.v.i v16, 2;\\\n\
        inst v16, v8%s; \\\n\
        )"%(vsew, ", v0.t" if masked else ""), file=f)
    print("#define TEST_VIOTA_OP_rs2_16( testnum, inst, result_addr, src1_addr ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la  x1, src1_addr; \\\n\
        la  x7, result_addr; \\\n\
        vle%d.v v8, (x1); \\\n\
        vmseq.vi v16, v8, 1; \\\n\
        vmv.v.i v8, 2;\\\n\
        inst v8, v16%s; \\\n\
        )"%(vsew, ", v0.t" if masked else ""), file=f)

    for n in range(1, 32):
        if n == 8 or n == 16 or (8 + lmul - 1 >= n and n + lmul - 1 >= 8) or (n >= 16 and 16 + lmul - 1 >= n): #vmseq no_overlap and viota no_overlap
            continue
        print("#define TEST_VIOTA_OP_rs2_%d( testnum, inst, result_addr, src1_addr )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v16, result_addr, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la  x1, src1_addr; \\\n\
        la  x7, result_addr; \\\n\
        vle%d.v v8, (x1); \\\n\
        vmseq.vi v%d, v8, 1; \\\n\
        vmv.v.i v16, 2;\\\n\
        inst v16, v%d%s; \\\n\
        )" % (vsew, n, n, ", v0.t" if masked else ""), file=f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 2:
            continue
        print("#define TEST_VIOTA_OP_rd_%d( testnum, inst, result_addr, src1_addr )"%n + "  \\\n\
        TEST_CASE_LOOP( testnum, v%d, result_addr,"%n + "  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la  x1, src1_addr; \\\n\
        la  x7, result_addr; \\\n\
        vle%d.v v8, (x1); \\\n\
        vmseq.vi v2, v8, 1; \\\n\
        vmv.v.i v%d, 2;\\\n\
        inst v%d, v2%s; \\\n\
        )" % (vsew, n, n, ", v0.t" if masked else ""), file=f)


def generate_tests_viota(instr, f, vlen, vsew, lmul):
    num_test = 1
    num_elem = int(vlen * lmul / vsew)
    lmul = 1 if lmul < 1 else int(lmul)
    num_elem_plus = num_elem + 1
    ####################viota######################################################################################################
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    for i in range(0, num_elem_plus, 10):
        print("TEST_VIOTA_OP( %d,  %s.m, walking_ones_ans%d, walking_ones_dat%d );" % (
            num_test, instr, i, i), file=f)
        num_test = num_test + 1
        print("TEST_VIOTA_OP( %d,  %s.m, walking_zeros_ans%d, walking_zeros_dat%d);" % (
            num_test, instr, i, i), file=f)
        num_test = num_test + 1

    print("  #-------------------------------------------------------------", file=f)
    print("  # %s Tests (different register)" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

    for i in range(1, 32):
        if i % lmul == 0:
            if i == 2:
                continue
            else:
                print("TEST_VIOTA_OP_rd_%d( %d,  %s.m, walking_zeros_ans%d, walking_zeros_dat%d );" % (
                    i, num_test, instr, i % num_elem_plus, i % num_elem_plus), file=f)
                num_test = num_test + 1
    for i in range(1, 32):
        if (8 + lmul - 1 < i or i + lmul - 1 < 8) and (i < 16 or 16 + lmul - 1 < i): # rs2 and rd no overlap each other
            print("TEST_VIOTA_OP_rs2_%d( %d,  %s.m, walking_ones_ans%d, walking_ones_dat%d );" % (
                i, num_test, instr, i % num_elem_plus, i % num_elem_plus), file=f)
            num_test = num_test + 1


def print_ending_viota(vlen, vsew, lmul, f):
    # generate const information
    print("  RVTEST_SIGBASE( x20,signature_x20_2)\n\
        \n\
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

    generate_walking_data_seg_common(int(vlen * lmul/vsew), int(vlen), int(vsew), f)
    generate_walking_answer_seg_viota(int(vlen * lmul/vsew), int(vlen), int(vsew), f)
    print_mask_origin_data_ending(f)

    print("\n\
    RVTEST_DATA_END\n\
    RVMODEL_DATA_BEGIN\n\
    signature_x12_0:\n\
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
    signature_x24_0:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x24_1:\n\
        .fill 512,4,0xdeadbeef\n\
    \n\
    \n\
    signature_x24_2:\n\
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
    RVMODEL_DATA_END\n\
    ", file=f)


def create_empty_test_viota(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    generate_macros_viota(f, vsew, lmul)

    # Common header files
    print_common_header(instr, f)

    generate_tests_viota(instr, f, vlen, vsew, lmul)

    # Common const information
    print_ending_viota(vlen, vsew, lmul, f)

    f.close()

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path
