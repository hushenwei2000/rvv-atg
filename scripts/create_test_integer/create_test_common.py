import os
import re

from scripts.test_common_info import is_overlap

def generate_macros_vvvxvi(f, lmul, no_fail = False):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#define TEST_VV_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
            MY_RVTEST_SIGUPD(x20, v24) \\\n\
        )", file=f)
    print("#define TEST_VX_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v16, v8, x1%s;"%(", v0.t" if masked else "") + " ; \\\n\
            MY_RVTEST_SIGUPD(x12, v16) \\\n\
        )", file=f)
    print("#define TEST_VI_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v8, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " ; \\\n\
            MY_RVTEST_SIGUPD(x24, v16) \\\n\
        )", file=f)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n)  + " \\\n\
            inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VV_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, result,"%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v%d, v16, v8%s;"%(n, (", v0.t" if masked else ""))+" \\\n\
        ) ", file=f)
    print("#define TEST_VV_OP_rd8( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v8, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v8, v24, v16%s;"%(", v0.t" if masked else "") + " ; \\\n\
        )", file=f)
    print("#define TEST_VV_OP_rd16( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)


def generate_macros_vw(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_W_WV_OP \n\
#define TEST_W_WV_OP( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    print("#undef TEST_W_WX_OP \n\
#define TEST_W_WX_OP( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        li x1, MASK_XLEN(val2); \\\n\
        inst v24, v8, x1%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    print("#undef TEST_W_VV_OP \n\
#define TEST_W_VV_OP( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    print("#undef TEST_W_VX_OP \n\
#define TEST_W_VX_OP( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val2); \\\n\
        inst v24, v8, x1%s;"%(", v0.t" if masked else "") + " ; ; \\\n\
    )", file=f)

    for n in range(1, 32):
        if n != 8 and n != 16 and n != 24 and n % lmul == 0:
            print("#define TEST_W_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s;"%(n, (", v0.t" if masked else ""))+" \\\n\
            )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 8 and n != 16 and n != 24:
            print("#define TEST_W_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v%d, result, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v%d, v8, v16%s;"%(n, (", v0.t" if masked else ""))+" \\\n\
            )",file=f)

def generate_macros_vwmacc(f, lmul):
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_W_VX_OP_RV \n\
#define TEST_W_VX_OP_RV( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_DOUBLE_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val2; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        li x1, MASK_XLEN(val1); \\\n\
        inst v24, x1, v8%s;"%(", v0.t" if masked else "")+" ; \\\n\
    )", file=f)

    print("#undef TEST_W_VV_OP_WITH_INIT \n\
#define TEST_W_VV_OP_WITH_INIT( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP_W( testnum, v24, result, \\\n\
        VSET_DOUBLE_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
        VSET_VSEW_4AVL \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        inst v24, v8, v16%s;"%((", v0.t" if masked else ""))+" ; \\\n\
    )", file=f)

    for n in range(2, 32):
        if n != 8 and n != 16 and n != 24 and n % lmul == 0:
            print("#define TEST_W_VV_OP_WITH_INIT_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v24, result,  \\\n\
                VSET_DOUBLE_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
                )",file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n%(2*lmul) ==0 and n != 8 and n != 16 and n != 24:
            print("#define TEST_W_VV_OP_WITH_INIT_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE_LOOP_W( testnum, v%d, result, "%n + "\\\n\
                VSET_DOUBLE_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(64 if vsew == 64 else vsew*2, n) + " \\\n\
                VSET_VSEW_4AVL \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v%d, v8, v16%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
                )",file=f)

def generate_macros_muladd(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_VV_OP_WITH_INIT \n\
#define TEST_VV_OP_WITH_INIT( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VV_OP_WITH_INIT_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE_LOOP( testnum, v24, result,  \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v%d, v16%s; "%(n, ", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_VV_OP_WITH_INIT_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, result, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v%d, v8, v16%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
        ) ", file=f)
    print("#define TEST_VV_OP_WITH_INIT_rd8( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v8, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            inst v8, v16, v24%s; "%(", v0.t" if masked else "") + "; \\\n\
        )", file=f)
    print("#define TEST_VV_OP_WITH_INIT_rd16( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            inst v16, v8, v24%s; "%(", v0.t" if masked else "") + "; \\\n\
        )", file=f)

    print("#udnef TEST_VX_OP_RV \n\
#define TEST_VX_OP_RV( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val1); \\\n\
            inst v24, x1, v8%s; "%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

def generate_macros_vadc(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False

    print("#undef TEST_ADC_VV_OP \n\
#define TEST_ADC_VV_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16, v0; \\\n\
        )", file=f)
    print("#undef TEST_ADC_VX_OP \n\
#define TEST_ADC_VX_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_VSEW(val2); \\\n\
            inst v24, v8, x1, v0; \\\n\
        )", file=f)
    print("#undef TEST_ADC_VI_OP \n\
#define TEST_ADC_VI_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2), v0; \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_ADC_VV_OP_1%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            inst v24, v8, v%d, v0; "%n + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_ADC_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE_LOOP( testnum, v%d, result,"%n + " \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v%d, v8, v16, v0;"%n+" \\\n\
        ) ",file=f)
    print("#define TEST_ADC_VV_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP( testnum, v8, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        inst v8, v16, v24, v0; \\\n\
        )", file = f)
    print("#define TEST_ADC_VV_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
    TEST_CASE_LOOP( testnum, v16, result, \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v16, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        la x7, val2; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        inst v16, v8, v24, v0; \\\n\
        )", file = f)


def generate_macros_vmadc(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#undef TEST_MADC_VV_OP \n\
#define TEST_MADC_VV_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16; \\\n\
        )", file=f)

    print("#undef TEST_MADC_VX_OP \n\
#define TEST_MADC_VX_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_XLEN(val2); \\\n\
            inst v24, v8, x1; \\\n\
        )", file=f)

    print("#undef TEST_MADC_VI_OP \n\
#define TEST_MADC_VI_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2); \\\n\
        )", file=f)

    print("#define TEST_MADC_VVM_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v24, v8, v16, v0; \\\n\
        )", file=f)

    print("#define TEST_MADC_VXM_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            li x1, MASK_VSEW(val2); \\\n\
            inst v24, v8, x1, v0; \\\n\
        )", file=f)

    print("#define TEST_MADC_VIM_OP( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2), v0; \\\n\
        )", file=f)

    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % lmul != 0:
            continue
        print("#define TEST_MADC_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d; "%n + " \\\n\
            )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16 or n == 24 or n % (lmul * 2) != 0:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_MADC_VV_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
        TEST_CASE_MASK_4VL( testnum, v%d, result, "%n + "\\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v%d, v8, v16; "%n + " \\\n\
        ) ", file=f)
    print("#define TEST_MADC_VV_OP_rd8( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v8, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            inst v8, v24, v16; \\\n\
        )", file=f)
    print("#define TEST_MADC_VV_OP_rd16( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_MASK_4VL( testnum, v16, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v16, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v16, v24, v8; \\\n\
        )", file=f)

def generate_macros_vvmvxmvim(f, lmul, generate_vv = True, generate_vx = True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    if generate_vv:
        print("#undef TEST_VVM_OP \n\
#define TEST_VVM_OP( testnum, inst, result, val1, val2 ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v24, v8, v16%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n == 8 or n == 16 or n == 24 or n % lmul != 0:
                continue
            print("#define TEST_VVM_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
                TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v8, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            if n == 8 or n == 16 or n == 24 or n % (lmul * 2) != 0:
                continue
            # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
            print("#define TEST_VVM_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v%d, result, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v%d, v8, v16%s; "%(n, (", v0.t" if masked else "")) + "\\\n\
            ) ", file=f)
        print("#define TEST_VVM_OP_rd8( testnum, inst, result, val2, val1 ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v8, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                inst v8, v24, v16%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)
        print("#define TEST_VVM_OP_rd16( testnum, inst, result, val2, val1 ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v16, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                la x7, val2; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                inst v16, v24, v8%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)

    if generate_vx:
        print("#undef TEST_VXM_OP \n\
#define TEST_VXM_OP( testnum, inst, result, val1, val2 ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x1, MASK_XLEN(val2); \\\n\
                inst v24, v8, x1%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)
        for n in range(1, 32):
            print("#define TEST_VXM_OP_1%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, result,  \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x%d, MASK_XLEN(val2);"%n + " \\\n\
                inst v24, v8, x%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
        for n in range(1, 32):
            print("#define TEST_VXM_OP_rd%d( testnum, inst, result, val1, val2 ) "%n + " \\\n\
            TEST_CASE_MASK_4VL( testnum, v%d, result, "%n + "\\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x1, MASK_XLEN(val2); \\\n\
                inst v%d, v8, x1%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)
        print("#define TEST_VXM_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v8, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v16, (x7);"%vsew + " \\\n\
                li x1, MASK_XLEN(val2); \\\n\
                inst v8, v16, x1%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)
        print("#define TEST_VXM_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
            TEST_CASE_MASK_4VL( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                li x1, MASK_XLEN(val2); \\\n\
                inst v24, v8, x1%s; "%(", v0.t" if masked else "") + " \\\n\
            )", file=f)

    print("#undef TEST_VIM_OP \n\
#define TEST_VIM_OP( testnum, inst, result, val1, val2 ) \
        TEST_CASE_MASK_4VL( testnum, v24, result, \
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v8, SEXT_IMM(val2)%s; "%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

def generate_macros_nvvnvxnvi(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False

    print("#undef TEST_N_VV_OP \n\
#define TEST_N_VV_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            la x7, val1; \\\n\
            vle%d.v v8, (x7);"%vsew + " \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

    print("#undef TEST_N_VX_OP \n\
#define TEST_N_VX_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            li x1, MASK_VSEW(val1); \\\n\
            inst v24, v16, x1%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

    print("#undef TEST_N_VI_OP \n\
#define TEST_N_VI_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE_LOOP( testnum, v24, result, \\\n\
            VSET_VSEW_4AVL \\\n\
            la x7, rd_origin_data; \\\n\
            vle%d.v v24, (x7);"%vsew + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            la x7, val2; \\\n\
            vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
            inst v24, v16, SEXT_IMM(val1)%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

    for n in range(1, 32):
        print("#define TEST_N_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            )", file=f)
    for n in range(1, 32):
        if n % lmul == 0:
            print("#define TEST_N_VV_OP_rd%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, result,"%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val2; \\\n\
                vle%d.v v16, (x7);"%(64 if vsew == 64 else vsew*2) + " \\\n\
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%vsew + " \\\n\
                inst v%d, v16, v8%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
            ) ", file=f)

def generate_macros_vred(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    print("#define TEST_VV_OP( testnum, inst, result, val2, val1 ) \\\n\
        TEST_CASE( testnum, v24, result, \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            inst v24, v16, v8%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    for n in range(2, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        print("#define TEST_VV_OP_1%d( testnum, inst, result, val2, val1 )"%n + " \\\n\
            TEST_CASE( testnum, v24, result, \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v%d, x7;"% n + " \\\n\
            inst v24, v16, v%d%s; "%(n, (", v0.t" if masked else "")) + " \\\n\
        )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 8 or n == 16 or n == 24:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VV_OP_rd%d( testnum, inst, result, val1, val2 )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result,"%n + " \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v16, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v8, x7; \\\n\
            inst v%d, v16, v8%s; "%(n, (", v0.t" if masked else "")) + "\\\n\
        ) ", file=f)
    print("#define TEST_VV_OP_rd8( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v8, result, \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v24, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v16, x7; \\\n\
            inst v8, v24, v16%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)
    print("#define TEST_VV_OP_rd16( testnum, inst, result, val1, val2 ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
            li x7, MASK_VSEW(val2); \\\n\
            vmv.v.x v8, x7; \\\n\
            li x7, MASK_VSEW(val1); \\\n\
            vmv.v.x v24, x7; \\\n\
            inst v16, v8, v24%s;"%(", v0.t" if masked else "") + " \\\n\
        )", file=f)

def generate_macros_vwred(f, lmul):
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


def generate_macros_ext_op(f, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    masked = True if os.environ['RVV_ATG_MASKED'] == "True" else False
    lmul = 1 if lmul < 1 else int(lmul)
    print("#undef TEST_EXT_OP \n\
#define TEST_EXT_OP( testnum, inst, result, val1 ) \\\n\
    TEST_CASE_LOOP( testnum, v24, result,  \\\n\
        VSET_VSEW_4AVL \\\n\
        la x7, rd_origin_data; \\\n\
        vle%d.v v24, (x7);"%vsew + " \\\n\
        %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
        la x7, val1; \\\n\
        vle%d.v v8, (x7);"%vsew + " \\\n\
        inst v24, v8%s;"%(", v0.t" if masked else "") + " \\\n\
    )", file=f)
    for n in range(1, 32):
        if n % lmul != 0 or n == 24:
            continue
        print("#define TEST_EXT_OP_rs1_%d( testnum, inst, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v24, result, \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v24, (x7);"%vsew + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                inst v24, v%d%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

    for n in range(1, 32):
        if n % lmul != 0 or n == 8:
            continue
        print("#define TEST_EXT_OP_rd_%d( testnum, inst, result, val1 )"%n + " \\\n\
            TEST_CASE_LOOP( testnum, v%d, result, "%n + " \\\n\
                VSET_VSEW_4AVL \\\n\
                la x7, rd_origin_data; \\\n\
                vle%d.v v%d, (x7);"%(vsew, n) + " \\\n\
                %s "%("la x7, mask_data; \\\n    vle%d.v v0, (x7); \\\n  "%vsew if masked else "")+" \
                la x7, val1; \\\n\
                vle%d.v v8, (x7);"%(vsew) + " \\\n\
                inst v%d, v8%s; "%(n, ", v0.t" if masked else "") + " \\\n\
            )", file = f)

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

def generate_tests_vvvxvi(instr, f, rs1_val, rs2_val, lmul, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_0)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VV_OP( "+str(n)+",  %s.%s, "%(instr, instr_suffix) + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
        for i in range(min(32, loop_num)):     
            k = i%31+1
            if k % lmul != 0 or k == 24:
                continue
            n+=1
            print("  TEST_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
            
            k = i%30+2
            if k % lmul != 0 or k == 8 or k == 16 or k == 24:
                continue
            n +=1
            # print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
        
        # if vsew == 8:
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 101, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 10, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 12, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -86);", file=f)
        # elif vsew == 16:
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 26213, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 180, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 182, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -21846);", file=f)
        # elif vsew == 32:
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 1717986917, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46339, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46341, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -1431655766);", file=f)
        # elif vsew == 64:
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 7378697629483820645, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000498, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000500, 3);", file=f)
        #     n += 1
        #     print("  TEST_VV_OP( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -6148914691236517206);", file=f)

            print("  TEST_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VX_OP( "+str(n)+",  %s.vx, " %
                instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[0]), file=f)
    vx_test_num = n - vv_test_num
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"rd_data_vi+%d, rs2_data+%d, 15)"%(i*step_bytes, i*step_bytes), file=f)
    vi_test_num = n - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vw(f, rs1_val, rs2_val, instr, lmul, instr_suffix='vv', generate_vx = True, generate_wvwx = True):
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul = float(os.environ['RVV_ATG_LMUL'])
    lmul_double = lmul * 2
    lmul_1 = 1 if lmul < 1 else int (lmul)
    lmul_double_1 = 1 if lmul_double < 1 else int (lmul_double)
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    step_bytes_double = step_bytes * 2
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_W_VV_OP( "+str(n)+",  %s.%s, " %
              (instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):
        k = i%31+1
        if k%(2*lmul)==0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul_double_1, 8, lmul_1) and not is_overlap(k, lmul_double_1, 16, lmul_1):
            n+=1
            print("  TEST_W_VV_OP_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes),file=f)
        
        k = i%30+2
        if k % lmul == 0 and k != 16 and k != 8 and k != 24 and not is_overlap(24, lmul_double_1, k, lmul_1):
            n +=1
            print("  TEST_W_VV_OP_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes),file=f)
    
    # if vsew == 8:
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
    # elif vsew == 16:
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
    # elif vsew == 32:
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
    # elif vsew == 64:
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
    
    vv_test_num = n
    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_W_VX_OP( "+str(n)+",  %s.vx, " %
                instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes_double, i*step_bytes, rs1_val[i]), file=f)
    
    vx_test_num = n - vv_test_num

    wv_test_num = 0
    wx_test_num = 0
    if generate_wvwx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # WV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_W_WV_OP( "+str(n)+",  %s.wv, " %
                instr+"rd_data_wv+%d, rs2_data_widen+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes_double, i*step_bytes), file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  # WX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_W_WX_OP( "+str(n)+",  %s.wx, " %
                instr+"rd_data_wx+%d, rs2_data_widen+%d, %s)"%(i*step_bytes_double, i*step_bytes_double, rs1_val[i]), file=f)
        wv_test_num = wx_test_num = loop_num
    
    return (vv_test_num, vx_test_num, wv_test_num, wx_test_num)
              
def generate_tests_vwmacc(f, rs1_val, rs2_val, instr, lmul, instr_suffix='vv', generate_vxrv=True):
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
    step_bytes_double = step_bytes * 2
    print("  #-------------------------------------------------------------", file=f)
    print("  # VV Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s, " %
              (instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)): 
        k = i%31+1
        if k%(2*lmul)==0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul_double_1, 8, lmul_1)and not is_overlap(k, lmul_double_1, 16, lmul_1):
            n+=1
            print("  TEST_W_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes),file=f)
        
        k = i%30+2
        if k % lmul == 0 and k != 8 and k != 16 and k != 24 and not is_overlap(24, lmul_double_1, k, lmul_1):
            n +=1
            print("  TEST_W_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.%s, "%(instr, instr_suffix)+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes_double, i*step_bytes, i*step_bytes),file=f)
    
    # if vsew == 8:
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 101, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 10, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 12, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -86);", file=f)
    # elif vsew == 16:
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 26213, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 180, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 182, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -21846);", file=f)
    # elif vsew == 32:
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 1717986917, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46339, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 46341, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -1431655766);", file=f)
    # elif vsew == 64:
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 7378697629483820645, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000498, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3037000500, 3);", file=f)
    #     n += 1
    #     print("  TEST_W_VV_OP_WITH_INIT( "+str(n)+",  %s.%s"%(instr, instr_suffix) + ", 5201314, 3, -6148914691236517206);", file=f)

    vv_test_num = n
    if generate_vxrv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
                instr+"rd_data_vx+%d, %s, rs2_data+%d)"%(i*step_bytes_double, rs1_val[i], i*step_bytes), file=f)
    vx_test_num = n - vv_test_num
    return (vv_test_num, vx_test_num)


def generate_tests_muladd(instr, f, rs1_val, rs2_val, lmul):
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv, " %
              instr + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k == 24 or k % lmul != 0:
            continue
        n+=1
        print("  TEST_VV_OP_WITH_INIT_rd%d( "%k+str(n)+",  %s.vv, "%instr+ "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
        
        k = i%30+2
        if k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_VV_OP_WITH_INIT_1%d( "%k+str(n)+",  %s.vv, "%instr + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    
    # if vsew == 8:
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 101);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 10);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 12);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -86, 3);", file=f)
    # elif vsew == 16:
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 26213);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 180);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 182);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -21846, 3);", file=f)
    # elif vsew == 32:
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 1717986917);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46339);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46341);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -1431655766, 3);", file=f)
    # elif vsew == 64:
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 7378697629483820645);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000498);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000500);", file=f)
    #     n += 1
    #     print("  TEST_VV_OP_WITH_INIT( "+str(n)+",  %s.vv"%instr + ", 5201314, -6148914691236517206, 3);", file=f)


    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_VX_OP_RV( "+str(n)+",  %s.vx, " %
              instr + "rd_data_vx+%d, %s, rs1_data+%d)"%(i*step_bytes, rs1_val[0], i*step_bytes), file=f)
    vx_test_num = n - vv_test_num
    
    return (vv_test_num, vx_test_num, 0)
  

def generate_tests_vmadc(instr, f, rs1_val, rs2_val, lmul, generate_vi = True):
    lmul = 1 if lmul < 1 else int(lmul)
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_MADC_VV_OP( "+str(n)+",  %s.vv, " %
              instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0:
            continue
        n+=1
        print("  TEST_MADC_VV_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes),file=f)
        
        k = i%30+2
        if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
    #     print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );",file=f)
    
    # if vsew == 8:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
    # elif vsew == 16:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
    # elif vsew == 32:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
    # elif vsew == 64:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)


        print("  TEST_MADC_VV_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes),file=f)
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VVM Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        # n +=1
        # print("  TEST_ADC_VVM_OP( "+str(n)+",  %s.vvm, " %
        #       instr+"5201314"+", "+"0xffffffee"+", "+"0x00000001"+" );", file=f)
        # n +=1
        # print("  TEST_ADC_VVM_OP( "+str(n)+",  %s.vvm, " %
        #       instr+"5201314"+", "+"0xfffff000"+", "+"0x00000001"+" );", file=f)
        # n +=1
        # print("  TEST_ADC_VVM_OP( "+str(n)+",  %s.vvm, " %
        #       instr+"5201314"+", "+"0xffffeee0"+", "+"0xffffffff"+" );", file=f)
        n += 1
        print("  TEST_MADC_VVM_OP( "+str(n)+",  %s.vvm, " %
              instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes), file=f)
        
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(loop_num):
        # n += 1
        # print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
        #       instr+"5201314"+", "+"0x00000000"+", "+"0x00000000"+" );", file=f)
        # n +=1
        # print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
        #       instr+"5201314"+", "+"0x00000000"+", "+"0x00000011"+" );", file=f)
        # n +=1
        # print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
        #       instr+"5201314"+", "+"0xffffffff"+", "+"0x00000001"+" );", file=f)
        # n +=1
        # print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
        #       instr+"5201314"+", "+"0xffffffff"+", "+"0xffffffff"+" );", file=f)
        n += 1
        print("  TEST_MADC_VX_OP( "+str(n)+",  %s.vx, " %
               instr+"5201314, rs2_data+%d, %s)"%(i*step_bytes, rs1_val[i % len(rs1_val)]), file=f)
        
    print("  #-------------------------------------------------------------", file=f)
    print("  # VXM Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        # n +=1
        # print("  TEST_ADC_VXM_OP( "+str(n)+",  %s.vxm, " %
        #       instr+"5201314"+", "+"0xffffffee"+", "+"0x00000001"+" );", file=f)
        # n +=1
        # print("  TEST_ADC_VXM_OP( "+str(n)+",  %s.vxm, " %
        #       instr+"5201314"+", "+"0xfffff000"+", "+"0x00000001"+" );", file=f)
        # n +=1
        # print("  TEST_ADC_VXM_OP( "+str(n)+",  %s.vxm, " %
        #       instr+"5201314"+", "+"0xffffeee0"+", "+"0xffffffff"+" );", file=f)
        n +=1
        print("  TEST_MADC_VXM_OP( "+str(n)+",  %s.vxm, " %
              instr+"5201314, rs2_data+%d, %s)"%(i*step_bytes, rs1_val[i % len(rs1_val)]), file=f)

    vx_test_num = n - vv_test_num

    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            # n +=1
            # print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
            #     instr+"5201314"+", "+"0xffffffee"+", "+"0x1"+" );", file=f)
            # n +=1
            # print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
            #     instr+"5201314"+", "+"0xfffff000"+", "+"0x0"+" );", file=f)
            # n +=1
            # print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
            #     instr+"5201314"+", "+"0xffffeee0"+", "+"0xe"+" );", file=f)
            n +=1
            print("  TEST_MADC_VI_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314, rs2_data+%d, 14)"%(i*step_bytes), file=f)
            
        print("  #-------------------------------------------------------------", file=f)
        print("  # VIM Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            # n +=1
            # print("  TEST_ADC_VIM_OP( "+str(n)+",  %s.vim, " %
            #     instr+"5201314"+", "+"0xffffffee"+", "+"0x1"+" );", file=f)
            # n +=1
            # print("  TEST_ADC_VIM_OP( "+str(n)+",  %s.vim, " %
            #     instr+"5201314"+", "+"0xfffff000"+", "+"0x1"+" );", file=f)
            # n +=1
            # print("  TEST_ADC_VIM_OP( "+str(n)+",  %s.vim, " %
            #     instr+"5201314"+", "+"0xffffeee0"+", "+"0xf"+" );", file=f)   
            n +=1
            print("  TEST_MADC_VIM_OP( "+str(n)+",  %s.vim, " %
                instr+"5201314, rs2_data+%d, 14)"%(i*step_bytes), file=f)     

    vi_test_num = n - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vadc(instr, f, rs1_val, rs2_val, lmul, generate_vi=True):
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_ADC_VV_OP( "+str(n)+",  %s.vvm, " %
              instr+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k == 24 or k % lmul != 0:
            continue
        n+=1
        print("  TEST_ADC_VV_OP_rd%d( "%k+str(n)+",  %s.vvm, "%instr+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
        
        k = i%30+2
        if k == 8 or k == 16 or k == 24 or k % lmul != 0:
            continue
        n +=1
        print("  TEST_ADC_VV_OP_1%d( "%k+str(n)+",  %s.vvm, "%instr+"rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
    
    vv_test_num = n
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_ADC_VX_OP( "+str(n)+",  %s.vxm, " %
              instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[i % len(rs1_val)]), file=f)
    vx_test_num = n - vv_test_num
    
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_ADC_VI_OP( "+str(n)+",  %s.vim, " %
                instr+"rd_data_vi+%d, rs2_data+%d, 14)"%(i*step_bytes, i*step_bytes), file=f)
    vi_test_num = n - vx_test_num

    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vvmvxmvim(instr, f, rs1_val, rs2_val, lmul, generate_vv=True, generate_vx=True, generate_vi=True):
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    if generate_vv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VV Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VVM_OP( "+str(n)+",  %s.vv, " %
                instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes), file=f)
        for i in range(min(32, loop_num)): 
            k = i%31+1
            if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0:
                continue
            n+=1
            print("  TEST_VVM_OP_rd%d( "%k+str(n)+",  %s.vv, "%instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes),file=f)
            
            k = i%30+2
            if k == 0 or k == 8 or k == 16 or k == 24 or k % lmul != 0:
                continue
            n +=1
            print("  TEST_VVM_OP_1%d( "%k+str(n)+",  %s.vv, "%instr+"5201314, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes),file=f)
    vv_test_num = n

    if generate_vx:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VXM_OP( "+str(n)+",  %s.vx, " %
                instr+"5201314, rs2_data+%d, %s)"%(i*step_bytes, rs1_val[i % len(rs1_val)]), file=f)
        for i in range(min(32, loop_num)):
            k = i%31+1
            if k == 0 or k == 24 or k % (lmul * 2) != 0:
                continue
            n+=1
            print("  TEST_VXM_OP_rd%d( "%k+str(n)+",  %s.vx, "%instr+"5201314, rs2_data+%d, %s)"%(i*step_bytes, rs1_val[i % len(rs1_val)]),file=f)
            
            k = i%30+2
            if k == 0 or k == 8 or k == 16 or k == 24 or k % (lmul * 2) != 0:
                continue
            n +=1
            print("  TEST_VXM_OP_1%d( "%k+str(n)+",  %s.vx, "%instr+"5201314, rs2_data+%d, %s)"%(i*step_bytes, rs1_val[i % len(rs1_val)]),file=f)

    vx_test_num = n - vv_test_num
    if generate_vi:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VI Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(loop_num):
            n += 1
            print("  TEST_VIM_OP( "+str(n)+",  %s.vi, " %
                instr+"5201314, rs2_data+%d, 4)"%(i*step_bytes), file=f)
    
    vi_test_num = n - vx_test_num
    return (vv_test_num, vx_test_num, vi_test_num)

def print_common_ending_rs1rs2rd(rs1_val, rs2_val, f):
    print("")

def generate_tests_nvvnvxnvi(instr, f, rs1_val, rs2_val, lmul):
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
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_N_VV_OP( "+str(n)+",  %s.wv, " %
              instr + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes), file=f)
    for i in range(min(32, loop_num)):     
        k = i%31+1
        if k%lmul == 0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul, 16, lmul*2):
            n+=1
            print("  TEST_N_VV_OP_rd%d( "%k+str(n)+",  %s.wv, "%instr + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)
        
        k = i%30+2
        if k%lmul == 0 and k != 8 and k != 16 and k != 24 and not is_overlap(k, lmul, 16, lmul*2):
            n +=1
            print("  TEST_N_VV_OP_1%d( "%k+str(n)+",  %s.wv, "%instr + "rd_data_vv+%d, rs2_data+%d, rs1_data+%d)"%(i*step_bytes, i*step_bytes, i*step_bytes),file=f)

    # if vsew == 8:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 101, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 10, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 12, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -86);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 101);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 10);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 12);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -86, 3);", file=f)
    # elif vsew == 16:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 26213, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 180, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 182, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -21846);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 26213);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 180);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 182);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -21846, 3);", file=f)
    # elif vsew == 32:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 1717986917, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46339, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 46341, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -1431655766);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 1717986917);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46339);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 46341);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -1431655766, 3);", file=f)
    # elif vsew == 64:
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 7378697629483820645, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000498, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3037000500, 3);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, -6148914691236517206);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 7378697629483820645);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000498);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, 3, 3037000500);", file=f)
    #     n += 1
    #     print("  TEST_VVM_OP( "+str(n)+",  %s.vv"%instr + ", 5201314, -6148914691236517206, 3);", file=f)

    vv_test_num = n
    print("  #-------------------------------------------------------------", file=f)
    print("  # VX Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_N_VX_OP( "+str(n)+",  %s.wx, " %
              instr+"rd_data_vx+%d, rs2_data+%d, %s)"%(i*step_bytes, i*step_bytes, rs1_val[i % len(rs1_val)]), file=f)
    
    vx_test_num = n - vv_test_num
    
    print("  #-------------------------------------------------------------", file=f)
    print("  # VI Tests", file=f)
    print("  #-------------------------------------------------------------", file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)", file=f)
    for i in range(loop_num):
        n += 1
        print("  TEST_N_VI_OP( "+str(n)+",  %s.wi, " %
              instr+"rd_data_vi+%d, rs2_data+%d, 4)"%(i*step_bytes, i*step_bytes), file=f)

    vi_test_num = n - vx_test_num
    return (vv_test_num, vx_test_num, vi_test_num)

def generate_tests_vred(instr, f, rs1_val, rs2_val, lmul, instr_suffix='vv', generate_vi = True, generate_vx = True, generate_vv = True):
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
    
def generate_tests_vwred(f, rs1_val, rs2_val, instr, lmul, instr_suffix='vv', generate_vxrv=True):
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
    if generate_vxrv:
        print("  #-------------------------------------------------------------", file=f)
        print("  # VX Tests", file=f)
        print("  #-------------------------------------------------------------", file=f)
        print("  RVTEST_SIGBASE( x20,signature_x20_1)", file=f)
        for i in range(len(rs1_val)):
            n += 1
            print("  TEST_W_VX_OP_RV( "+str(n)+",  %s.vx, " %
                instr+"5201314"+", "+rs2_val[i]+", "+rs1_val[i]+" );", file=f)

def generate_tests_ext_op(instr, f, rs1_val, rs2_val, lmul):
    vlen = int(os.environ['RVV_ATG_VLEN'])
    vsew = int(os.environ['RVV_ATG_VSEW'])
    lmul_1 = 1 if lmul < 1 else int(lmul)
    n = 0
    
    num_elem = int((vlen * lmul / vsew))
    if num_elem == 0:
        return 0
    loop_num = int(min(len(rs1_val), len(rs2_val)) / num_elem)
    step_bytes = int(vlen * lmul / 8)
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)
    for i in range(loop_num):
        if int(vsew / 2) >= 8: 
            print("TEST_EXT_OP( %d,  %s.vf2, "%(n, instr) + "rd_data_vv+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes), file=f)
            n += 1
    count1 = n
    for i in range(loop_num):
        if int(vsew / 4) >= 8:
            print("TEST_EXT_OP( %d,  %s.vf4, "%(n, instr) + "rd_data_vv+%d, rs1_data+%d);"%((count1 + i)*step_bytes, i*step_bytes), file=f)
            n += 1
    count2 = n
    for i in range(loop_num):
        if int(vsew / 8) >= 8:
            print("TEST_EXT_OP( %d,  %s.vf8, "%(n, instr) + "rd_data_vv+%d, rs1_data+%d);"%((count2 + i)*step_bytes, i*step_bytes), file=f)
            n += 1
    
    print("  #-------------------------------------------------------------",file=f)
    print("  # %s Tests (different register)"%instr,file=f)
    print("  #-------------------------------------------------------------",file=f)
    print("  RVTEST_SIGBASE( x12,signature_x12_1)",file=f)

    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8:
            continue
        if int(vsew / 2) >= 8: 
            print("TEST_EXT_OP_rd_%d( %d,  %s.vf2, "%(k, n, instr) + "rd_data_vv+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes), file=f)
            n += 1
    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8:
            continue
        if int(vsew / 4) >= 8:
            print("TEST_EXT_OP_rd_%d( %d,  %s.vf4, "%(k, n, instr) + "rd_data_vv+%d, rs1_data+%d);"%((count1 + i)*step_bytes, i*step_bytes), file=f)
            n += 1
    for i in range(min(32, loop_num)):
        k = i % 31 + 1  
        if k % lmul != 0 or k == 8:
            continue
        if int(vsew / 8) >= 8:
            print("TEST_EXT_OP_rd_%d( %d,  %s.vf8, "%(k, n, instr) + "rd_data_vv+%d, rs1_data+%d);"%((count2 + i)*step_bytes, i*step_bytes), file=f)
            n += 1


    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 24:
            continue
        if int(vsew / 2) >= 8: 
            print("TEST_EXT_OP_rs1_%d( %d,  %s.vf2, "%(k, n, instr) + "rd_data_vv+%d, rs1_data+%d);"%(i*step_bytes, i*step_bytes), file=f)
            n += 1

    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 24:
            continue
        if int(vsew / 4) >= 8:
            print("TEST_EXT_OP_rs1_%d( %d,  %s.vf4, "%(k, n, instr) + "rd_data_vv+%d, rs1_data+%d);"%((count1 + i)*step_bytes, i*step_bytes), file=f)
            n += 1

    for i in range(min(32, loop_num)):
        k = i % 31 + 1
        if k % lmul != 0 or k == 24:
            continue
        if int(vsew / 8) >= 8:
            print("TEST_EXT_OP_rs1_%d( %d,  %s.vf8, "%(k, n, instr) + "rd_data_vv+%d, rs1_data+%d);"%((count2 + i)*step_bytes, i*step_bytes), file=f)
            n += 1
    
    return (n, 0, 0)
