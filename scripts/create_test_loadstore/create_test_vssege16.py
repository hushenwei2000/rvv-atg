import logging
import os
from scripts.test_common_info import *
import re

name = 'vssege16'

instr = 'vsseg2e16'
instr1 = 'vlseg2e16'
instr2 = 'vsseg3e16' 
instr2l = 'vlseg3e16'
instr3 = 'vsseg4e16' 
instr3l = 'vlseg4e16'
instr4 = 'vsseg5e16' 
instr4l = 'vlseg5e16'
instr5 = 'vsseg6e16' 
instr5l = 'vlseg6e16'
instr6 = 'vsseg7e16' 
instr6l = 'vlseg7e16'
instr7 = 'vsseg8e16' 
instr7l = 'vlseg8e16' 


def generate_macros(f):
    for n in range(1,30):
        print("#define TEST_VSSEG1_OP_1%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li x30, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x%d); "%n + "\\\n\
            load_inst v14, (x%d); "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSSEG1_OP_rd%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base;  \\\n\
            li x7, MASK_EEW(result, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x7;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v14, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSSEG1_OP_130( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x30, base;  \\\n\
            li x7, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v1, x7; \\\n\
            VSET_VSEW \\\n\
            store_inst v1, (x30); \\\n\
            load_inst v14, (x30);  \\\n\
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
        print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG1_OP( "+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+",  "+"2 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr2l,instr2)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr3l,instr3)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr4l,instr4)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr5l,instr5)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr6l,instr6)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        n += 1
        print("   TEST_VSSEG3_OP( "+str(n)+", %s.v, %s.v, "%(instr7l,instr7)+"16"+", "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0xa0a0"+",  "+"0 + tdat"+");", file=f)
        
        
    for i in range(100):     
        k = i%31+1
        if(k == 31):
            continue;
        n+=1
        print("  TEST_VSSEG1_OP_rd%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+",  "+"0 + tdat"+" );",file=f)
    
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("   TEST_VSSEG1_OP_1%d( "%k+str(n)+", %s.v, %s.v, "%(instr1,instr)+"16"+", "+"0xa0a0"+", "+"-8 + tdat8"+" );",file=f)



def create_empty_test_vssege16(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print("  TEST_VSSEG1_OP(11, vlseg2e16.v, vsseg2e16.v, 16, 0x00ff, 0  + tdat  ); ", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vssege16(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
