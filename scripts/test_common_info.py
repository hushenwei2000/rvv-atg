def print_common_header(instr, f):
    print("#----------------------------------------------------------------------------- \n\
    # %s.S\n\
    #-----------------------------------------------------------------------------\n\
    #\n\
    # Test vsub instructions.\n\
    #\n\n\
    #include \"model_test.h\"\n\
    #include \"arch_test.h\"\n\
    #include \"riscv_test.h\"\n\
    #include \"test_macros_vector.h\"\n" % instr, file=f)

    print("RVTEST_ISA(\"RV64RV64IMAFDCVZicsr\")\n\
    \n\
    .section .text.init\n\
    .globl rvtest_entry_point\n\
    rvtest_entry_point:\n\
    \n\
    #ifdef TEST_CASE_1\n\
    \n\
    RVTEST_CASE(0,\"//check ISA:=regex(.*64.*);check ISA:=regex(.*V.*);def TEST_CASE_1=True;\",%s)\n\
    \n\
    RVTEST_RV64UV\n\
    RVMODEL_BOOT\n\
    RVTEST_CODE_BEGIN\n\
    RVTEST_VSET\n\
    " % instr, file=f)


def print_common_ending(f):
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
