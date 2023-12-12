import logging
import os
from random import randint
from scripts.test_common_info import *
import re

instr = 'vrgatherei16'
rs1_val = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647, 2147483648, 2863311530, 4294967294, 4294967293, 4294967291, 4294967287, 4294967279, 4294967263, 4294967231, 4294967167, 4294967039, 4294966783, 4294966271, 4294965247, 4294963199, 4294959103, 4294950911, 4294934527, 4294901759, 4294836223, 4294705151, 4294443007, 4293918719, 4292870143, 4290772991, 4286578687, 4278190079, 4261412863, 4227858431, 4160749567, 4026531839, 3758096383, 3221225471]
val_64 = [4294967296, 8589934592, 17179869184, 34359738368, 68719476736, 137438953472, 274877906944, 549755813888, 1099511627776, 2199023255552, 4398046511104, 8796093022208, 17592186044416, 35184372088832, 70368744177664, 140737488355328, 281474976710656, 562949953421312, 1125899906842624, 2251799813685248, 4503599627370496, 9007199254740992, 18014398509481984, 36028797018963968, 72057594037927936, 144115188075855872, 288230376151711744, 576460752303423488, 1152921504606846976, 2305843009213693952, 4611686018427387904, -922337203685477580, -2147483649, -4294967297, -8589934593, -17179869185, -34359738369, -68719476737, -137438953473, -274877906945, -549755813889, -1099511627777, -2199023255553, -4398046511105, -8796093022209, -17592186044417, -35184372088833, -70368744177665, -140737488355329, -281474976710657, -562949953421313, -1125899906842625, -2251799813685249, -4503599627370497, -9007199254740993, -18014398509481985, -36028797018963969, -72057594037927937, -144115188075855873, -288230376151711745, -576460752303423489, -1152921504606846977, -2305843009213693953, -4611686018427387905, 9223372036854775807,  6148914691236517205, -6148914691236517206, -9223372036854775808]
rs2_val = [-2147483648, -1431655766, -1073741825, -536870913, -268435457, -134217729, -67108865, -33554433, -16777217, -8388609, -4194305, -2097153, -1048577, -524289, -262145, -131073, -65537, -32769, -16385, -8193, -4097, -2049, -1025, -513, -257, -129, -65, -33, -17, -9, -5, -3, -2, 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 1431655765, 2147483647]

def generate_macros(f, lmul, vsew):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    rs1lmul = (16 / vsew) * lmul
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
        if n == 24 or n == 16 or n == 8 or n % rs1lmul != 0 or n % lmul != 0 or (not (n + rs1lmul - 1 < 24 or n > 24 + lmul - 1)): # last condition is:(not( rs1 no overlap rd))
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
        if n == 24 or n == 16 or n == 8 or n % lmul != 0:
            continue
        if 16 + rs1lmul - 1 < n or 16 > n + lmul - 1:
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

def extract_operands(f, vsew):
    global rs1_val
    global rs2_val
    global val_64
    v = rs1_val + rs2_val
    if vsew == 64:
        v = v + val_64
        
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    vsew = float(os.environ['RVV_ATG_VSEW'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = len(v) / num_elem
    while loop_num == 0 and len(v) > 0:
        v = v * 2
        loop_num = len(v) / num_elem
    return v, v


def generate_tests(f, rs1_val, rs2_val, lmul, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    rs1lmul = (16 / vsew) * lmul
    n = 0
    
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s, "%(instr, instr_suffix) + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
        for i in range(min(32, loop_num)):     
            k = i%31+1
            if k != 8 and k != 16 and k != 24 and k % lmul == 0 and (16 + rs1lmul - 1 < k or 16 > k + lmul - 1) and k!= 12 and k != 20 and k != 24:
                n+=1
                print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
            
            k = i%30+2
            if k != 24 and k != 16 and k != 8 and k % rs1lmul == 0 and k % lmul == 0 and (k + rs1lmul - 1 < 24 or k > 24 + lmul - 1) and k!= 12 and k != 20 and k != 24:
                n +=1
                print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            n += 1
            print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
                instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[0]), file=f)
    vx_test_num = n - vv_test_num
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)

        for i in range(loop_num):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"rd_data_vi+%d, rs2_data+%d, 15)"%(i*step_bytes, i*step_bytes), file=f)
    vi_test_num = n - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)


def create_empty_test_vrgatherei16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, vsew)

    num_elem = int(vlen * lmul / vsew)
    # Add walking_val_grouped values, need at least num_elem
    for i in range(num_elem - len(rs2_val)):
        rs1_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))
        rs2_val.append(randint(-(2**(vsew-1)), 2**(vsew-1)-1))

    # Generate macros to test diffrent register
    generate_macros(f, lmul, vsew)

    # Generate tests
    num_tests_tuple = generate_tests(f, rs1_val, rs2_val, lmul, generate_vi = False, generate_vx = False)

    # Common const information
    print_common_ending_rs1rs2rd_vvvxvi(rs1_val, rs2_val, num_tests_tuple, vsew, f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
