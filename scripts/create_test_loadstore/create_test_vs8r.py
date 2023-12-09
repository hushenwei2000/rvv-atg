import logging
import os
from scripts.test_common_info import *
import re

name = 'vs8r'
instr = 'vs8r'
instr1 = 'vl8re8'
instr2 = 'vl8re16'
instr3 = 'vl8re32'


def generate_macros(f, vsew, lmul):
    emul = 8 / vsew * lmul
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n == 12 or n == 20 or n == 24: # signature base registers
            continue
        print("#define TEST_VSRE2_OP_1%d(  testnum, load_inst, store_inst, eew, result1, result2, base )"%n + " \\\n\
        TEST_CASE_VLRE( testnum, eew, result1, result2, \\\n\
            la  x%d, base; "%n + " \\\n\
            li x29, MASK_EEW(result1, eew); \\\n\
            li x30, MASK_EEW(result2, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.x v8, x29; \\\n\
            vmv.v.x v9, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d); "%n + "\\\n\
            load_inst v16, (x%d); "%n + " \\\n\
        )",file=f)

    for n in range(1,32):
        if n%8 ==0 :
            print("#define TEST_VSRE2_OP_rd%d(  testnum, load_inst, store_inst, eew, result1, result2, base )"%n + " \\\n\
            TEST_CASE_VLRE( testnum, eew, result1, result2, \\\n\
                la  x1, base;  \\\n\
                li x7, MASK_EEW(result1, eew); \\\n\
                li x8, MASK_EEW(result2, eew); \\\n\
                vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
                vmv.v.x v%d, x7; "%n + "\\\n\
                vmv.v.x v%d, x8; "%(n+1) + "\\\n\
                VSET_VSEW \\\n\
                store_inst v%d, (x1); "%n + "\\\n\
                load_inst v16, (x1);  \\\n\
            )",file=f)



def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 8 / vsew * lmul
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(1):
        n += 1
        print("  TEST_VSRE2_OP( "+str(n)+",  %s.v, %s.v, "%(instr1,instr)+" 8 "+", "+"0xff"+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSRE2_OP( "+str(n)+",  %s.v, %s.v, "%(instr2,instr)+" 16 "+", "+"0xff00"+", "+"0xff00"+",  "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSRE2_OP( "+str(n)+",  %s.v, %s.v, "%(instr3,instr)+" 32 "+", "+"0xff0000ff"+", "+"0xff0000ff"+",  "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VSRE2_OP( "+str(n)+",  %s.v, %s.v, "%(instr3,instr)+" 32 "+", "+"0xff0000ff"+", "+"0xff0000ff"+",  "+"4096 + tdat"+" );", file=f)
        # n += 1
        # print("  TEST_VSRE2_OP( "+str(n)+",  %s.v, %s.v, "%(instr4,instr)+" 64 "+", "+"0x00ff000000ff0000"+",  "+"0 + tdat"+" );", file=f)
       
        

    for i in range(100):     
        k = i%30+1
        if k != 8 and k != 16 and k % lmul == 0 and k % 8 == 0 and k!= 12 and k != 20 and k !=24 and k != 29 and k != 30:
            n+=1
            print("  TEST_VSRE2_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr3,instr)+"32"+", "+"0xf00f00ff"+", "+"0xf00f00ff"+", "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if k == 31 or k == 30  or k == 12 or k == 20 or k == 24 or k == 29 or k == 30:
            continue;
        n +=1
        print("  TEST_VSRE2_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr3,instr)+"32"+", "+"0xf00fff00"+", "+"0xf00f00ff"+", "+"-8 + tdat4"+" );",file=f)
    return n

    


def create_empty_test_vs8r(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    generate_macros(f, vsew, lmul)


    # Common const information

    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vs8r(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f, vsew, lmul)

    # Generate tests
    n = generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information

    # Load const information
    print_load_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
