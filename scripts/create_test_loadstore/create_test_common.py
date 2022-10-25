import re

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

def generate_vlseg3_macro(f, emul):
    print("#undef TEST_CASE_VLSEG3", file=f)
    print("#define TEST_CASE_VLSEG3( testnum, testreg, eew, correctval1, correctval2, correctval3, code... ) \\\n\
            test_ ## testnum: \\\n\
                code; \\\n\
                li x7, MASK_EEW(correctval1, eew); \\\n\
                li x8, MASK_EEW(correctval2, eew); \\\n\
                li x9, MASK_EEW(correctval3, eew); \\\n\
                li TESTNUM, testnum; \\\n\
                vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
                VMVXS_AND_MASK_EEW( x14, testreg, eew ) \\\n\
                VMVXS_AND_MASK_EEW( x15, v%d, eew )"%(8+emul) + " \\\n\
                VMVXS_AND_MASK_EEW( x16, v%d, eew )"%(8+emul*2) + "\\\n\
                VSET_VSEW \\\n\
                bne x14, x7, fail; \\\n\
                bne x15, x8, fail; \\\n\
                bne x16, x9, fail; \\\n\
        ", file=f)

def generate_macros_vlseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    # testreg is v8
    generate_vlseg3_macro(f, emul)
    for n in range(1, 32):
        print("#define TEST_VLSEG1_OP_1%d( testnum, inst, eew, result, base )"%n + " \\\n\
            TEST_CASE( testnum, v8, result, \\\n\
                la  x%d, base; "%n + "\\\n\
                inst v8, (x%d); "%n + "\\\n\
        )", file=f)
    for n in range(1, 31):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % emul == 0:
            print("#define TEST_VLSEG1_OP_rd%d( testnum, inst, eew, result, base )"%n + " \\\n\
                TEST_CASE( testnum, v%d, result, "%n + "\\\n\
                    la  x2, base; \\\n\
                    inst v%d, (x2); "%n + "\\\n\
            ) ", file=f)

def generate_macros_vlsseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    # testreg is v8
    generate_vlseg3_macro(f, emul)
    for n in range(1, 32):
        print("#define TEST_VLSSEG1_OP_1%d(  testnum, inst, eew, result, stride, base )"%n + " \\\n\
            TEST_CASE( testnum, v8, result, \\\n\
                la  x%d, base; "%n + "\\\n\
                li  x30, stride; \\\n\
                inst v8, (x%d), x30 ; "%n + "\\\n\
        )", file=f)
    for n in range(1, 32):
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        if n % emul == 0:
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

def generate_macros_vlxei(f, vsew, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(2, 30):
        if n == 30:
            continue
        print("#define TEST_VLXEI_OP_1%d( testnum, inst, index_eew, result1, result2, base_data, base_index )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v16, __riscv_vsew, result1, result2, \\\n\
                la  x%d, base_data; "%n + "\\\n\
                la  x30, base_index; \\\n\
                vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v8, (x30); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v16, (x%d), v8; "%n + "\\\n\
                VSET_VSEW \\\n\
        )", file=f)
    for n in range(1, 32):
        if n == 8 or n == 16:
            continue
        # Beacuse of the widening instruction, rd should valid for the destination’s EMUL
        print("#define TEST_VLXEI_OP_rd%d( testnum, inst, index_eew, result1, result2, base_data, base_index )"%n + " \\\n\
            TEST_CASE_LOAD( testnum, v%d, __riscv_vsew, result1, result2, "%n + "\\\n\
                la  x1, base_data; \\\n\
                la  x6, base_index; \\\n\
                vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v8, (x6); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v%d, (x1), v8; "%n + "\\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    print("#define TEST_VLXEI_OP_rd8( testnum, inst, index_eew, result1, result2, base_data, base_index ) \\\n\
            TEST_CASE_LOAD( testnum, v8, __riscv_vsew, result1, result2, \\\n\
                la  x1, base_data; \\\n\
                la  x2, base_index; \\\n\
                vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v16, (x2); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v8, (x1), v16; \\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    print("#define TEST_VLXEI_OP_rd16( testnum, inst, index_eew, result1, result2, base_data, base_index ) \\\n\
            TEST_CASE_LOAD( testnum, v16, __riscv_vsew, result1, result2, \\\n\
                la  x1, base_data; \\\n\
                la  x2, base_index; \\\n\
                vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \\\n\
                MK_VLE_INST(index_eew) v8, (x2); \\\n\
                VSET_VSEW_4AVL \\\n\
                inst v16, (x1), v8; \\\n\
                VSET_VSEW \\\n\
        ) ", file=f)
    print("#define TEST_VLXEI_OP_130( testnum, inst, index_eew, result1, result2, base_data, base_index )" + " \\\n\
        TEST_CASE_LOAD( testnum, v16, __riscv_vsew, result1, result2, \\\n\
            la  x30, base_data; " + "\\\n\
            la  x31, base_index; \\\n\
            vsetvli x29, x0, MK_EEW(index_eew), tu, mu; \\\n\
            MK_VLE_INST(index_eew) v8, (x31); \\\n\
            VSET_VSEW_4AVL \\\n\
            inst v16, (x30), v8; " + "\\\n\
            VSET_VSEW \\\n\
    )", file=f)
    print("#define TEST_VLXEI_OP_131( testnum, inst, index_eew, result1, result2, base_data, base_index )" + " \\\n\
        TEST_CASE_LOAD( testnum, v16, __riscv_vsew, result1, result2, \\\n\
            la  x31, base_data; " + "\\\n\
            la  x30, base_index; \\\n\
            vsetvli x29, x0, MK_EEW(index_eew), tu, mu; \\\n\
            MK_VLE_INST(index_eew) v8, (x30); \\\n\
            VSET_VSEW_4AVL \\\n\
            inst v16, (x31), v8; " + "\\\n\
            VSET_VSEW \\\n\
    )", file=f)

def generate_macros_vlxeiseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    # testreg is v8
    generate_vlseg3_macro(f, lmul)
    for n in range(1,31):
        print("#define TEST_VLXSEG1_OP_1%d( testnum, inst, index_eew, result, base_data, base_index  )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x31, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x31);    \\\n\
            inst v16, (x%d), v8 ; "%n + " \\\n\
        )",file=f)

    for n in range(1,30):
        if n == 8 or n == 16 or n % emul != 0:
            continue
        print("#define TEST_VLXSEG1_OP_rd%d( testnum, inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE( testnum, v%d, result, "%n + "\\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6);    \\\n\
            inst v%d, (x1), v8; "%n + " \\\n\
        )",file=f)

    print("#define TEST_VLXSEG1_OP_131( testnum, inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x31, base_data; \\\n\
            la  x2, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x2);    \\\n\
            inst v16, (x31), v8 ;  \\\n\
        )",file=f)
    print("#define TEST_VLXSEG1_OP_rd30( testnum, inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v30, result, \\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6);    \\\n\
            inst v30, (x1), v8 ;  \\\n\
        )",file=f)
    print("#define TEST_VLXSEG1_OP_rd24( testnum, inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v24, result, \\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6);    \\\n\
            inst v24, (x1), v8 ;  \\\n\
        )",file=f)
    print("#define TEST_VLXSEG1_OP_rd20( testnum, inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v20, result, \\\n\
            la  x1, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v8, (x6);    \\\n\
            inst v20, (x1), v8 ;  \\\n\
        )",file=f)

def generate_macros_vse(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    for n in range(1,30):
        print("#define TEST_VSE_OP_1%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d); "%n + "\\\n\
            load_inst v16, (x%d) ; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        if n == 8 or n == 16 or n == 31 or n % emul != 0:
            continue
        print("#define TEST_VSE_OP_rd%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, " + "\\\n\
            la  x1, base;  \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x30;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v16, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSE_OP_130( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x30, base;  \\\n\
            li  x2, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x2; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x30); \\\n\
            load_inst v16, (x30) ;  \\\n\
        )",file=f)

def generate_vsseg3_macro(f, emul):
    print("#undef TEST_VSSEG3_OP", file=f)
    print("#define TEST_VSSEG3_OP( testnum, load_inst, store_inst, eew, result1, result2, result3, base ) \\\n\
        TEST_CASE_VLSEG3( testnum, v8, eew, result1, result2, result3,  \\\n\
            la  x1, base; \\\n\
            li x7, MASK_EEW(result1, eew); \\\n\
            li x8, MASK_EEW(result2, eew); \\\n\
            li x9, MASK_EEW(result3, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.x v8, x7; \\\n\
            vmv.v.x v%d, x8; "%(8+emul)+" \\\n\
            vmv.v.x v%d, x9; "%(8+emul*2)+" \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x1); \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.i v8, 0; \\\n\
            vmv.v.i v%d, 0; "%(8+emul) + " \\\n\
            vmv.v.i v%d, 0; "%(8+emul*2) + " \\\n\
            VSET_VSEW \\\n\
            load_inst v8, (x1); \\\n\
        )", file=f)


def generate_macros_vsse(f):
    for n in range(1,31):
        print("#define TEST_VSSE_OP_1%d( testnum, load_inst, store_inst, eew, result, stride, base )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x29, stride;  \\\n\
            li  x30, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d), x29; "%n + "\\\n\
            load_inst v16, (x%d), x29 ; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSSE_OP_rd%d( testnum, load_inst, store_inst, eew, result, stride, base )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x3;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1), x2; "%n + " \\\n\
            load_inst v16, (x1), x2; \\\n\
        )",file=f)

    print("#define TEST_VSSE_OP_130( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x30, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x30), x2; \\\n\
            load_inst v16, (x30), x2 ;  \\\n\
        )",file=f)

    print("#define TEST_VSSE_OP_129( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x29, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x29), x2; \\\n\
            load_inst v16, (x29), x2 ;  \\\n\
        )",file=f)
    print("#define TEST_VSSE_OP_rd31( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v31, result, \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x3, result; \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v31, x3; \\\n\
            VSET_VSEW \\\n\
            store_inst v31, (x1), x2; \\\n\
            load_inst v1, (x1), x2;  \\\n\
        )",file=f)

def generate_macros_vsuxei(f):
    for n in range(1,30):
        print("#define TEST_VSXEI_OP_1%d( testnum, load_inst, store_inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x30, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x30);    \\\n\
            li  x31, result; \\\n\
            vmv.v.x v8, x31; \\\n\
            store_inst v8, (x%d), v24;"%n + " \\\n\
            load_inst v16, (x%d), v24;"%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSXEI_OP_rd%d( testnum, load_inst, store_inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x1, base_data;   \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x3, result; \\\n\
            vmv.v.x v%d, x3; "%n + "\\\n\
            store_inst v%d, (x1), v24;"%n + " \\\n\
            load_inst v16, (x1), v24; \\\n\
        )",file=f)

    print("#define TEST_VSXEI_OP_130( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x30, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x31, result; \\\n\
            vmv.v.x v8, x31; \\\n\
            store_inst v8, (x30), v24; \\\n\
            load_inst v16, (x30), v24; \\\n\
        )",file=f)
    print("#define TEST_VSXEI_OP_131( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x31, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x3, result; \\\n\
            vmv.v.x v8, x3; \\\n\
            store_inst v8, (x31), v24; \\\n\
            load_inst v16, (x31), v24; \\\n\
        )",file=f)
    print("#define TEST_VSXEI_OP_rd31( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v31, result, \\\n\
            la  x1, base_data;   \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v2, (x6);    \\\n\
            li  x3, result; \\\n\
            vmv.v.x v31, x3; \\\n\
            store_inst v31, (x1), v2; \\\n\
            load_inst v14, (x1), v2; \\\n\
        )",file=f)

def generate_macros_vsseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    generate_vlseg3_macro(f,emul)
    generate_vsseg3_macro(f,emul)
    for n in range(1,30):
        print("#define TEST_VSSEG1_OP_1%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li x30, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.x v8, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d); "%n + "\\\n\
            load_inst v16, (x%d); "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSSEG1_OP_rd%d( testnum, load_inst, store_inst, eew, result, base )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x1, base;  \\\n\
            li x7, MASK_EEW(result, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.x v%d, x7;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1); "%n + " \\\n\
            load_inst v16, (x1); \\\n\
        )",file=f)

    print("#define TEST_VSSEG1_OP_130( testnum, load_inst, store_inst, eew, result, base ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x30, base;  \\\n\
            li x7, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.x v8, x7; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x30); \\\n\
            load_inst v16, (x30);  \\\n\
        )",file=f)

def generate_macros_vsuxseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    generate_vlseg3_macro(f, lmul)
    print("#define TEST_VSXSEG3_OP( testnum, load_inst, store_inst, index_eew, result1, result2, result3, base_data, base_index ) \\\n\
        TEST_CASE_VLSEG3( testnum, v8, __riscv_vsew, result1, result2, result3,  \\\n\
            la  x1, base_data; \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6); \\\n\
            li x7, MASK_VSEW(result1); \\\n\
            li x8, MASK_VSEW(result2); \\\n\
            li x9, MASK_VSEW(result3); \\\n\
            vsetivli x31, 1, __e_riscv_vsew, m1, tu, mu; \\\n\
            vmv.v.x v8, x7; \\\n\
            vmv.v.x v%d, x8; "%(8+lmul) + "\\\n\
            vmv.v.x v%d, x9; "%(8+lmul*2) + "\\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x1), v24; \\\n\
            vsetivli x31, 1, __e_riscv_vsew, m1, tu, mu; \\\n\
            vmv.v.i v8, 0; \\\n\
            vmv.v.i v%d, 0; "%(8+lmul) + " \\\n\
            vmv.v.i v%d, 0; "%(8+lmul*2) + " \\\n\
            VSET_VSEW \\\n\
            load_inst v8, (x1), v24; \\\n\
        )", file=f)
    for n in range(1,30):
        print("#define TEST_VSXSEG1_OP_1%d( testnum, load_inst, store_inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base_data; "%n + " \\\n\
            la  x30, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x30);    \\\n\
            li  x31, MASK_VSEW(result); \\\n\
            vmv.v.x v8, x31; \\\n\
            store_inst v8, (x%d), v24;"%n + " \\\n\
            load_inst v16, (x%d), v24;"%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSXSEG1_OP_rd%d( testnum, load_inst, store_inst, index_eew, result, base_data, base_index )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x1, base_data;   \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x3, MASK_VSEW(result); \\\n\
            vmv.v.x v%d, x3; "%n + "\\\n\
            store_inst v%d, (x1), v24;"%n + " \\\n\
            load_inst v16, (x1), v24; \\\n\
        )",file=f)

    print("#define TEST_VSXSEG1_OP_130( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x30, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x31, MASK_VSEW(result); \\\n\
            vmv.v.x v8, x31; \\\n\
            store_inst v8, (x30), v24; \\\n\
            load_inst v16, (x30), v24; \\\n\
        )",file=f)
    print("#define TEST_VSXSEG1_OP_131( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x31, base_data;  \\\n\
            la  x6, base_index; \\\n\
            MK_VLE_INST(index_eew) v24, (x6);    \\\n\
            li  x3, MASK_VSEW(result); \\\n\
            vmv.v.x v8, x3; \\\n\
            store_inst v8, (x31), v24; \\\n\
            load_inst v16, (x31), v24; \\\n\
        )",file=f)

def generate_macros_vssseg(f, lmul, vsew, eew):
    emul = eew / vsew * lmul
    emul = 1 if emul < 1 else int(emul)
    lmul = 1 if lmul < 1 else int(lmul)
    generate_vlseg3_macro(f, emul)
    print("#define TEST_VSSSEG3_OP( testnum, load_inst, store_inst, eew, result1, result2, result3, stride, base ) \\\n\
        TEST_CASE_VLSEG3( testnum, v8, eew, result1, result2, result3,  \\\n\
            la  x1, base; \\\n\
            li  x2, stride; \\\n\
            li x7, MASK_EEW(result1, eew); \\\n\
            li x8, MASK_EEW(result2, eew); \\\n\
            li x9, MASK_EEW(result3, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.x v8, x7; \\\n\
            vmv.v.x v%d, x8;"%(8+emul) + " \\\n\
            vmv.v.x v%d, x9;"%(8+emul*2) + " \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x1), x2; \\\n\
            vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \\\n\
            vmv.v.i v8, 0; \\\n\
            vmv.v.i v%d, 0;"%(8+emul) + " \\\n\
            vmv.v.i v%d, 0;"%(8+emul*2) + " \\\n\
            VSET_VSEW \\\n\
            load_inst v8, (x1), x2; \\\n\
        )", file=f)
    for n in range(1,29):
        print("#define TEST_VSSSEG1_OP_1%d( testnum, load_inst, store_inst, eew, result, stride, base  )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x%d, base; "%n + " \\\n\
            li  x29, stride; \\\n\
            li  x30, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x30; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x%d), x29; "%n + "\\\n\
            load_inst v16, (x%d), x29; "%n + " \\\n\
        )",file=f)

    for n in range(1,31):
        print("#define TEST_VSSSEG1_OP_rd%d( testnum, load_inst, store_inst, eew, result, stride, base  )"%n + " \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x1, base;  \\\n\
            li  x2, stride; \\\n\
            li  x7, MASK_EEW(result, eew); \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v%d, x7;  "%n + "\\\n\
            VSET_VSEW \\\n\
            store_inst v%d, (x1), x2; "%n + " \\\n\
            load_inst v16, (x1), x2; \\\n\
        )",file=f)

    print("#define TEST_VSSSEG1_OP_130( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x30, base;  \\\n\
            li  x2, stride; \\\n\
            li  x7, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x7; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x30), x2; \\\n\
            load_inst v16, (x30), x2;  \\\n\
        )",file=f)
    print("#define TEST_VSSSEG1_OP_129( testnum, load_inst, store_inst, eew, result, stride, base ) \\\n\
        TEST_CASE( testnum, v16, result, \\\n\
            la  x29, base;  \\\n\
            li  x2, stride; \\\n\
            li  x7, MASK_EEW(result, eew);  \\\n\
            vsetivli x31, 1, MK_EEW(eew), tu, mu; \\\n\
            vmv.v.x v8, x7; \\\n\
            VSET_VSEW \\\n\
            store_inst v8, (x29), x2; \\\n\
            load_inst v16, (x29), x2;  \\\n\
        )",file=f)
 