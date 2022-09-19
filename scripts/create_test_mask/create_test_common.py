from scripts.test_common_info import print_data_width_prefix


def generate_walking_data_seg_common(element_num, vlen, f):
    # Generate walking ones
    for i in range(element_num + 1):
        print("walking_ones_dat%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            element_width = vlen / element_num
            print_data_width_prefix(f, element_width)
            print("0x1" if i == j + 1 else "0x0", file=f)
        print("", file=f)

    # Generate walking zeros
    for i in range(element_num + 1):
        print("walking_zeros_dat%d:" % i, file=f)
        for j in range(element_num):
            print("\t", end="", file=f)
            element_width = vlen / element_num
            print_data_width_prefix(f, element_width)
            print("0x0" if i == j + 1 else "0x1", file=f)
        print("", file=f)


def generate_macros_common(f):
    print("#define TEST_VMRL_OP_rs1_1( testnum, inst, sew, result, src1_addr, src2_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v5, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v6, (x1); \\\n\
            vmseq.vi v1, v5, 1; \\\n\
            vmseq.vi v2, v6, 1; \\\n\
            inst v3, v2, v1; \\\n\
            VSET_VSEW \\\n\
        )", file=f)
    for n in range(2, 32):
        print("#define TEST_VMRL_OP_rs1_%d( testnum, inst, sew, result, src1_addr, src2_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v5, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v6, (x1); \\\n\
            vmseq.vi v1, v5, 1; \\\n\
            vmseq.vi v%d, v6, 1; \\\n\
            inst v14, v1, v%d; \\\n\
            VSET_VSEW \\\n\
        )" % (n, n, n), file=f)
    for n in range(2, 32):
        print("#define TEST_VMRL_OP_rd_%d( testnum, inst, sew, result, src1_addr, src2_addr ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la  x1, src1_addr; \\\n\
            MK_VLE_INST(sew) v5, (x1); \\\n\
            la  x1, src2_addr; \\\n\
            MK_VLE_INST(sew) v6, (x1); \\\n\
            vmseq.vi v1, v5, 1; \\\n\
            vmseq.vi v2, v6, 1; \\\n\
            inst v%d, v1, v2; \\\n\
            VSET_VSEW \\\n\
        )" % (n, n), file=f)
    print("#define TEST_VMRL_OP_rd_1( testnum, inst, sew, result, src1_addr, src2_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        MK_VLE_INST(sew) v5, (x1); \\\n\
        la  x1, src2_addr; \\\n\
        MK_VLE_INST(sew) v6, (x1); \\\n\
        vmseq.vi v3, v5, 1; \\\n\
        vmseq.vi v2, v6, 1; \\\n\
        inst v1, v3, v2; \\\n\
        VSET_VSEW \\\n\
    )", file=f)
    print("#define TEST_VMRL_OP_rd_2( testnum, inst, sew, result, src1_addr, src2_addr ) \\\n\
    TEST_CASE_MASK_4VL( testnum, v14, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la  x1, src1_addr; \\\n\
        MK_VLE_INST(sew) v5, (x1); \\\n\
        la  x1, src2_addr; \\\n\
        MK_VLE_INST(sew) v6, (x1); \\\n\
        vmseq.vi v1, v5, 1; \\\n\
        vmseq.vi v3, v6, 1; \\\n\
        inst v2, v1, v3; \\\n\
        VSET_VSEW \\\n\
    )", file=f)


def generate_tests_common(instr, f, vlen, vsew):
    print("  #-------------------------------------------------------------", file=f)
    print("  # %s tests" % instr, file=f)
    print("  #-------------------------------------------------------------", file=f)
    num_elem = int(vlen / vsew)
    num_elem_plus = num_elem + 1
    num_elem_plus_square = num_elem_plus ** 2
    num_elem_plus_square_old = num_elem_plus_square
    for i in range(0, num_elem_plus_square):
        print("TEST_VMRL_OP( %d,  %s.mm,  %d,  5201314, walking_ones_dat%d, walking_ones_dat%d );" % (
            i, instr, (vsew if vsew <= 64 else 64), i / num_elem_plus, i % num_elem_plus), file=f)

    for i in range(num_elem_plus_square, num_elem_plus_square * 2):
        print("TEST_VMRL_OP( %d,  %s.mm,  %d,  5201314, walking_zeros_dat%d, walking_zeros_dat%d );" % (
            i, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)

    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus_square_old):
        print("TEST_VMRL_OP( %d,  %s.mm,  %d,  5201314, walking_ones_dat%d, walking_zeros_dat%d );" % (
            i, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)

    num_elem_plus_square = num_elem_plus_square + num_elem_plus_square_old
    for i in range(num_elem_plus_square, num_elem_plus_square + num_elem_plus_square_old):
        print("TEST_VMRL_OP( %d,  %s.mm,  %d,  5201314, walking_zeros_dat%d, walking_ones_dat%d );" % (
            i, instr, (vsew if vsew <= 64 else 64), (i - num_elem_plus_square) / num_elem_plus, (i - num_elem_plus_square) % num_elem_plus), file=f)

    # generate cover different registers
    print("  #-------------------------------------------------------------", file=f)
    print("  # vmandnot Tests (different register)", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)

    num_test = num_elem_plus_square + num_elem_plus_square
    for i in range(1, 32):
        print("TEST_VMRL_OP_rd_%d( %d,  %s.mm,  %d,  5201314, walking_zeros_dat0, walking_ones_dat1 );" % (
            i, num_test, instr, (vsew if vsew <= 64 else 64),), file=f)
        num_test = num_test + 1
    for i in range(2, 32):
        print("TEST_VMRL_OP_rs1_%d( %d,  %s.mm,  %d,  5201314, walking_zeros_dat0, walking_ones_dat1 );" % (
            i, num_test, instr, (vsew if vsew <= 64 else 64),), file=f)
        num_test = num_test + 1


def print_ending_common(vlen, vsew, f):
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

    generate_walking_data_seg_common(int(vlen/vsew), int(vlen), f)

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
