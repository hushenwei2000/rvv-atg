import logging
import os
from scripts.test_common_info import *
import re

name = 'vlsege8'

instr = 'vlseg2e8'
instr1 = 'vlseg3e8'
instr2 = 'vlseg4e8'
instr3 = 'vlseg5e8'
instr4 = 'vlseg6e8'
instr5 = 'vlseg7e8'
instr6 = 'vlseg8e8'


def generate_macros(f):
    for n in range(1, 32):
        print("#define TEST_VLSEG1_OP_1%d( testnum, inst, eew, result, base )"%n + " \\\n\
            TEST_CASE( testnum, v16, result, \\\n\
                la  x%d, base; "%n + "\\\n\
                inst v16, (x%d); "%n + "\\\n\
        )", file=f)
    for n in range(1, 31):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLSEG1_OP_rd%d( testnum, inst, eew, result, base )"%n + " \\\n\
            TEST_CASE( testnum, v%d, result, "%n + "\\\n\
                la  x2, base; \\\n\
                inst v%d, (x2); "%n + "\\\n\
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


def generate_tests(f, rs1_val, rs2_val):
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(2):
        n += 1
        print("  TEST_VLSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"1 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr2+" 8 "+", "+"0x0f"+", "+"0xf0"+", "+"0x0f"+", "+"12 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr3+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"-12 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr4+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr5+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"0 + tdat"+" );", file=f)
        

    for i in range(100):     
        k = i%31+1
        if(k == 31):
            continue;
        n+=1
        print("  TEST_VLSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0xff"+", "+"0 + tdat"+" );",file=f)
        
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VLSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0x00"+", "+"4 + tdat"+" );",file=f)
    


def create_empty_test_vlsege8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print(" TEST_VLSEG1_OP( 3, vlseg2e8.v, 8, 0xff, 0  + tdat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlsege8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
