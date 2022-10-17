import logging
import os
from scripts.test_common_info import *
import re

instr = 'vsse16'
instr1 = 'vlse16'


def generate_macros(f):
    for n in range(1,29):
        print("#define TEST_VSSE_OP_1%d( testnum, load_inst, store_inst, eew, result, stride, base )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x29, stride;  \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x%d), x29; "%n + "\\\n\
            load_inst v14, (x%d), x29 ; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSSE_OP_rd%d( testnum, load_inst, store_inst, eew, result, stride, base )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x3;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1), x2; "%n + " \\\n\
            load_inst v31, (x1), x2; \\\n\
        )",file=f)

    print("#define TEST_VSSE_OP_130( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x30, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x30), x2; \\\n\
            load_inst v14, (x30), x2 ;  \\\n\
        )",file=f)
    print("#define TEST_VSSE_OP_129( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x29, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x29), x2; \\\n\
            load_inst v14, (x29), x2 ;  \\\n\
        )",file=f)
    print("#define TEST_VSSE_OP_rd31( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v31, result, \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v31, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v31, (x1), x2; \\\n\
            load_inst v1, (x1), x2;  \\\n\
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


def generate_tests(f, rs1_val, rs2_val, vsew, lmul):
    emul = 16 / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+", "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"2"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"2"+", "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"4100"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSE_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"-4100"+", "+"0 + tdat15"+");", file=f)
   
    for i in range(100):     
        k = i%31+1
        if k % emul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul):
            n+=1
            print("  TEST_VSSE_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+", "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if k % emul == 0 and k not in [31, 8, 16] and not is_overlap(k, lmul, 8, emul):
            n +=1
            print("  TEST_VSSE_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"0"+", "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vsse16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print(" TEST_VSSE_OP( 10, vlse16.v, vsse16.v, 16, 0x00aa, 2, 0  + tdat ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vsse16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
    generate_tests(f, rs1_val, rs2_val, vsew, lmul)

    # Common const information
    # print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(instr, path))

    return path
