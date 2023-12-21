import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *
import re

instr = 'vfncvt'


def generate_macros_vfncvt(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_FP_N_V_OP \n\
#define TEST_FP_N_V_OP( testnum, inst,  val1 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24,       \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew*2 + " \\\n\
        inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_FP_N_V_OP_rs1_%d( testnum, inst,  val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v24,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew*2, n) + " \\\n\
                inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_FP_N_V_OP_rd_%d( testnum, inst,  val1 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d,  "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew*2) + " \\\n\
                inst v%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

def generate_tests_vfncvt(instr, f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    global rs1_val, rs2_val, rs1_val_64, rs2_val_64
    if vsew == 32:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    # rs1_val = list(set(rs1_val))
    # rs2_val = list(set(rs2_val))

    lmul_1 = 1 if lmul < 1 else int(lmul)
    lmul_double_1 = 1 if lmul * 2 < 1 else int(lmul * 2)
    n = 0
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = min(int(min(len(rs1_val), len(rs2_val)) / num_elem), 20)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    # print("loop_num = ", loop_num);
    # print("vlen = ", vlen, ", vsew = ", vsew, ", len(rs1_val) = ", len(rs1_val), ", len(rs2_val) = ", len(rs2_val));
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    # for i in range(loop_num):
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.xu.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.x.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.rtz.xu.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.rtz.x.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.f.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.rod.f.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    
    # for i in range(loop_num):
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.f.xu.w') + "rs1_data_int+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    #     print("TEST_FP_N_V_OP( %d,  %s, "%(n, 'vfncvt.f.x.w') + "rs1_data_int+%d);"%(i*step_bytes_double), file=f)
    #     n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfcvt Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % (2*lmul) == 0 and k != 8 and not is_overlap(24, lmul_1 ,k, lmul_double_1):
            for i in range(loop_num):
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.xu.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.x.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.rtz.xu.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.rtz.x.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.f.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.rod.f.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
                n += 1
            for i in range(loop_num):
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.f.xu.w') + "rs1_data_int+%d);"%(i*step_bytes_double), file=f)
                n += 1
                print("TEST_FP_N_V_OP_rs1_%d( %d,  %s, "%(k, n, 'vfncvt.f.x.w') + "rs1_data_int+%d);"%(i*step_bytes_double), file=f)
                n += 1

        k = i % 31 + 1
        if k % lmul != 0 or k == 8 or is_overlap(k, lmul_1 ,8, lmul_double_1):
            continue
        for i in range(loop_num):
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.xu.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.x.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.rtz.xu.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.rtz.x.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.f.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.rod.f.f.w') + "rs1_data+%d);"%(i*step_bytes_double), file=f)
            n += 1
        for i in range(loop_num):
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.f.xu.w') + "rs1_data_int+%d);"%(i*step_bytes_double), file=f)
            n += 1
            print("TEST_FP_N_V_OP_rd_%d( %d,  %s, "%(k, n, 'vfncvt.f.x.w') + "rs1_data_int+%d);"%(i*step_bytes_double), file=f)
            n += 1
    return (n, 0, 0)

def create_empty_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir):
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


def create_first_test_vfncvt(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros_vfncvt(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests_vfncvt(instr, f, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vfcvt(rs1_val, rs2_val, num_tests_tuple, vsew, f, is_narrow = True)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
