import logging
import os
from scripts.test_common_info import *
import re

instr = 'vrgather'
rs1_val = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647, 2147483648, 2863311530, 4294967294, 4294967293, 4294967291, 4294967287, 4294967279, 4294967263, 4294967231, 4294967167, 4294967039, 4294966783, 4294966271, 4294965247, 4294963199, 4294959103, 4294950911, 4294934527, 4294901759, 4294836223, 4294705151, 4294443007, 4293918719, 4292870143, 4290772991, 4286578687, 4278190079, 4261412863, 4227858431, 4160749567, 4026531839, 3758096383, 3221225471]
rs2_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]


def generate_macros(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#define TEST_VV_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#define TEST_VX_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v16, v8, x1%s;"%(", v0.t" if masked else "") + " ; \\\n\
        )", file=f)
    print("#define TEST_VI_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v8, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " ; \\\n\
        )", file=f)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n)  + " \\\n\
            inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VV_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, result,"%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v%d, v16, v8%s;"%(n, (", v0.t" if masked else ""))+" \\\n\
        ) ", file=f)
    print("#define TEST_VV_OP_rd8( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v8, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v8, v24, v16%s;"%(", v0.t" if masked else "") + " ; \\\n\
        )", file=f)
    print("#define TEST_VV_OP_rd16( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)


def extract_operands(f):
    global rs1_val
    global rs2_val
    return rs1_val, rs2_val


def generate_tests(f, rs1_val, rs2_val, lmul, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s, "%(instr, instr_suffix) + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
        for i in range(min(32, loop_num)):     
            k = i%31+1
            if k % lmul != 0 or k == 24:
                continue
            n+=1
            print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
            
            k = i%30+2
            if k % lmul != 0 or k == 8 or k == 16 or k == 24:
                continue
            n +=1
            print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
                instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[0]), file=f)
    vx_test_num = n - vv_test_num
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"rd_data_vi+%d, rs2_data+%d, 15)"%(i*step_bytes, i*step_bytes), file=f)
    vi_test_num = n - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)


def create_empty_test_vrgather(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    num_tests_tuple = generate_tests(f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vvvxvi(rs1_val, rs2_val, num_tests_tuple, vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
