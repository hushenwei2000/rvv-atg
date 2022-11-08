import logging
import os
from scripts.test_common_info import *
import re

instr = 'vwmaccus'


def generate_macros(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vsew = int(os.environ['RVV_ATG_VSEW'])
    print("#undef TEST_W_VX_OP_RV \n\
#define TEST_W_VX_OP_RV( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_DOUBLE_VSEW_4AVL \\\n\
        vmv.v.i v24, 0; \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val1); \\\n\
        inst v24, x1, v8; \\\n\
    )", file=f)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_W_VX_OP_RV_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
                VSET_DOUBLE_VSEW_4AVL \\\n\
                vmv.v.i v24, 0; \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x%d, MASK_XLEN(val1); "%n + " \\\n\
                inst v24, x%d, v8; "%n + " \\\n\
        )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % (lmul*2) != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_W_VX_OP_RV_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE_LOOP_W( testnum, v%d, result, "%n + "\\\n\
            VSET_DOUBLE_VSEW_4AVL \\\n\
            vmv.v.i v24, 0; \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1);  \\\n\
            inst v%d, x1, v8; "%n + " \\\n\
        )",file=f)
   


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
        print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
              instr+"rd_data_vx+%d, %s, rs2_data+%d)"%(i*step_bytes_double, rs1_val[i], i*step_bytes), file=f)
    for i in range(min(32, loop_num)):
        k = i%31+1
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul*2) != 0:
            continue
        if k%2==0:
            n+=1
            print("  TEST_W_VX_OP_RV_rd%d( "%k+str(n)+",  %s.vx, "%instr+"rd_data_vx+%d, %s, rs2_data+%d)"%(i*step_bytes_double, rs1_val[i], i*step_bytes),file=f)
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_W_VX_OP_RV_1%d( "%k+str(n)+",  %s.vx, "%instr+"rd_data_vx+%d, %s, rs2_data+%d)"%(i*step_bytes_double, rs1_val[i], i*step_bytes),file=f)
    
    return n

def print_ending_vwmaccus(f, num_test, rs1_val, rs2_val):
    # test_num_tuple is vv_test_num, vx_test_num, wv_test_num, wx_test_num
    vsew = int(os.environ['RVV_ATG_VSEW'])
    vlen = int(os.environ['RVV_ATG_VLEN'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    num_elem = int(vlen * lmul / vsew)
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
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
    print(".align %d"%(int(vsew / 8)), file=f)
    print("rs1_data:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew)
        print("%s"%rs1_val[i], file=f)
    
    print(".align %d"%(int(vsew * 2 / 8)), file=f)
    print("rs1_data_widen:", file=f)
    for i in range(len(rs1_val)):
        print_data_width_prefix(f, vsew  * 2)
        print("%s"%rs1_val[i], file=f)
    
    print("\n.align %d"%(int(vsew  / 8)), file=f)
    print("rs2_data:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew )
        print("%s"%rs2_val[i], file=f)

    print(".align %d"%(int(vsew  * 2 / 8)), file=f)
    print("rs2_data_widen:", file=f)
    for i in range(len(rs2_val)):
        print_data_width_prefix(f, vsew  * 2)
        print("%s"%rs2_val[i], file=f)

    print("\n.align %d"%(int(vsew  / 8)), file=f)
    print("rd_data_vv:", file=f)
    print("\nrd_data_vx:", file=f)
    for i in range(num_test * num_elem):
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


def create_empty_test_vwmaccus(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VV_OP_NOUSE( 1, vadd.vv, 2, 1, 1 );", file=f)

    # Common const information
    print_common_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vwmaccus(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    num_test = generate_tests(f, rs1_val, rs2_val, lmul)

    # Common const information
    print_ending_vwmaccus(f, num_test, rs1_val, rs2_val)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
