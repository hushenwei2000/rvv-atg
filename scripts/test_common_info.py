def print_common_header(instr, f):
    print("#----------------------------------------------------------------------------- \n\
    # %s.S\n\
    #-----------------------------------------------------------------------------\n\
    #\n\
    # Test %s instructions.\n\
    #\n\n\
    #include \"model_test.h\"\n\
    #include \"arch_test.h\"\n\
    #include \"riscv_test.h\"\n\
    #include \"test_macros_vector.h\"\n" % (instr, instr),file=f)

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

def print_data_width_prefix(f, vsew):
    if vsew == 8:
        print(".byte", end="\t", file=f)
    elif vsew == 16:
        print(".hword", end="\t", file=f)
    elif vsew == 32:
        print(".word", end="\t", file=f)
    elif vsew == 64:
        print(".dword", end="\t", file=f)


def print_load_ending(f):
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
    .type tdat, @object\n\
    .size tdat, 4128\n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdat9:  .zero 4064\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    \n\
    idx8dat:\n\
    idx8dat1:  .byte 0\n\
    idx8dat2:  .byte 4\n\
    idx8dat3:  .byte 8\n\
    idx8dat4:  .byte 12\n\
    idx8dat5:  .word 0x00000000\n\
    idx8dat6:  .word 0x00000000\n\
    idx8dat7:  .word 0x00000000\n\
    idx8dat8:  .zero 5201314\n\
    \n\
    idx16dat:\n\
    idx16dat1:  .word 0x00040000\n\
    idx16dat2:  .word 0x000c0008\n\
    idx16dat3:  .word 0x00140010\n\
    idx16dat4:  .word 0x001c0018\n\
    idx16dat5:  .zero 5201314\n\
    \n\
    idx32dat:\n\
    idx32dat1:  .word 0x00000000\n\
    idx32dat2:  .word 0x00000004\n\
    idx32dat3:  .word 0x00000008\n\
    idx32dat4:  .word 0x0000000c\n\
    idx32dat5:  .zero 5201314\n\
    \n\
    idx64dat:\n\
    idx64dat1:  .word 0x00000000\n\
    idx64dat2:  .word 0x00000000\n\
    idx64dat3:  .word 0x00000004\n\
    idx64dat4:  .word 0x00000000\n\
    idx64dat5:  .word 0x00000008\n\
    idx64dat6:  .word 0x00000000\n\
    idx64dat7:  .word 0x0000000c\n\
    idx64dat8:  .word 0x00000000\n\
    idx64dat9:  .zero 5201314\n\
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


def print_loadls_ending(f):
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
    .type tsdat, @object\n\
    .size tsdat, 1049856\n\
    tsdat:\n\
    tsdat1:  .zero 524800\n\
    tsdat2:  .word 0x00ff00ff\n\
    tsdat3:  .word 0xff00ff00\n\
    tsdat4:  .word 0x0ff00ff0\n\
    tsdat5:  .word 0xf00ff00f\n\
    tsdat6:  .word 0x00ff00ff\n\
    tsdat7:  .word 0xff00ff00\n\
    tsdat8:  .word 0x0ff00ff0\n\
    tsdat9:  .word 0xf00ff00f\n\
    tsdat10: .zero 524800\n\
    \n\
    .type tdat, @object\n\
    .size tdat, 4128\n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdat9:  .zero 4064\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    \n\
    idx8dat:\n\
    idx8dat1:  .byte 0\n\
    idx8dat2:  .byte 4\n\
    idx8dat3:  .byte 8\n\
    idx8dat4:  .byte 12\n\
    idx8dat5:  .word 0x00000000\n\
    idx8dat6:  .word 0x00000000\n\
    idx8dat7:  .word 0x00000000\n\
    \n\
    idx16dat:\n\
    idx16dat1:  .word 0x00040000\n\
    idx16dat2:  .word 0x000c0008\n\
    idx16dat3:  .word 0x00140010\n\
    idx16dat4:  .word 0x001c0018\n\
    \n\
    idx32dat:\n\
    idx32dat1:  .word 0x00000000\n\
    idx32dat2:  .word 0x00000004\n\
    idx32dat3:  .word 0x00000008\n\
    idx32dat4:  .word 0x0000000c\n\
    \n\
    idx64dat:\n\
    idx64dat1:  .word 0x00000000\n\
    idx64dat2:  .word 0x00000000\n\
    idx64dat3:  .word 0x00000004\n\
    idx64dat4:  .word 0x00000000\n\
    idx64dat5:  .word 0x00000008\n\
    idx64dat6:  .word 0x00000000\n\
    idx64dat7:  .word 0x0000000c\n\
    idx64dat8:  .word 0x00000000\n\
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


def print_loadlr_ending(f):
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
    .type tdat, @object\n\
    .size tdat, 8448\n\
    tdat:\n\
    tdat1:  .word 0x00ff00ff\n\
    tdat2:  .word 0xff00ff00\n\
    tdat3:  .word 0x0ff00ff0\n\
    tdat4:  .word 0xf00ff00f\n\
    tdat5:  .word 0x00ff00ff\n\
    tdat6:  .word 0xff00ff00\n\
    tdat7:  .word 0x0ff00ff0\n\
    tdat8:  .word 0xf00ff00f\n\
    tdat9:  .zero 32\n\
    tdat10:  .word 0x00ff00ff\n\
    tdat11:  .word 0xff00ff00\n\
    tdat12:  .word 0x0ff00ff0\n\
    tdat13:  .word 0xf00ff00f\n\
    tdat14:  .word 0x00ff00ff\n\
    tdat15:  .word 0xff00ff00\n\
    tdat16:  .word 0x0ff00ff0\n\
    tdat17:  .word 0xf00ff00f\n\
    tdta18:  .zero 32\n\
    tdat19:  .word 0x00ff00ff\n\
    tdat20:  .word 0xff00ff00\n\
    tdat21:  .word 0x0ff00ff0\n\
    tdat22:  .word 0xf00ff00f\n\
    tdat23:  .word 0x00ff00ff\n\
    tdat24:  .word 0xff00ff00\n\
    tdat25:  .word 0x0ff00ff0\n\
    tdat26:  .word 0xf00ff00f\n\
    tdta27:  .zero 32\n\
    tdta28:  .zero 7584\n\
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
