import re

def generate_macros_vw(f, lmul):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    for n in range(2, 32):
        if n != 1 and n != 2 and n != 14:
            print("#define TEST_W_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_W( testnum, v14, result, \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v1, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v%d, x7;"%n + " \\\n\
                inst v14, v1, v%d;"%n+" \\\n\
            )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 1 and n != 2 and n != 14:
            print("#define TEST_W_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_W( testnum, v%d, result, "%n + "\\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v1, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v2, x7; \\\n\
                inst v%d, v1, v2;"%n+" \\\n\
            )",file=f)

def generate_macros_vwmacc(f, lmul):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    for n in range(2, 32):
        if n != 1 and n != 2 and n != 14:
            print("#define TEST_W_VV_OP_WITH_INIT_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
                TEST_CASE_W( testnum, v14, result,  \\\n\
                li x7, 0; \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v14, x7; \\\n\
                VSET_VSEW \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v1, x7; \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v%d, x7; "%n + " \\\n\
                inst v14, v1, v%d; "%n + " \\\n\
                )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 1 and n != 2 and n != 14:
            print("#define TEST_W_VV_OP_WITH_INIT_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
                TEST_CASE_W( testnum, v%d, result, "%n + "\\\n\
                li x7, 0; \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v14, x7; \\\n\
                VSET_VSEW \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v1, x7; \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v2, x7;  \\\n\
                inst v%d, v1, v2; "%n + " \\\n\
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

def generate_tests_vw(f, rs1_val, rs2_val, instr, lmul, generate_wvwx = True):
    n = 1
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k%(2*lmul)==0 and k != 1 and k != 2 and k != 14:
            n+=1
            print("  TEST_W_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k != 1 and k != 2 and k != 14:
            n +=1
            print("  TEST_W_VV_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_VX_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    if generate_wvwx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # WV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_W_WV_OP( "+str(n)+",  %s.wv, " %
                instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  # WX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_W_WX_OP( "+str(n)+",  %s.wx, " %
                instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
              
def generate_tests_vwmacc(f, rs1_val, rs2_val, instr, lmul):
    n = 1
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k%(2*lmul)==0 and k != 1 and k != 2 and k != 14:
            n+=1
            print("  TEST_W_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k != 1 and k != 2 and k != 14:
            n +=1
            print("  TEST_W_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
