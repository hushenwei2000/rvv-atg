import logging
import os
from scripts.test_common_info import *
from scripts.create_test_floating.create_test_common import *

instr = 'vfwredsum'
rs1_val = ["0x00000000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0xBF800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0x3F800000", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0xFF7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x7F7FFFFF", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x80855555", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x00800001", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x80800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000", "0x00800000",
           "0x00800000", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x807FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x007FFFFF", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x807FFFFE", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x00000002", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x80000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x00000001", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x80000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", "0x00000000", ]
rs2_val = ["0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000",
           "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", "0x00000000", "0xBF800000", "0x3F800000", "0xFF7FFFFF", "0x7F7FFFFF", "0x80855555", "0x00800001", "0x80800000", "0x00800000", "0x807FFFFF", "0x007FFFFF", "0x807FFFFE", "0x00000002", "0x80000001", "0x00000001", "0x80000000", ]


def generate_macros(f, lmul):
    # lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n % lmul != 0: continue
        rs2, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_WV_OP_DS_1%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_WVWF_FP( testnum, v%d, flags, val1, val2, \\\n\
            fld f0, 0(a0); \\\n\
            flw f1, 8(a0); \\\n\
            flw f4, 8(a0); \\\n\
            VSET_DOUBLE_VSEW \\\n\
            vfmv.s.f v%d, f0; \\\n\
            VSET_VSEW \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f4, f4; \\\n\
            finst f2, f0, f4; \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, rd, n, rs2, rd, rs2, n),file=f)
    for n in range(1,32):
        if n % (2*lmul) != 0: continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_WV_OP_DS_rd%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_WVWF_FP( testnum, v%d, flags, val1, val2, \\\n\
            fld f0, 0(a0); \\\n\
            flw f1, 8(a0); \\\n\
            flw f4, 8(a0); \\\n\
            VSET_DOUBLE_VSEW \\\n\
            vfmv.s.f v%d, f0; \\\n\
            VSET_VSEW \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f4, f4; \\\n\
            finst f2, f0, f4; \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, n, rs1, rs2, n, rs2, rs1),file=f)


def generate_tests(f, lmul):
    n = 1
    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwredosum Tests",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_FP_WV_OP_DS( "+str(n)+",  vfwredosum.vs, fadd.d, 0xff100, "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    # print("  #-------------------------------------------------------------",file=f)
    # print("  # vfwredusum Tests",file=f)
    # print("  # Raise opcode `vfwredusum.vs v14,v2,v1'",file=f)
    # print("  #-------------------------------------------------------------",file=f)
    # 
    # for i in range(len(rs1_val)):
    #     n += 1
    #     print("  #TEST_W_FP_WV_OP_DS( "+str(n)+",  vfwredusum.vs, fadd.d, 0xff100, "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

    print("  #-------------------------------------------------------------",file=f)
    print("  # vfwredosum Tests (different register)",file=f)
    print("  #-------------------------------------------------------------",file=f)
    
    for i in range(len(rs1_val)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 12 or k == 20 or k == 24: continue
        n += 1
        print("  TEST_W_FP_WV_OP_DS_1%d( "%k+str(n)+",  vfwredosum.vs, fadd.d, 0xff100, "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)

        if k % (2*lmul) != 0 or k == 12 or k == 20 or k == 24: continue
        n += 1
        print("  TEST_W_FP_WV_OP_DS_rd%d( "%k+str(n)+",  vfwredosum.vs, fadd.d, 0xff100, "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
        
    return n


def create_empty_test_vfwredsum(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)


    # Common const information
    print_ending(f, generate_data=False)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vfwredsum(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Generate macros to test diffrent register
    generate_macros(f, lmul)

    # Generate tests
    n = generate_tests(f, lmul)

    # Common const information
    print_ending(f, test_tuples=(0,n,0))

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
