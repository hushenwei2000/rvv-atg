import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *

instr = 'vfwcvt'
rs2_val = ['0x00000000', '0x80000000', '0x00000001', '0x80000001', '0x00000002', '0x807FFFFE', '0x007FFFFF', '0x807FFFFF', '0x00800000', '0x80800000', '0x00800001', '0x80855555', '0x7F7FFFFF', '0xFF7FFFFF', '0x3F800000', '0xBF800000', '0x00000000', '0x80000000', '0x00000001', '0x80000001', '0x00000002', '0x807FFFFE', '0x007FFFFF', '0x807FFFFF', '0x00800000', '0x80800000', '0x00800001', '0x80855555', '0x7F7FFFFF', '0xFF7FFFFF', '0x3F800000', '0xBF800000', ]


def generate_macros_vfwcvt(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    print("#undef TEST_FP_W_V_OP \n\
#define TEST_FP_W_V_OP( testnum, inst, flags, result, val1 ) \\\n\
    TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8; \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_W_V_OP_rs1_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_W_FP( testnum, v24, flags, result, v8, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v%d; "%n + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_W_V_OP_rd_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_W_FP( testnum, v%d, flags, result, v8, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v8; "%n + " \\\n\
            )", file = f)

def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0


def generate_tests_vfwcvt(instr, f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    rs1_val = list(set(rs1_val))
    rs2_val = list(set(rs2_val))

    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    # for i in range(loop_num):
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.rtz.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.rtz.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.f.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    
    # for i in range(loop_num):
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.f.xu.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_W_V_OP( %d,  %s, 0xff100, "%(n, 'vfwcvt.f.x.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
    #     n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul == 0 and k != 8:
            for i in range(loop_num):
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.rtz.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.rtz.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.f.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1
            for i in range(loop_num):
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.f.xu.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_W_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.f.x.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
                n += 1

        k = i % 31 + 1
        if k % (2*lmul) != 0 or k == 8:
            continue
        for i in range(loop_num):
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.rtz.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.rtz.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.f.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
        for i in range(loop_num):
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.f.xu.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_W_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfwcvt.f.x.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes_double, i*step_bytes), file=f)
            n += 1
    return (n, 0)

def print_ending(f):
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


def create_empty_test_vfwcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_W_FP_INT_OP( 1,  %s.xu.f.v, 0, 1, 1);"%instr, file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfwcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros_vfwcvt(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vfwcvt(instr, f, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs2_val, num_tests_tuple, vsew, f, is_widen = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
