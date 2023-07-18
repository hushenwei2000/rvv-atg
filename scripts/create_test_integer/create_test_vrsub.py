import logging
import os
from scripts.test_common_info import *
import re

instr = 'vrsub'


def generate_macros(f, vsew):
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#define TEST_VX_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v16, v8, x1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#define TEST_VI_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v8, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(2, 32):
        print("#define TEST_VX_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v16, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x%d, MASK_XLEN(val1); "%n + "\\\n\
                inst v16, v8, x%d%s; "%(n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VX_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, result,"%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew , n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x1, MASK_XLEN(val1); \\\n\
                inst v%d, v8, x1%s; "%(n, ", v0.t" if masked else "") + " \\\n\
        ) ", file=f)



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


def generate_tests(f, rs1_val, rs2_val, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    lmul_double_1 = 1 if (lmul * 2) < 1 else int(lmul * 2)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
              instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[i]), file=f)
    for i in range(min(32, loop_num)):     
        k = i%31+1 
        if k%lmul == 0 and k != 8 and k != 16 and k != 24  and k != 12 and k != 20 and k != 24:
            n+=1
            print("  TEST_VX_OP_rd%d( "%k+str(n)+",  %s.vx, "%instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[i]),file=f)
        k = i%30+2
        if k != 12 and k != 20 and k != 24:
            n +=1
    #     print("  TEST_VX_OP_1%d( "%k+str(n)+",  %s.vx, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
    #     print("  #-------------------------------------------------------------", file=f)
    
    # if vsew == 8:
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 101, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 10, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 12, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -86);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 101);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 10);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 12);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -86, 3);", file=f)
    # elif vsew == 16:
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 26213, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 180, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 182, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -21846);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 26213);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 180);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 182);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -21846, 3);", file=f)
    # elif vsew == 32:
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 1717986917, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 46339, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 46341, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -1431655766);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 1717986917);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 46339);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 46341);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -1431655766, 3);", file=f)
    # elif vsew == 64:
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3037000498, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3037000500, 3);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 7378697629483820645);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 3037000498);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, 3, 3037000500);", file=f)
    #     n += 1
    #     print("  TEST_VX_OP( "+str(n)+",  %s.vx"%instr + ", 5201314, -6148914691236517206, 3);", file=f)

    
            print("  TEST_VX_OP_1%d( "%k+str(n)+",  %s.vx, "%instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[i]),file=f)
    vx_test_num = n

    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
              instr+"rd_data_vi+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, 15), file=f)
    vi_test_num = n - vx_test_num

    return (0, vx_test_num, vi_test_num)
    

def create_empty_test_vrsub(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vrsub(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, vsew)

    # Generate tests
    vv_num_tests = generate_tests(f, rs1_val, rs2_val, lmul)

    # Common const information
    print_common_ending_rs1rs2rd_vvvxvi(rs1_val, rs2_val, vv_num_tests, vsew, f, generate_vv=False)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
