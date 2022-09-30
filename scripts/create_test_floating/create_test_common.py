def valid_aligned_regs(reg):
    i = reg // 8
    if i == 0 or i == 3: return 8, 16
    elif i == 1: return 16, 24
    else: return 24, 8


def generate_macros(f, vsew, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    if vsew == 32:
        for n in range(1,32):
            if n % lmul != 0: continue
            rs2, rd = valid_aligned_regs(n)
            print("#define TEST_FP_VV_OP_1%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, \\\n\
                flw f0, 0(a0); \\\n\
                flw f1, 4(a0); \\\n\
                vfmv.s.f v%d, f0; \\\n\
                vfmv.s.f v%d, f1; \\\n\
                flw f2, 8(a0); \\\n\
                inst v%d, v%d, v%d; \\\n\
            )"%(n, rd, rs2, n, rd, rs2, n),file=f)
        for n in range(1,32):
            if n % lmul != 0: continue
            rs1, rs2 = valid_aligned_regs(n)
            print("#define TEST_FP_VV_OP_rd%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, \\\n\
                flw f0, 0(a0); \\\n\
                flw f1, 4(a0); \\\n\
                vfmv.s.f v%d, f0; \\\n\
                vfmv.s.f v%d, f1; \\\n\
                flw f2, 8(a0); \\\n\
                inst v%d, v%d, v%d; \\\n\
            )"%(n, n, rs2, rs1, n, rs2, rs1),file=f)
    elif vsew == 64:
        for n in range(1,32):
            if n % lmul != 0: continue
            rs2, rd = valid_aligned_regs(n)
            print("#define TEST_FP_VV_OP_1%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, \\\n\
                fld f0, 0(a0); \\\n\
                fld f1, 8(a0); \\\n\
                vfmv.s.f v%d, f0; \\\n\
                vfmv.s.f v%d, f1; \\\n\
                fld f2, 16(a0); \\\n\
                inst v%d, v%d, v%d; \\\n\
            )"%(n, rd, rs2, n, rd, rs2, n),file=f)
        for n in range(1,32):
            if n % lmul != 0: continue
            rs1, rs2 = valid_aligned_regs(n)
            print("#define TEST_FP_VV_OP_rd%d( testnum, inst, flags, result, val1, val2 ) \\\n\
            TEST_CASE_FP( testnum, v%d, flags, result, val1, val2, \\\n\
                fld f0, 0(a0); \\\n\
                fld f1, 8(a0); \\\n\
                vfmv.s.f v%d, f0; \\\n\
                vfmv.s.f v%d, f1; \\\n\
                fld f2, 16(a0); \\\n\
                inst v%d, v%d, v%d; \\\n\
            )"%(n, n, rs2, rs1, n, rs2, rs1),file=f)


def generate_macros_widen(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n % lmul != 0: continue
        rs2, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_1%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, rd, rs2, n, rd, rs2, n),file=f)
    for n in range(1,32):
        if n % (2*lmul) != 0: continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_rd%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, n, rs2, rs1, n, rs2, rs1),file=f)


def generate_macros_widen_rs2(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n % lmul != 0: continue
        rs1, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_2%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, rd, rs1, n, rd, rd, rs1, n),file=f)
    for n in range(1,32):
        if n % (2*lmul) != 0: continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_rd%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, n, rs1, rs2, n, n, rs1, rs2),file=f)


def generate_macros_widen_rs2_neg(f, lmul):
    lmul = 1 if lmul < 1 else int(lmul)
    for n in range(1,32):
        if n % lmul != 0: continue
        rs1, rd = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_NEGRESULT_2%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            fneg.d f2, f2; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, rd, rs1, n, rd, rd, rs1, n),file=f)
    for n in range(1,32):
        if n % (2*lmul) != 0: continue
        rs1, rs2 = valid_aligned_regs(n)
        print("#define TEST_W_FP_VV_OP_NEGRESULT_rd%d( testnum, inst, finst, flags, val1, val2 ) \\\n\
        TEST_CASE_W_FP( testnum, v%d, flags, val1, val2, \\\n\
            flw f0, 0(a0); \\\n\
            flw f1, 4(a0); \\\n\
            vfmv.s.f v%d, f0; \\\n\
            vfmv.s.f v%d, f1; \\\n\
            fcvt.d.s f0, f0; \\\n\
            fcvt.d.s f1, f1; \\\n\
            finst f2, f0, f1; \\\n\
            fneg.d f2, f2; \\\n\
            VSET_VSEW_4AVL \\\n\
            vmv.v.i v%d, 0; \\\n\
            VSET_VSEW \\\n\
            inst v%d, v%d, v%d; \\\n\
        )"%(n, n, rs1, rs2, n, n, rs1, rs2),file=f)