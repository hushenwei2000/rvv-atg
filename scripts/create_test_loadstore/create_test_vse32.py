import logging
import os
from scripts.test_common_info import *
import re

instr = 'vse32'
instr1 = 'vle32'


def generate_macros(f):
    for n in range(1,30):
        print("#define TEST_VSE_OP_1%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x%d); "%n + "\\\n\
            load_inst v14, (x%d) ; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSE_OP_rd%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base;  \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x30;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v31, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSE_OP_130( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x30, base;  \\\n\
            li  x2, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x2; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x30); \\\n\
            load_inst v14, (x30) ;  \\\n\
        )",file=f)
    print("#define TEST_VSE_OP_131( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x31, base;  \\\n\
            li  x2, result; \\\n\
            vsetivli x30, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x2; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x31); \\\n\
            load_inst v14, (x31) ;  \\\n\
        )",file=f)
    print("#define TEST_VSE_OP_rd31( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v31, result, \\\n\
            la  x1, base;  \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v31, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v31, (x1); \\\n\
            load_inst v1, (x1);  \\\n\
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


def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("  TEST_VSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+" 8 "+", "+"0xff"+",  "+"0 + tdat"+" );", file=f)
        
    for i in range(100):     
        k = i%31+1
        n+=1
        print("  TEST_VSE_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0xaa"+",  "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VSE_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"8"+", "+"0x00"+",  "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vse32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print("  TEST_VSE_OP( 25, vle32.v, vse32.v, 32, 0xa00aa00a,  0   + tdat8 );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vse32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(instr))

    path = "%s/%s_first.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)

    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    generate_tests(f, rs1_val, rs2_val)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
