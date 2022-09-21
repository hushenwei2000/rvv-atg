import logging
import os
from scripts.test_common_info import *
import re

name = 'vluxsegei8'

instr  = 'vluxseg2ei8'
instr1 = 'vluxseg3ei8'
instr2 = 'vluxseg4ei8'
instr3 = 'vluxseg5ei8'
instr4 = 'vluxseg6ei8'
instr5 = 'vluxseg7ei8'
instr6 = 'vluxseg8ei8'


def generate_macros(f):
    for n in range(1,31):
        print("#define TEST_VLXSEG1_OP_1%d( testnum, inst, index_eew, result, base_data, base_index  )"%n + " \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x31, base_index; \\\n\
            MK_VLE_INST(index_eew) v2, (x31);    \\\n\
            inst v14, (x%d), v2 ; "%n + " \\\n\
        )",file=f)

    for n in range(1,30):
        print("#define TEST_VLXSEG1_OP_rd%d( testnum, inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v31, (x6);    \\\n\
            inst v%d, (x1), v31; "%n + " \\\n\
        )",file=f)

    print("#define TEST_VLXSEG1_OP_131( testnum, inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v14, result, \\\n\
            la  x31, base_data; \\\n\
            la  x2, base_index; \\\n\
            MK_VLE_INST(index_eew) v2, (x2);    \\\n\
            inst v14, (x31), v2 ;  \\\n\
        )",file=f)
    print("#define TEST_VLXSEG1_OP_rd30( testnum, inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v30, result, \\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v2, (x6);    \\\n\
            inst v30, (x1), v2 ;  \\\n\
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
        print("  TEST_VLXSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00ff00ff"+", "+"0 + tdat"+" , "+"idx8dat"+");", file=f)
        n += 1
        print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 8 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0x0ff00ff0"+", "+"0 + tdat"+", "+"idx8dat"+" );", file=f)
        n += 1
        print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr2+" 8 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"12 + tdat"+", "+"idx8dat"+" );", file=f)
        n += 1
        print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr3+" 8 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0x0ff00ff0"+","+"-12 + tdat4"+", "+"idx8dat"+" );", file=f)
        n += 1
        print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr4+" 8 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
        n += 1
        print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr5+" 8 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
        n += 1
        print("  TEST_VLXSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0 + tdat4"+", "+"idx8dat"+" );", file=f)
        

    for i in range(100):     
        k = i%31+1
        if(k == 31):
            continue;
        n+=1
        print("   TEST_VLXSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+"8"+", "+"0x00ff00ff"+", "+"0 + tdat"+", "+"idx8dat"+");",file=f)
        
        k = i%30+2
        # if(k == 31):
        #     continue;
        n +=1
        print("  TEST_VLXSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+"8"+", "+"0x00ff00ff"+", "+"0 + tdat"+", "+"idx8dat"+" );",file=f)
    


def create_empty_test_vluxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print(" TEST_VLXSEG1_OP( 3, vluxseg2ei8.v, 8, 0x00ff00ff, 0  + tdat, idx8dat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vluxsegei8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
