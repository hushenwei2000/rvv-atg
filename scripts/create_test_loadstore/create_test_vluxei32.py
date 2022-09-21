import logging
import os
from scripts.test_common_info import *
import re

instr = 'vluxei32'


def generate_macros(f):
    for n in range(2, 30):
        print("#define TEST_VLXEI_OP_1%d( testnum, inst, index_eew, result1, result2, base_data, base_index )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v14, __riscv_vsew, result1, result2, \\\n\
                la  x%d, base_data; "%n + "\\\n\
                la  x30, base_index; \\\n\
                vsetivli x31, 4, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v2, (x30); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v14, (x%d), v2; "%n + "\\\n\
                VSET_VSEW \\\n\
        )", file=f)
    for n in range(1, 31):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLXEI_OP_rd%d( testnum, inst, index_eew, result1, result2, base_data, base_index )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v%d, __riscv_vsew, result1, result2, "%n + "\\\n\
                la  x1, base_data; \\\n\
                la  x6, base_index; \\\n\
                vsetivli x31, 4, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v31, (x6); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v%d, (x1), v31; "%n + "\\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    print("#define TEST_VLXEI_OP_130( testnum, inst, index_eew, result1, result2, base_data, base_index ) \\\n\
            TEST_CASE_LOAD( testnum, v14, __riscv_vsew, result1, result2, \\\n\
                  la  x30, base_data; \\\n\
                  la  x6,  base_index; \\\n\
                  vsetivli x31, 4, MK_EEW(index_eew), tu, mu; \\\n\
                  MK_VLE_INST(index_eew) v2, (x6); \\\n\
                  VSET_VSEW_4AVL \\\n\
                  inst v14, (x30), v2; \\\n\
                  VSET_VSEW \\\n\
        )", file=f)
    print("#define TEST_VLXEI_OP_rd31( testnum, inst, index_eew, result1, result2, base_data, base_index ) \\\n\
            TEST_CASE_LOAD( testnum, v31, __riscv_vsew, result1, result2, \\\n\
                la  x1, base_data; \\\n\
                la  x2, base_index; \\\n\
                vsetivli x31, 4, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v2, (x2); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v31, (x1), v2; \\\n\
                VSET_VSEW \\\n\
        ) ", file=f)


def extract_operands(f, rpt_path):
    rs1_val = []
    rs2_val = []
    f = open(rpt_path)
    line = f.read()
    matchObj = re.compile('rs1_val ?== ?(-?\d+)')
    rs1_val_10 = matchObj.findall(line)
    rs1_val = ['{:#032x}'.format(int(x) & 0xffffffffffffffff)
               for x in rs1_val_10]
    matchObj = re.compile('rs2_val ?== ?(-?\d+)')
    rs2_val_10 = matchObj.findall(line)
    rs2_val = ['{:#032x}'.format(int(x) & 0xffffffffffffffff)
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
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, " %
              instr+" 32 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+", "+"0 + tdat"+", "+"idx32dat"+" );", file=f)
        n += 1
        print("  TEST_VLXEI_OP( "+str(n)+",  %s.v, " %
              instr+" 32 "+", "+"0xf00ff00f"+", "+"0x00ff00ff"+", "+"0 + tdat4"+", "+"idx32dat"+" );", file=f)
       

    for i in range(100):     
        k = i%31+1
        n+=1
        print("  TEST_VLXEI_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+"0x0ff00ff0"+", "+"0xf00ff00f"+" , "+"-4 + tdat4"+", "+"idx32dat"+" );",file=f)
        
        k = i%30+2
        if(k == 31):
            continue;
        n +=1
        print("  TEST_VLXEI_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+"0x00ff00ff"+", "+"0xff00ff00"+" , "+"0 + tdat"+", "+"idx32dat"+" );",file=f)
    


def create_empty_test_vluxei32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(instr))

    path = "%s/%s_empty.S" % (output_dir, instr)
    f = open(path, "w+")

    # Common header files
    print_common_header(instr, f)

    print(" TEST_VLXEI_OP( 2, vluxei32.v, 32, 0x00ff00ff, 0xff00ff00, 0  + tdat , idx32dat );", file=f)

    # Common const information
    #print_common_ending(f)
    # Load const information
    print_load_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(instr, path))

    return path


def create_first_test_vluxei32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
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
