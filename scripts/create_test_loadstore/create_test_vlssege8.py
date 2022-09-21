import logging
import os
from scripts.test_common_info import *
import re

name = 'vlssege8'

instr = 'vlsseg2e8'
instr1 = 'vlsseg3e8'
instr2 = 'vlsseg4e8'
instr3 = 'vlsseg5e8'
instr4 = 'vlsseg6e8'
instr5 = 'vlsseg7e8'
instr6 = 'vlsseg8e8'


def generate_macros(f):
    for n in range(1, 30):
        print("#define TEST_VLSSEG1_OP_1%d(  testnum, inst, eew, result, stride, base )"%n + " \\\n\
            TEST_CASE( testnum, v16, result, \\\n\
                la  x%d, base; "%n + "\\\n\
                li  x30, stride; \\\n\
                inst v16, (x%d), x30 ; "%n + "\\\n\
        )", file=f)
    for n in range(1, 31):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLSSEG1_OP_rd%d(  testnum, inst, eew, result, stride, base )"%n + " \\\n\
            TEST_CASE( testnum, v%d, result, "%n + "\\\n\
                la  x1, base; \\\n\
                li  x2, stride; \\\n\
                inst v%d, (x1), x2; "%n + "\\\n\
        ) ", file=f)
    print("#define TEST_VLSSEG1_OP_130(  testnum, inst, eew, result, stride, base ) \\\n\
            TEST_CASE( testnum, v16, result, \\\n\
                la  x30, base; \\\n\
                li  x3, stride; \\\n\
                inst v16, (x30), x3 ; \\\n\
        )", file=f)



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
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"0"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"2"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"3"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"0"+", "+"1 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"1"+", "+"1 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"2"+", "+"1 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"3"+", "+"1 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"0"+", "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"1"+", "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"2"+", "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0xff"+", "+"3"+", "+"2 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"0"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"1"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"2"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"3"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"4100"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG1_OP( "+str(n)+",  %s.v, " %instr+" 8 "+", "+"0x00"+", "+"-4100"+", "+"3 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr1+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr2+" 8 "+", "+"0x0f"+", "+"0xf0"+", "+"0x0f"+", "+"1"+", "+"12 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr3+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"1"+", "+"-12 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr4+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr5+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLSSEG3_OP( "+str(n)+",  %s.v, " %instr6+" 8 "+", "+"0xff"+", "+"0x00"+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );", file=f)
        

    for i in range(100):     
        k = i%31+1
        if(k == 31):
            continue;
        n+=1
        print("  TEST_VLSSEG1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0xff"+", "+"1"+", "+"0 + tdat"+" );",file=f)
        
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VLSSEG1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 8 "+", "+"0x00"+", "+"1"+", "+"4 + tdat"+" );",file=f)
    


def create_empty_test_vlssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    print(" TEST_VLSSEG1_OP( 3, vlsseg2e8.v, 8, 0xff, 1,  0  + tdat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlssege8(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
