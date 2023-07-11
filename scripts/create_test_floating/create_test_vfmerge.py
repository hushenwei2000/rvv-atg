import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *
import re

instr = 'vfmerge'

def generate_macros(f, vsew):
    print("#undef TEST_FP_VF_OP_AFTER_VMSEQ \n\
#define TEST_FP_VF_OP_AFTER_VMSEQ( testnum, flags, result, val1, val2, vmseqop1, vmseqop2 ) \\\n\
    TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
        VSET_VSEW_4AVL \\\n\
        li x7, MASK_VSEW(vmseqop1); \\\n\
        vmv.v.x v8, x7; \\\n\
        vmseq.vi v0, v8, vmseqop2; \\\n\
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        fl%s f1, (x7);"%(('d' if vsew == 64 else 'w')) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        vfmerge.vfm v24, v8, f1, v0;  \\\n\
    )", file=f)
    for n in range(1, 32):
        # if n == 2 or n == 14:
        #     continue
        print("#define TEST_FP_VF_OP_AFTER_VMSEQ_rs1_%d( testnum, flags, result, val1, val2, vmseqop1, vmseqop2 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v24, flags, result, v8,     \\\n\
                VSET_VSEW_4AVL \\\n\
                li x7, MASK_VSEW(vmseqop1); \\\n\
                vmv.v.x v8, x7; \\\n\
                vmseq.vi v0, v8, vmseqop2; \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                fl%s f%d, (x7);"%(('d' if vsew == 64 else 'w'), n) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                vfmerge.vfm v24, v8, f%d, v0; "%n + " \\\n\
            )", file = f)

    for n in range(1, 32):
        # if n == 1:
        #     continue
        print("#define TEST_FP_VF_OP_AFTER_VMSEQ_rd_%d( testnum, flags, result, val1, val2, vmseqop1, vmseqop2 )"%n + " \\\n\
            TEST_CASE_LOOP_FP( testnum, v%d, flags, result, v8,  "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                li x7, MASK_VSEW(vmseqop1); \\\n\
                vmv.v.x v8, x7; \\\n\
                vmseq.vi v0, v8, vmseqop2; \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                fl%s f1, (x7);"%(('d' if vsew == 64 else 'w')) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                vfmerge.vfm v%d, v8, f1, v0; "%n + " \\\n\
            )", file = f)


def generate_tests(f, vsew, lmul):
    global rs1_val, rs2_val
    if vsew == 64:
        rs1_val = rs1_val_64
        rs2_val = rs2_val_64
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0

    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfmerge.vfm Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(loop_num):        
        n += 1
        print("TEST_FP_VF_OP_AFTER_VMSEQ( %d,        0xff100,        rd_data_vf+%d, rs2_data+%d, rs1_data+%d, 0xe, 1);"%(n, i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfmerge.vfm Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(min(32,loop_num)):
        k = i%31+1  
        if not (k == 8 or k == 16 or k == 24 or k % lmul != 0):
            n += 1
            print("  TEST_FP_VF_OP_AFTER_VMSEQ_rd_%d( "%k+str(n)+", 0xff100, " + "rd_data_vf+%d, rs2_data+%d, rs1_data+%d, 0xe, 1);"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)

        k = i%31+1  
        if not (k == 8 or k == 16 or k == 24 or k % lmul != 0):
            n += 1
            print("  TEST_FP_VF_OP_AFTER_VMSEQ_rs1_%d( "%k+str(n)+", 0xff100, " + "rd_data_vf+%d, rs2_data+%d, rs1_data+%d, 0xe, 1);"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    return (0, n, 0)


def create_empty_test_vfmerge(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VFMVF_OP( 1,  fdat_rs1_0 );", file=f)

    # Common const information
    print_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfmerge(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros(f, vsew)

    # Generate tests
    num_tests_tuple = generate_tests(f, vsew, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vvvfrv(rs1_val, rs2_val, num_tests_tuple, vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
