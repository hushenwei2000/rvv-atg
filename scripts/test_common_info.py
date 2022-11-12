import os
import re
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

def extract_operands(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    rs1_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs1_val_10]
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    rs2_val = ['{:#016x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs2_val_10]
    f.close()
    return rs1_val, rs2_val

def is_overlap(rd, rd_mul, rs, rs_mul):
    return not ((rd > rs + rs_mul - 1) or (rd + rd_mul - 1 < rs))

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

def print_loaddword_ending(f):
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
    .type tdat, @object\n\
    .size tdat, 4128\n\
    tdat:\n\
    tdat1:  .dword 0x00ff00ff\n\
    tdat2:  .dword 0xff00ff00\n\
    tdat3:  .dword 0x0ff00ff0\n\
    tdat4:  .dword 0xf00ff00f\n\
    tdat5:  .dword 0x00ff00ff\n\
    tdat6:  .dword 0xff00ff00\n\
    tdat7:  .dword 0x0ff00ff0\n\
    tdat8:  .dword 0xf00ff00f\n\
    tdat9:  .zero 4064\n\
    tdat10:  .dword 0x00ff00ff\n\
    tdat11:  .dword 0xff00ff00\n\
    tdat12:  .dword 0x0ff00ff0\n\
    tdat13:  .dword 0xf00ff00f\n\
    tdat14:  .dword 0x00ff00ff\n\
    tdat15:  .dword 0xff00ff00\n\
    tdat16:  .dword 0x0ff00ff0\n\
    tdat17:  .dword 0xf00ff00f\n\
    \n\
    idx8dat:\n\
    idx8dat1:  .byte 0\n\
    idx8dat2:  .byte 8\n\
    idx8dat3:  .byte 16\n\
    idx8dat4:  .byte 24\n\
    idx8dat5:  .word 0x00000000\n\
    idx8dat6:  .word 0x00000000\n\
    idx8dat7:  .word 0x00000000\n\
    idx8dat8:  .zero 5201314\n\
    \n\
    idx16dat:\n\
    idx16dat1:  .word 0x00080000\n\
    idx16dat2:  .word 0x00180010\n\
    idx16dat3:  .word 0x00280020\n\
    idx16dat4:  .word 0x00380030\n\
    idx16dat5:  .zero 5201314\n\
    \n\
    idx32dat:\n\
    idx32dat1:  .word 0x00000000\n\
    idx32dat2:  .word 0x00000008\n\
    idx32dat3:  .word 0x00000010\n\
    idx32dat4:  .word 0x00000018\n\
    idx32dat5:  .zero 5201314\n\
    \n\
    idx64dat:\n\
    idx64dat1:  .word 0x00000000\n\
    idx64dat2:  .word 0x00000000\n\
    idx64dat3:  .word 0x00000008\n\
    idx64dat4:  .word 0x00000000\n\
    idx64dat5:  .word 0x00000010\n\
    idx64dat6:  .word 0x00000000\n\
    idx64dat7:  .word 0x00000018\n\
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

def print_common_ending_rs1rs2rd_vvvxvi(rs1_val, rs2_val, test_num_tuple, vsew, f, generate_vi = True, generate_vx = True, generate_vv = True, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print("!!!!!loop_num=%d, vv_test_num=%d"%(loop_num, test_num_tuple[0]))
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
    if generate_vv:
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_vx:
        print("\nrd_data_vx:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_vi:
        print("\nrd_data_vi:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    print("\n\
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

def print_common_ending_rs1rs2rd_vw(rs1_val, rs2_val, test_num_tuple, vsew, f, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1, generate_wvwx = True):
    # test_num_tuple is vv_test_num, vx_test_num, wv_test_num, wx_test_num
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print("!!!!!loop_num=%d, vv_test_num=%d"%(loop_num, test_num_tuple[0]))
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
    print("rs1_data_widen:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier * 2)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print(".align %d"%(int(vsew * rs2_data_multiplier * 2 / 8)), file=f)
    print("rs2_data_widen:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier * 2)
        print("%s"%rs2_val[i], file=f)

    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
    print("rd_data_vv:", file=f)
    for i in range(test_num_tuple[0] * num_elem):
        print_data_width_prefix(f, vsew * 2)
        print("0x5201314", file=f)

    print("\nrd_data_vx:", file=f)
    for i in range(test_num_tuple[1] * num_elem):
        print_data_width_prefix(f, vsew * 2)
        print("0x5201314", file=f)

    if generate_wvwx:
        print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
        print("\nrd_data_wv:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
        print("\nrd_data_wx:", file=f)
        for i in range(test_num_tuple[3] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
    print("\n\
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

def print_common_ending_rs1rs2rd_vvvfrv(rs1_val, rs2_val, test_num_tuple, vsew, f, generate_vv = True, generate_vf = True, generate_rv = False, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print("!!!!!loop_num=%d, vv_test_num=%d"%(loop_num, test_num_tuple[0]))
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
    if generate_vv:
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_vf:
        print("\nrd_data_vf:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    if generate_rv:
        print("\nrd_data_rv:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew)
            print("0x5201314", file=f)

    print("\n\
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

def print_common_ending_rs1rs2rd_wvwf(rs1_val, rs2_val, test_num_tuple, vsew, f, generate_vv = True, generate_vf = True, rs1_data_multiplier = 1, rs2_data_multiplier = 1, rd_data_multiplier = 1, generate_wvwf = True):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

    print(test_num_tuple)
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
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
    print("rs1_data_widen:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier * 2)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rs2_data_multiplier / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier)
        print("%s"%rs2_val[i], file=f)

    print(".align %d"%(int(vsew * rs1_data_multiplier * 2 / 8)), file=f)
    print("rs2_data_widen:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew * rs2_data_multiplier * 2)
        print("%s"%rs1_val[i], file=f)

    print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
    if generate_vv:
        print("rd_data_vv:", file=f)
        for i in range(test_num_tuple[0] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)

    if generate_vf:
        print("\nrd_data_vf:", file=f)
        for i in range(test_num_tuple[1] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)

    if generate_wvwf:
        print("\n.align %d"%(int(vsew * rd_data_multiplier * 2 / 8)), file=f)
        print("\nrd_data_wv:", file=f)
        for i in range(test_num_tuple[2] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)
        print("\nrd_data_wf:", file=f)
        for i in range(test_num_tuple[3] * num_elem):
            print_data_width_prefix(f, vsew * 2)
            print("0x5201314", file=f)

    print("\n\
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

def print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs1_int_val, test_num_tuple, vsew, f, is_widen = False, is_narrow = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(len(rs1_val) / num_elem)
    lmul_1 = 1 if lmul < 1 else int(lmul)
    num_elem_1 = int(vlen * lmul_1 / vsew)

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
    rs1_data_multiplier = 2 if is_narrow else 1
    rd_data_multiplier = 2 if is_widen else 1
    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)

    print(".align %d"%(int(vsew * rs1_data_multiplier / 8)), file=f)
    print("rs1_data_int:", file=f)
    for i in range(len(rs1_int_val)):
        print_data_width_prefix(f, vsew * rs1_data_multiplier)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew * rd_data_multiplier / 8)), file=f)
    print("rd_data:", file=f)
    for i in range(test_num_tuple[0] * num_elem):
        print_data_width_prefix(f, vsew * rd_data_multiplier)
        print("0x5201314", file=f)

    print("\nrd_data_int:", file=f)
    for i in range(test_num_tuple[1] * num_elem):
        print_data_width_prefix(f, vsew * rd_data_multiplier)
        print("0x5201314", file=f)


    print("\n\
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