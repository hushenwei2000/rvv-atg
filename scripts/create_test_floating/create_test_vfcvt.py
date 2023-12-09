import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *
import re

instr = 'vfcvt'


def generate_fdat_seg(f):
    print("fdat_rs1:", file=f)
    for i in range(len(rs1_val)):
        print("fdat_rs1_" + str(i) + ":  .word " + rs1_val[i], file=f)
    print("", file=f)
    print("fdat_rs2:", file=f)
    for i in range(len(rs2_val)):
        print("fdat_rs2_" + str(i) + ":  .word " + rs2_val[i], file=f)


def generate_macros_vfcvt(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    print("#undef TEST_FP_V_OP \n\
#define TEST_FP_V_OP( testnum, inst, flags, result, val1 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8; \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_V_OP_rs1_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v%d; "%n + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_V_OP_rd_%d( testnum, inst, flags, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v8; "%n + " \\\n\
            )", file = f)

def extract_operands(f, rpt_path):
    # Floating pooints tests don't need to extract operands, rs1 and rs2 are fixed
    return 0

def generate_tests_vfcvt(instr, f, lmul):
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
    loop_num = min(int(min(len(rs1_val), len(rs2_val)) / num_elem), 20)
    step_bytes = int(vlen * lmul / 8)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    # for i in range(loop_num):
    #     print("TEST_FP_V_OP( %d,  %s, 0xff100, "%(n, 'vfcvt.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_V_OP( %d,  %s, 0xff100, "%(n, 'vfcvt.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_V_OP( %d,  %s, 0xff100, "%(n, 'vfcvt.rtz.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_V_OP( %d,  %s, 0xff100, "%(n, 'vfcvt.rtz.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
    #     n += 1
    
    # for i in range(loop_num):
    #     print("TEST_FP_V_OP( %d,  %s, 0xff100, "%(n, 'vfcvt.f.xu.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes), file=f)
    #     n += 1
    #     print("TEST_FP_V_OP( %d,  %s, 0xff100, "%(n, 'vfcvt.f.x.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes), file=f)
    #     n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul == 0 and k != 24:
            for i in range(loop_num):
                print("TEST_FP_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.rtz.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.rtz.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
                n += 1
            for i in range(loop_num):
                print("TEST_FP_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.f.xu.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes), file=f)
                n += 1
                print("TEST_FP_V_OP_rs1_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.f.x.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes), file=f)
                n += 1

        k = i % 31 + 1
        if k % lmul != 0 or k == 8:
            continue
        for i in range(loop_num):
            print("TEST_FP_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.rtz.xu.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.rtz.x.f.v') + "rd_data+%d, rs1_data+%d);"%(n*step_bytes, i*step_bytes), file=f)
            n += 1
        for i in range(loop_num):
            print("TEST_FP_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.f.xu.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes), file=f)
            n += 1
            print("TEST_FP_V_OP_rd_%d( %d,  %s, 0xff100, "%(k, n, 'vfcvt.f.x.v') + "rd_data+%d, rs1_data_int+%d);"%(n*step_bytes, i*step_bytes), file=f)
            n += 1
    return (n, 0, 0)

def create_empty_test_vfcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfcvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros_vfcvt(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vfcvt(instr, f, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs2_val, num_tests_tuple, vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
