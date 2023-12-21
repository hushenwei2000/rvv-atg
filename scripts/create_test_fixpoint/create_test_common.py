from scripts.test_common_info import is_overlap, extract_operands
import re, os
def generate_macros(f, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_AVG_VV_OP \n\
#define TEST_AVG_VV_OP( testnum, inst, vxrm_val, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#undef TEST_AVG_VX_OP \n\
#define TEST_AVG_VX_OP( testnum, inst, vxrm_val, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v24, v16, x1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#undef TEST_AVG_VI_OP \n\
#define TEST_AVG_VI_OP( testnum, inst, vxrm_val, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v16, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul == 0 and n != 24 and n != 8 and n != 16:
            print("#define TEST_AVG_VV_OP_1_%d( testnum, inst, vxrm_val, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                csrwi vxrm, vxrm_val; \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew,n) + " \\\n\
                inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + "\\\n\
            )", file=f)
    for n in range(1, 32):
        if n % (lmul * 2) == 0 and n != 24 and n != 8 and n != 16:
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            print("#define TEST_AVG_VV_OP_rd%d( testnum, inst, vxrm_val,  val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                csrwi vxrm, vxrm_val; \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                inst v%d, v16, v8%s; "%(n, (", v0.t" if masked else "")) + "\\\n\
            )", file=f)

def generate_macros_vnclip(f, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_AVG_N_VV_OP \n\
#define TEST_AVG_N_VV_OP( testnum, inst, vxrm_val, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + "  \\\n\
        )", file=f)

    print("#undef TEST_AVG_N_VX_OP \n\
#define TEST_AVG_N_VX_OP( testnum, inst, vxrm_val, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            li x1, MASK_VSEW(val1); \\\n\
            inst v24, v16, x1%s;"%(", v0.t" if masked else "") + "  \\\n\
        )", file=f)

    print("#undef TEST_AVG_N_VI_OP \n\
#define TEST_AVG_N_VI_OP( testnum, inst, vxrm_val, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            csrwi vxrm, vxrm_val; \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            inst v24, v16, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + "  \\\n\
        )", file=f)
    
    for n in range(1, 32):
        if n % lmul == 0 and n != 24 and n != 8 and n != 16:
            print("#define TEST_AVG_N_VV_OP_1%d(  testnum, inst, vxrm_val, val2, val1  ) "%n + "\\\n\
            TEST_CASE_LOOP( testnum, v24, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                csrwi vxrm, vxrm_val; \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
    for n in range(1, 32):
        if n % (lmul * 2) == 0 and n != 24 and n != 8 and n != 16:
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            print("#define TEST_AVG_N_VV_OP_rd%d(  testnum, inst, vxrm_val, val2, val1  ) "%n + " \\\n\
                TEST_CASE_LOOP( testnum, v%d, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                csrwi vxrm, vxrm_val; \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v16, v8%s; "%(n, (", v0.t" if masked else "")) + "\\\n\
            )", file=f)


def generate_tests(f, rs1_val, rs2_val, instr, lmul, generate_vi = False):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_AVG_VV_OP( "+str(n)+",  %s.vv, %d, " %
                (instr, vxrm) + "rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):     
        for vxrm in range(4):
            k = i%31+1
            if k % (lmul * 2) == 0 and k != 24 and k != 8 and k != 16 and k != 12 and k != 20 and k != 24:
                n+=1
                print("  TEST_AVG_VV_OP_rd%d( "%k+str(n)+",  %s.vv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes),file=f)
            
            k = i%30+2
            if k % lmul == 0 and k != 24 and k != 8 and k != 16 and k != 12 and k != 20 and k != 24:
                n +=1
                print("  TEST_AVG_VV_OP_1_%d( "%k+str(n)+",  %s.vv, %d, "%(instr, vxrm) + "rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes),file=f)
    
    vv_test_num = n
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_AVG_VX_OP( "+str(n)+",  %s.vx, %d," %
                (instr, vxrm)+"rs2_data+%d, %s)"%(i*step_bytes, rs1_val[0]), file=f)
    
    vx_test_num = n - vv_test_num
    vi_test_num = 0
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        
        for i in range(loop_num):
            for vxrm in range(4):
                n += 1
                print("  TEST_AVG_VI_OP( "+str(n)+",  %s.vi, %d," %
                    (instr, vxrm)+"rs2_data+%d, 15)"%(i*step_bytes), file=f)
        vi_test_num = n - vv_test_num - vx_test_num
    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vnclip(f, rs1_val, rs2_val, instr, lmul):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    lmul_double_1 = 1 if (lmul * 2) < 1 else int(lmul * 2)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    print("  #-------------------------------------------------------------", file=f)
    print("  # WV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)

    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_AVG_N_VV_OP( "+str(n)+",  %s.wv, %d," %
                (instr, vxrm) + "rs2_data+%d, rs1_data+%d)"%(i*step_bytes*2, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):
        for vxrm in range(4):
            k = i%31+1
            if k % (lmul * 2) == 0 and k != 24 and k != 8 and k != 16 and not is_overlap(k, lmul_1, 16, lmul_double_1) and k != 12 and k != 20 and k != 24:
                n+=1
                print("  TEST_AVG_N_VV_OP_rd%d( "%k+str(n)+",  %s.wv, %d,"%(instr, vxrm) + "rs2_data+%d, rs1_data+%d)"%(i*step_bytes*2, i*step_bytes),file=f)
            
            k = i%30+2
            if k % lmul == 0 and k != 24 and k != 8 and k != 16 and not is_overlap(k, lmul_1, 16, lmul_double_1) and k != 12 and k != 20 and k != 24:
                n +=1
                print("  TEST_AVG_N_VV_OP_1%d( "%k+str(n)+",  %s.wv,  %d,"%(instr, vxrm) + "rs2_data+%d, rs1_data+%d)"%(i*step_bytes*2, i*step_bytes),file=f)
    vv_test_num = n
    print("  #-------------------------------------------------------------", file=f)
    print("  # WX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_AVG_N_VX_OP( "+str(n)+",  %s.wx,  %d," %
                (instr, vxrm)+"rs2_data+%d, %s)"%(i*step_bytes*2, rs1_val[0]), file=f)
    vx_test_num = n - vv_test_num
    print("  #-------------------------------------------------------------", file=f)
    print("  # WI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    
    for i in range(loop_num):
        for vxrm in range(4):
            n += 1
            print("  TEST_AVG_N_VI_OP( "+str(n)+",  %s.wi,  %d," %
                (instr, vxrm)+"rs2_data+%d, 15)"%(i*step_bytes*2), file=f)
    vi_test_num = n - vv_test_num - vx_test_num
    return (vv_test_num, vx_test_num, vi_test_num)
  