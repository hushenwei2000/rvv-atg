import logging
import os
from scripts.test_common_info import *
import re
import numpy as np

name = 'vlre32'
instr = 'vl1re32'
instr1 = 'vl2re32'
instr2 = 'vl4re32'
instr3 = 'vl8re32'


def generate_macros(f):
    for n in range(1, 32):
        if n == 12 or n == 20 or n == 24: # signature base registers
            continue
        print("#define TEST_VLRE1_OP_1%d( testnum, inst, eew, result, base )"%n + " \\\n\
            TEST_CASE( testnum, v16, result, \\\n\
                la  x%d, base; "%n + "\\\n\
                inst v16, (x%d); "%n + "\\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLRE1_OP_rd%d( testnum, inst, eew, result, base )"%n + " \\\n\
            TEST_CASE( testnum, v%d, result, "%n + "\\\n\
                la  x2, base; \\\n\
                inst v%d, (x2); "%n + "\\\n\
        ) ", file=f)

def generate_array(f, vl, vsew):
    base = 0
    sew = 32
    sewlen = sew//4
    vsewlen = vsew // 8
    a = np.array(
    ["0x00ff00ff", "0xff00ff00", "0x0ff00ff0", "0xf00ff00f", "0x00ff00ff", "0xff00ff00", "0x0ff00ff0", "0xf00ff00f" 
    ]
    )

    b = np.array(["0x00000000"])
    c = np.array(["0x00000000"])

    for n in range(7):
        c = np.concatenate((c,b))
    k = np.concatenate((a,c))

    m = np.concatenate((k,k,k))
    d = '0x' + m[base][-sewlen:]
    n = '0x' + m[ (vl//32)  + base ][-sewlen:]
    d1 = '0x' + m[base + 2][-sewlen:]
    n1 = '0x' + m[ (vl//32) + base + 2][-sewlen:]

    if vsew == 64 :
        fir_fill1 = '0x' + m[base + 1][-vsewlen:] + m[base][-vsewlen: ]
        fir_fill2 = '0x' + m[base + 2][-2:] + m[base + 1][-8:] + m[base][-8:-2]
        fir_fill3 = '0x' + m[base + 2][-4:] + m[base + 1][-8:] + m[base][-8:-4]
        fir_fill4 = '0x' + m[base + 2][-6:] + m[base + 1][-8:] + m[base][-8:-6]
    else :
            fir_fill1 = '0x' + m[base][-8:]
            fir_fill2 = '0x' + m[base + 1][-2:] + m[base][-8:-2]
            fir_fill3 = '0x' + m[base + 1][-4:] + m[base][-8:-4]
            fir_fill4 = '0x' + m[base + 1][-6:] + m[base][-8:-6]

    vfill = np.array([d,n,d1,n1])
    fir_fill = np.array([fir_fill1,fir_fill2,fir_fill3,fir_fill4])

    return vfill, fir_fill


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


def generate_tests(f, rs1_val, rs2_val, fill, fir_fill, vsew ,lmul):
    emul = 32 / vsew * lmul
    if emul < 0.125 or emul > 8:
        return
    emul = 1 if emul < 1 else int(emul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(2):
        n += 1
        print("  TEST_VLRE1_OP( "+str(n)+",  %s.v, " %instr+" 32 "+", "+fir_fill[0]+", "+"0 + tdat"+" );", file=f)
        n += 1
        print("  TEST_VLRE2_OP( "+str(n)+",  %s.v, " %instr1+" 32 "+", "+fill[0]+", "+fill[1]+", "+"-12 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLRE2_OP( "+str(n)+",  %s.v, " %instr2+" 32 "+", "+fill[0]+", "+fill[1]+",  "+"-12 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLRE2_OP( "+str(n)+",  %s.v, " %instr3+" 32 "+", "+fill[0]+", "+fill[1]+",  "+"-12 + tdat4"+" );", file=f)
        n += 1
        print("  TEST_VLRE2_OP( "+str(n)+",  %s.v, " %instr3+" 32 "+", "+fill[0]+", "+fill[1]+",  "+"4096 + tdat4"+" );", file=f)

    for i in range(100):     
        k = i%31+1
        n+=1
        if( k % lmul == 0 and k % emul == 0 and k % lmul == 0 and k != 31 and k != 12 and k != 20 and k != 24):
            print("  TEST_VLRE1_OP_rd%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+fir_fill[0]+", "+"0 + tdat"+" );",file=f)
        
        k = i%30+2
        if(k == 31 or k == 12 or k == 20 or k == 24):
            continue;
        n +=1
        print("  TEST_VLRE1_OP_1%d( "%k+str(n)+",  %s.v, "%instr+" 32 "+", "+fir_fill[0]+", "+"0 + tdat"+" );",file=f)
    return n


def create_empty_test_vlre32(xlen, vlen, vsew, lmul, vta, vma, output_dir):
    logging.info("Creating empty test for {}".format(name))

    path = "%s/%s_empty.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)


    # Common const information

    # Load const information
    print_loadlr_ending(f)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating empty test for {}: finish in {}!".format(name, path))

    return path


def create_first_test_vlre32(xlen, vlen, vsew, lmul, vta, vma, output_dir, rpt_path):
    logging.info("Creating first test for {}".format(name))

    path = "%s/%s_first.S" % (output_dir, name)
    f = open(path, "w+")

    # Common header files
    print_common_header(name, f)

    # Extract operands
    rs1_val, rs2_val = extract_operands(f, rpt_path)
    fill, fir_fill = generate_array(f, vlen, vsew)
    # Generate macros to test diffrent register
    generate_macros(f)

    # Generate tests
    n = generate_tests(f, rs1_val, rs2_val, fill, fir_fill, vsew, lmul)

    # Common const information

    # Load const information
    print_loadlr_ending(f, n)

    f.close()
    os.system("cp %s %s" % (path, output_dir))

    logging.info(
        "Creating first test for {}: finish in {}!".format(name, path))

    return path
