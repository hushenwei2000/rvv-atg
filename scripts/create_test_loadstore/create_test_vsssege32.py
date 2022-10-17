import logging
import os
from scripts.test_common_info import *
import re

name = 'vsssege32'

instr = 'vssseg2e32'
instr1 = 'vlsseg2e32'
instr2 = 'vssseg3e32' 
instr2l = 'vlsseg3e32'
instr3 = 'vssseg4e32' 
instr3l = 'vlsseg4e32'
instr4 = 'vssseg5e32' 
instr4l = 'vlsseg5e32'
instr5 = 'vssseg6e32' 
instr5l = 'vlsseg6e32'
instr6 = 'vssseg7e32' 
instr6l = 'vlsseg7e32'
instr7 = 'vssseg8e32' 
instr7l = 'vlsseg8e32' 


def generate_macros(f):
    for n in range(1,29):
        print("#define TEST_VSSSEG1_OP_1%d( testnum, load_inst, store_inst, eew, result, stride, base  )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x29, stride; \\\n\
            li  x30, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x%d), x29; "%n + "\\\n\
            load_inst v14, (x%d), x29; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSSSEG1_OP_rd%d( testnum, load_inst, store_inst, eew, result, stride, base  )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x7, MASK_EEW(result, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x7;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1), x2; "%n + " \\\n\
            load_inst v14, (x1), x2; \\\n\
        )",file=f)

    print("#define TEST_VSSSEG1_OP_130( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x30, base;  \\\n\
            li  x2, stride; \\\n\
            li  x7, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x7; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x30), x2; \\\n\
            load_inst v14, (x30), x2;  \\\n\
        )",file=f)
    print("#define TEST_VSSSEG1_OP_129( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x29, base;  \\\n\
            li  x2, stride; \\\n\
            li  x7, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x7; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x29), x2; \\\n\
            load_inst v14, (x29), x2;  \\\n\
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
        print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"4100"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"-4100"+", "+"0 + tdat15"+");", file=f)
        n += 1
        print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"0"+", "+"4 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"4"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"4"+", "+"4 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"32"+", "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+",  "+"0xa0a0a0a0"+", "+"0"+", "+"0 + tdat"+");", file=f)
        
        
    for i in range(100):     
        k = i%31+1
        if(k == 31):
            continue;
        n+=1
        print("   TEST_VSSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"0"+",  "+"0 + tdat"+");",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("    TEST_VSSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"32"+", "+"0xa0a0a0a0"+", "+"32"+",  "+"0 + tdat"+");",file=f)



def create_empty_test_vsssege32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print("  TEST_VSSSEG1_OP(11, vlsseg2e16.v, vssseg2e16.v, 16, 0x0ff0, 2,  8  + tdat  ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vsssege32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

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
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
