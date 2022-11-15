import re

def generate_macros_vv(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE( testnum, v24, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"% n + " \\\n\
            inst v24, v16, v%d; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result,"%n + " \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            inst v%d, v16, v8;"%n+" \\\n\
        ) ", file=f)
    print("#define TEST_VV_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v8, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v24, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v16, x7; \\\n\
            inst v8, v24, v16; \\\n\
        )", file=f)
    print("#define TEST_VV_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v16, v8, v24; \\\n\
        )", file=f)


def generate_macros_vw(f, lmul):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    for n in range(2, 32):
        if n != 8 and n != 16 and n != 24 and n % lmul == 0 :
            print("#define TEST_W_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_W( testnum, v24, result, \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v%d, x7;"%n + " \\\n\
                inst v24, v8, v%d;"%n+" \\\n\
            )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 8 and n != 16 and n != 24:
            print("#define TEST_W_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_W( testnum, v%d, result, "%n + "\\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v16, x7; \\\n\
                inst v%d, v8, v16;"%n+" \\\n\
            )",file=f)

def generate_macros_vwmacc(f, lmul):
    if lmul < 1:
        lmul = 1
    else:
        lmul = int(lmul)
    for n in range(2, 32):
        if n != 8 and n != 16 and n != 24 and n % lmul == 0:
            print("#define TEST_W_VV_OP_WITH_INIT_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
                TEST_CASE_W( testnum, v24, result,  \\\n\
                li x7, 0; \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v24, x7; \\\n\
                VSET_VSEW \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v%d, x7; "%n + " \\\n\
                inst v24, v8, v%d; "%n + " \\\n\
                )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 8 and n != 16 and n != 24:
            print("#define TEST_W_VV_OP_WITH_INIT_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
                TEST_CASE_W( testnum, v%d, result, "%n + "\\\n\
                li x7, 0; \\\n\
                VSET_DOUBLE_VSEW \\\n\
                vmv.v.x v%d, x7; "%n + "\\\n\
                VSET_VSEW \\\n\
                li x7, MASK_VSEW(val1); \\\n\
                vmv.v.x v8, x7; \\\n\
                li x7, MASK_VSEW(val2); \\\n\
                vmv.v.x v16, x7;  \\\n\
                inst v%d, v8, v16; "%n + " \\\n\
                )",file=f)

def generate_macros_muladd(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VV_OP_WITH_INIT_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE( testnum, v24, result,  \\\n\
            li x7, 0; \\\n\
            vmv.v.x v24, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7; "%n + " \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            inst v24, v%d, v16; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VV_OP_WITH_INIT_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            li x7, 0; \\\n\
            vmv.v.x v%d, x7; "%n + "\\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7;  \\\n\
            inst v%d, v8, v16; "%n + " \\\n\
        ) ", file=f)
    print("#define TEST_VV_OP_WITH_INIT_rd8( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v8, result, \\\n\
            li x7, 0; \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v8, v16, v24; \\\n\
        )", file=f)
    print("#define TEST_VV_OP_WITH_INIT_rd16( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            li x7, 0; \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v16, v8, v24; \\\n\
        )", file=f)

def generate_macros_vvm(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VVM_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_MASK( testnum, v24, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"%n + " \\\n\
            inst v24, v8, v%d; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % (lmul * 2) != 0:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VVM_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
        TEST_CASE_MASK( testnum, v%d, result, "%n + "\\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v16, x7; \\\n\
            inst v%d, v8, v16; "%n + " \\\n\
        ) ", file=f)
    print("#define TEST_VVM_OP_rd8( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_MASK( testnum, v8, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v24, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v16, x7; \\\n\
            inst v8, v24, v16; \\\n\
        )", file=f)
    print("#define TEST_VVM_OP_rd16( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_MASK( testnum, v16, result, \\\n\
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v24, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            inst v16, v24, v8; \\\n\
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

def generate_tests_vvvxvi(instr, f, rs1_val, rs2_val, lmul, vsew, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s, " %
                (instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
        for i in range(100):     
            k = i%31+1
            if k % lmul != 0 or k == 24:
                continue
            n+=1
            print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
            
            k = i%30+2
            if k % lmul != 0 or k == 8 or k == 16 or k == 24:
                continue
            n +=1
            print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
        
        if vsew == 8:
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 101, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 10, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 12, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -86);", file=f)
        elif vsew == 16:
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 26213, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 180, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 182, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -21846);", file=f)
        elif vsew == 32:
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 1717986917, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46339, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46341, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -1431655766);", file=f)
        elif vsew == 64:
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 7378697629483820645, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000498, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000500, 3);", file=f)
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -6148914691236517206);", file=f)


    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
                instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314"+", "+rs1_val[i]+", "+" 4 "+" );", file=f)

def generate_tests_vw(f, rs1_val, rs2_val, instr, lmul, vsew, generate_wvwx = True):
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
        if k%(2*lmul)==0 and k != 8 and k != 16 and k != 24:
            n+=1
            print("  TEST_W_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k % lmul == 0 and k != 16 and k != 8 and k != 24:
            n +=1
            print("  TEST_W_VV_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    
    if vsew == 8:
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
    elif vsew == 16:
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
    elif vsew == 32:
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
    elif vsew == 64:
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)

    
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
              
def generate_tests_vwmacc(f, rs1_val, rs2_val, instr, lmul, vsew, instr_suffix='vv', generate_vxrv=True):
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
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s, " %
              (instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k%(2*lmul)==0 and k != 8 and k != 16 and k != 24:
            n+=1
            print("  TEST_W_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k % lmul == 0 and k != 8 and k != 16 and k != 24:
            n +=1
            print("  TEST_W_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    
    if vsew == 8:
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 101, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 10, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 12, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -86);", file=f)
    elif vsew == 16:
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 26213, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 180, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 182, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -21846);", file=f)
    elif vsew == 32:
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 1717986917, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46339, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46341, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -1431655766);", file=f)
    elif vsew == 64:
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 7378697629483820645, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000498, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000500, 3);", file=f)
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -6148914691236517206);", file=f)

    
    if generate_vxrv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
                instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)

def generate_tests_muladd(instr, f, rs1_val, rs2_val, lmul, vsew):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k == 24 or k % lmul != 0:
            continue
        n+=1
        print("  TEST_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
        
        k = i%30+2
        if k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs1_val[i]+" , "+rs2_val[i]+");",file=f)
    
    if vsew == 8:
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 101);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 10);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 12);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -86, 3);", file=f)
    elif vsew == 16:
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 26213);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 180);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 182);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -21846, 3);", file=f)
    elif vsew == 32:
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 1717986917);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46339);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46341);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -1431655766, 3);", file=f)
    elif vsew == 64:
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 7378697629483820645);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000498);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000500);", file=f)
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -6148914691236517206, 3);", file=f)

    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VX_OP_RV( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)    
  
