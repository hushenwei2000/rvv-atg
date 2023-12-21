from random import randint
import random
from scripts.test_common_info import print_data_width_prefix, gen_arr_load, print_rvmodel_data


def generate_walking_data_seg_common(element_num, vlen, vsew, f):
    # Generate walking ones
    for i in range(element_num + 1):
        print("walking_ones_dat%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            print_data_width_prefix(f, vsew)
            print("0x1" if i == j + 1 else "0x0", file=f)
        print("", file=f)

    # Generate walking zeros
    for i in range(element_num + 1):
        print("walking_zeros_dat%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            print_data_width_prefix(f, vsew)
            print("0x0" if i == j + 1 else "0x1", file=f)
        print("", file=f)


def generate_macros_common(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    print("#define TEST_VMRL_OP_rs1_1( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v16,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v8, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v16, (x1); \\\n\
            vmseq.vi v24, v8, 1; \\\n\
            vmseq.vi v8, v16, 1; \\\n\
            inst v16, v8, v24; \\\n\
            VSET_VSEW \\\n\
        )", file=f)
    for n in range(2, 32):
        if n >= 16 and n < 16 + lmul:
            print("#define TEST_VMRL_OP_rs1_%d( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v14,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, src1_addr; \\\n\
                MK_VLE_INST(sew) v8, (x1); \\\n\
                la  x1, src2_addr; \\\n\
                MK_VLE_INST(sew) v4, (x1); \\\n\
                vmseq.vi v1, v8, 1; \\\n\
                vmseq.vi v%d, v4, 1; \\\n\
                inst v14, v1, v%d; \\\n\
                VSET_VSEW \\\n\
            )" % (n, n, n), file=f)
        else:
            print("#define TEST_VMRL_OP_rs1_%d( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v14,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la  x1, src1_addr; \\\n\
                MK_VLE_INST(sew) v8, (x1); \\\n\
                la  x1, src2_addr; \\\n\
                MK_VLE_INST(sew) v16, (x1); \\\n\
                vmseq.vi v1, v8, 1; \\\n\
                vmseq.vi v%d, v16, 1; \\\n\
                inst v14, v1, v%d; \\\n\
                VSET_VSEW \\\n\
            )" % (n, n, n), file=f)
    for n in range(2, 32):
        print("#define TEST_VMRL_OP_rd_%d( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v%d,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v8, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v16, (x1); \\\n\
            vmseq.vi v1, v8, 1; \\\n\
            vmseq.vi v2, v16, 1; \\\n\
            inst v%d, v1, v2; \\\n\
            VSET_VSEW \\\n\
        )" % (n, n, n), file=f)
    print("#define TEST_VMRL_OP_rd_1( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v1,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        MK_VLE_INST(sew) v8, (x1); \\\n\
        la  x1, src2_addr; \\\n\
        MK_VLE_INST(sew) v16, (x1); \\\n\
        vmseq.vi v3, v8, 1; \\\n\
        vmseq.vi v2, v16, 1; \\\n\
        inst v1, v3, v2; \\\n\
        VSET_VSEW \\\n\
    )", file=f)
    print("#define TEST_VMRL_OP_rd_2( testnum, inst, sew,  src1_addr, src2_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v2,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        MK_VLE_INST(sew) v8, (x1); \\\n\
        la  x1, src2_addr; \\\n\
        MK_VLE_INST(sew) v16, (x1); \\\n\
        vmseq.vi v1, v8, 1; \\\n\
        vmseq.vi v3, v16, 1; \\\n\
        inst v2, v1, v3; \\\n\
        VSET_VSEW \\\n\
    )", file=f)


def generate_tests_common(instr, f, vlen, vsew, lmul):
    # lmul = 1 if lmul < 1 else int(lmul)
    n = 0
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    num_elem = int(vlen * lmul / vsew)
    num_elem_plus = num_elem + 1
    num_elem_plus_square = num_elem_plus ** 2
    num_elem_plus_square_old = num_elem_plus_square
    # If there are too many tests ( > 1000), only test some of them
    percentage = 1000 / (4 * num_elem_plus_square)
    for i in range(0, num_elem_plus_square):
        if random.random() < percentage:
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_ones_dat%d, walking_ones_dat%d );" % (
                i, instr, (vsew if vsew <= 64 else 64), i / num_elem_plus, i % num_elem_plus), file=f)
            n = n + 1

    for i in range(num_elem_plus_square, num_elem_plus_square * 2):
        if random.random() < percentage:
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_zeros_dat%d, walking_zeros_dat%d );" % (
                i, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)
            n = n + 1

    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus_square_old):
        if random.random() < percentage:
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_ones_dat%d, walking_zeros_dat%d );" % (
                i, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)
            n = n + 1

    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus_square_old):
        if random.random() < percentage:
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_zeros_dat%d, walking_ones_dat%d );" % (
                i, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)
            n = n + 1
    
    # Fully Cover rs2_val
    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus):
        if random.random() < percentage:
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_ones_dat%d, walking_zeros_dat%d );" % (
            i, instr, (vsew if vsew <= 64 else 64), i - num_elem_plus_square, i - num_elem_plus_square), file=f)
            n = n + 1

    num_elem_plus_square = num_elem_plus_square + num_elem_plus
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus):
        if random.random() < percentage:
            print("TEST_VMRL_OP( %d,  %s.mm,  %d,   walking_zeros_dat%d, walking_ones_dat%d );" % (
            i, instr, (vsew if vsew <= 64 else 64), i - num_elem_plus_square, i - num_elem_plus_square), file=f)
            n = n + 1

    return n


def print_ending_common(vlen, vsew, lmul, f, n):
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

    print("\n\
    RVTEST_DATA_END\n", file=f)
    arr = gen_arr_load(n)
    print_rvmodel_data(arr, f)
