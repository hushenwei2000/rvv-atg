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
    generate_vlseg3_macro(f, 1)
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
  