import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import valid_aligned_regs

instr = 'vfrsqrt7'

rs2_val_32 = ['0x00000000', '0x80000000', '0x00000001', '0x80000001', '0x00000002', '0x807FFFFE', '0x007FFFFF', '0x807FFFFF', '0x00800000', '0x80800000', '0x00800001', '0x80855555', '0x7F7FFFFF', '0xFF7FFFFF', '0x3F800000', '0xBF800000', ]
rs2_val_64 = ['0x0000000000000000', '0x8000000000000000', '0x0000000000000001', '0x8000000000000001', '0x0000000000000002', '0x8000000000000002', '0x000FFFFFFFFFFFFF', '0x800FFFFFFFFFFFFF', '0x0010000000000000', '0x8010000000000000', '0x0010000000000002', '0x8010000000000002', '0x7FEFFFFFFFFFFFFF', '0xFFEFFFFFFFFFFFFF', '0x3FF0000000000000', '0xBF80000000000000', ]


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n % lmul != 0: continue
        rd = valid_aligned_regs(n)[0]
        print("#define TEST_FP_HEX_1OPERAND_OP_2%d( testnum, inst, flags, result, val ) \\\n\
        TEST_CASE( testnum, v%d, result, \\\n\
            li x7, MASK_VSEW(val); \\\n\
            vmv.v.x v%d, x7; \\\n\
            inst v%d, v%d; \\\n\
            frflags a1; \\\n\
            li a2, flags; \\\n\
        )"%(n, rd, n, rd, n),file=f)
    for n in range(1,32):
        if n % lmul != 0: continue
        rs2 = valid_aligned_regs(n)[0]
        print("#define TEST_FP_HEX_1OPERAND_OP_rd%d( testnum, inst, flags, result, val ) \\\n\
        TEST_CASE( testnum, v%d, result, \\\n\
            li x7, MASK_VSEW(val); \\\n\
            vmv.v.x v%d, x7; \\\n\
            inst v%d, v%d; \\\n\
            frflags a1; \\\n\
            li a2, flags; \\\n\
        )"%(n, n, rs2, n, rs2),file=f)


def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0


def generate_tests(f, vsew, lmul):
    if vsew == 32:
        rs2_val = rs2_val_32
    elif vsew == 64:
        rs2_val = rs2_val_64

    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfrsqrt7.v Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_0)",file=f)
    for i in range(len(rs2_val)):
        n += 1
        print("  TEST_FP_HEX_1OPERAND_OP( "+str(n)+",  vfrsqrt7.v, 0xff100, 5201314, "+rs2_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfrsqrt7.v Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(len(2*rs2_val)):     
        k = i % 31 + 1
        if k % lmul != 0: continue
        n += 1
        print("  TEST_FP_HEX_1OPERAND_OP_rd%d( "%k+str(n)+",  vfrsqrt7.v, 0xff100, 5201314, "+(2*rs2_val)[i]+" );",file=f)

        n += 1
        print("  TEST_FP_HEX_1OPERAND_OP_2%d( "%k+str(n)+",  vfrsqrt7.v, 0xff100, 5201314, "+(2*rs2_val)[i]+" );",file=f)


def print_ending(f):
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


def create_empty_test_vfrsqrt7_b1(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_b1_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_FP_HEX_1OPERAND_OP( 1,  %s.v, 0, 1, 1);"%instr, file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfrsqrt7_b1(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_b1_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    generate_tests(f, vsew, lmul)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