def generate_tests_vmadc(instr, f, rs1_val, rs2_val, lmul, vsew, generate_vi = True):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0:
            continue
        n+=1
        print("  TEST_VVM_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+");",file=f)
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    
    if vsew == 8:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
    elif vsew == 16:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
    elif vsew == 32:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
    elif vsew == 64:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)


    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+"0x00000000"+", "+"0x00000000"+" );", file=f)
        n +=1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+"0x00000000"+", "+"0x00000011"+" );", file=f)
        n +=1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+"0xffffffff"+", "+"0x00000001"+" );", file=f)
        n +=1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+"0xffffffff"+", "+"0xffffffff"+" );", file=f)
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(len(rs1_val)):
            n +=1
            print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314"+", "+"0xffffffee"+", "+"0x1"+" );", file=f)
            n +=1
            print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314"+", "+"0xfffff000"+", "+"0x0"+" );", file=f)
            n +=1
            print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314"+", "+"0xffffeee0"+", "+"0xe"+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VVM Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n +=1
        print("  TEST_ADC_VVM_OP( "+str(n)+",  %s.vvm, " %
              instr+"5201314"+", "+"0xffffffee"+", "+"0x00000001"+" );", file=f)
        n +=1
        print("  TEST_ADC_VVM_OP( "+str(n)+",  %s.vvm, " %
              instr+"5201314"+", "+"0xfffff000"+", "+"0x00000001"+" );", file=f)
        n +=1
        print("  TEST_ADC_VVM_OP( "+str(n)+",  %s.vvm, " %
              instr+"5201314"+", "+"0xffffeee0"+", "+"0xffffffff"+" );", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VXM Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n +=1
        print("  TEST_ADC_VXM_OP( "+str(n)+",  %s.vxm, " %
              instr+"5201314"+", "+"0xffffffee"+", "+"0x00000001"+" );", file=f)
        n +=1
        print("  TEST_ADC_VXM_OP( "+str(n)+",  %s.vxm, " %
              instr+"5201314"+", "+"0xfffff000"+", "+"0x00000001"+" );", file=f)
        n +=1
        print("  TEST_ADC_VXM_OP( "+str(n)+",  %s.vxm, " %
              instr+"5201314"+", "+"0xffffeee0"+", "+"0xffffffff"+" );", file=f)
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VIM Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(len(rs1_val)):
            n +=1
            print("  TEST_ADC_VIM_OP( "+str(n)+",  %s.vim, " %
                instr+"5201314"+", "+"0xffffffee"+", "+"0x1"+" );", file=f)
            n +=1
            print("  TEST_ADC_VIM_OP( "+str(n)+",  %s.vim, " %
                instr+"5201314"+", "+"0xfffff000"+", "+"0x1"+" );", file=f)
            n +=1
            print("  TEST_ADC_VIM_OP( "+str(n)+",  %s.vim, " %
                instr+"5201314"+", "+"0xffffeee0"+", "+"0xf"+" );", file=f)     

    
def generate_tests_vvmvxmvim(instr, f, rs1_val, rs2_val, lmul, vsew, generate_vim=True):
    lmul = 1 if lmul < 1 else int(lmul)
    n = 1
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    for i in range(100):     
        k = i%31+1
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0:
            continue
        n+=1
        print("  TEST_VVM_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+");",file=f)
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs1_val[i]+" , "+rs2_val[i]+");",file=f)

    if vsew == 8:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 101);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 10);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 12);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -86, 3);", file=f)
    elif vsew == 16:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 26213);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 180);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 182);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -21846, 3);", file=f)
    elif vsew == 32:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 1717986917);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46339);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46341);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -1431655766, 3);", file=f)
    elif vsew == 64:
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 7378697629483820645);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000498);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000500);", file=f)
        n += 1
        print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -6148914691236517206, 3);", file=f)


    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(len(rs1_val)):
        n += 1
        print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
              instr+"5201314"+", "+rs1_val[i]+", "+rs2_val[i]+" );", file=f)
    if generate_vim:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314"+", "+rs1_val[i]+", "+" 4 "+" );", file=f)