import re
def generate_macros(f, lmul):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    for n in range(1, 32):
        if n % lmul == 0 and n != 24 and n != 8 and n != 16:
            print("#define TEST_AVG_VV_OP_1_%d( testnum, inst, result00, result01, result10, result11, val2, val1 ) "%n + " \\\n\
            TEST_CASE_AVG_VV( testnum, inst, v%d, v24, result00, result01, result10, result11, "%n + " \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v%d, x7;"%n + " \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v8, x7; \\\n\
            )", file=f)
    for n in range(1, 32):
        if n % (lmul * 2) == 0 and n != 24 and n != 8 and n != 16:
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            print("#define TEST_AVG_VV_OP_rd%d( testnum, inst, result00, result01, result10, result11, val2, val1 ) "%n + " \\\n\
            TEST_CASE_AVG_VV( testnum, inst, v16, v%d, result00, result01, result10, result11, "%n + " \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v16, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v8, x7; \\\n\
            ) ", file=f)

def generate_macros_vnclip(f, lmul):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    for n in range(1, 32):
        if n % lmul == 0 and n != 24 and n != 8 and n != 16:
            print("#define TEST_W_AVG_WV_OP_1%d( testnum, inst, result00, result01, result10, result11, val2, val1 ) "%n + " \\\n\
            TEST_CASE_AVG_VV( testnum, inst, v%d, v24, result00, result01, result10, result11, "%n + " \\\n\
                li x7, MASK_DOUBLE_VSEW(val2); \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v%d, x7;"%n + " \\\n\
                VSET_VSEW  \\\n\
                li x7, val1; \\\n\
                vmv.v.x v8, x7; \\\n\
            )", file=f)
    for n in range(1, 32):
        if n % (lmul * 2) == 0 and n != 24 and n != 8 and n != 16:
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            print("#define TEST_W_AVG_WV_OP_rd%d( testnum, inst, result00, result01, result10, result11, val2, val1 ) "%n + " \\\n\
                TEST_CASE_AVG_VV( testnum, inst, v16, v%d, result00, result01, result10, result11, "%n + " \\\n\
                    li x7, MASK_DOUBLE_VSEW(val2); \\\n\
                    VSET_DOUBLE_VSEW \\\n\
                    vmv.v.x v16, x7; \\\n\
                    VSET_VSEW  \\\n\
                    li x7, val1; \\\n\
                    vmv.v.x v8, x7; \\\n\
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

def generate_tests(f, rs1_val, rs2_val, instr, lmul, generate_vi = False):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_AVG_VV_OP( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k % (lmul * 2) == 0 and k != 24 and k != 8 and k != 16:
            n+=1
            print("  TEST_AVG_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k % lmul == 0 and k != 24 and k != 8 and k != 16:
            n +=1
            print("  TEST_AVG_VV_OP_1_%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_AVG_VX_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_AVG_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+" 4 "+" );", file=f)

def generate_tests_vnclip(f, rs1_val, rs2_val, instr, lmul):
    n = 1
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    print("  #-------------------------------------------------------------", file=f)
    print("  # WV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_AVG_WV_OP( "+str(n)+",  %s.wv, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k % (lmul * 2) == 0 and k != 24 and k != 8 and k != 16:
            n+=1
            print("  TEST_W_AVG_WV_OP_rd%d( "%k+str(n)+",  %s.wv, "%instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k % lmul == 0 and k != 24 and k != 8 and k != 16:
            n +=1
            print("  TEST_W_AVG_WV_OP_1%d( "%k+str(n)+",  %s.wv, "%instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # WX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_AVG_WX_OP( "+str(n)+",  %s.wx, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # WI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_AVG_WI_OP( "+str(n)+",  %s.wi, " %
              instr+"5201314"+", "+"5201314"+", "+"5201314"+", "+"5201314"+", "+rs2_val[i]+", "+" 4 "+" );", file=f)
  