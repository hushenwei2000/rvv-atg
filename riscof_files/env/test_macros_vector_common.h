// Compare only low VSEW-bits of v14 and correctval
#define VMVXS_AND_MASK_VSEW( targetreg, testreg ) \
    vmv.x.s targetreg, testreg; \
    li x2, VSEW_MASK_BITS; \
    and targetreg, targetreg, x2; \

#define VMVXS_AND_MASK_EEW( targetreg, testreg, eew ) \
    vmv.x.s targetreg, testreg; \
    li x2, MASK_BITS(eew); \
    and targetreg, targetreg, x2; \

#define VMVXS_AND_MASK_DOUBLEVSEW( targetreg, testreg ) \
    vmv.x.s targetreg, testreg; \
    li x2, DOUBLE_VSEW_MASK_BITS; \
    and targetreg, targetreg, x2; \

#define TEST_CASE( testnum, testreg, code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_W( testnum, testreg, code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_MASK( testnum, testreg,  code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    vpopc.m x14, testreg; \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_MASK_4VL( testnum, testreg,  code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VSET_VSEW_4AVL \
    vpopc.m x14, testreg; \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_SCALAR_SETVSEW_AFTER( testnum, testreg,  code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VSET_VSEW \
    RVTEST_SIGUPD(x20, testreg);


#define TEST_CASE_LOAD( testnum, testreg, eew, correctval1, correctval2, code... ) \
test_ ## testnum: \
    code; \
    li x7, MASK_EEW(correctval1, eew); \
    li TESTNUM, testnum; \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    VMVXS_AND_MASK_EEW( x14, testreg, eew ) \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    vsetivli x31, 4, MK_EEW(eew), tu, mu; \
    vslidedown.vi v16, testreg, 1; \
    VSET_VSEW \
    li x7, MASK_EEW(correctval2, eew); \
    li TESTNUM, testnum; \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    VMVXS_AND_MASK_EEW( x14, v16, eew ) \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x24, testreg);


// For simplicity, all vlre/vsre test use 2 fields
#define TEST_CASE_VLRE( testnum, eew, correctval1, correctval2, code... ) \
test_ ## testnum: \
    code; \
    li x7, MASK_EEW(correctval1, eew); \
    li x8, MASK_EEW(correctval2, eew); \
    li TESTNUM, testnum; \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    VMVXS_AND_MASK_EEW( x14, v16, eew ) \
    VMVXS_AND_MASK_EEW( x15, v17, eew ) \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, v16); \
    VECTOR_RVTEST_SIGUPD(x20, v17);

#define TEST_CASE_LOOP( testnum, testreg, code...) \
test_ ## testnum: \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    RVTEST_BASEUPD(x20) \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \

#define TEST_CASE_LOOP_W( testnum, testreg, code...) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW_4AVL \
    csrr x31, vstart; \
    csrr x30, vl; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    RVTEST_BASEUPD(x20) \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \
    VSET_VSEW_4AVL; 

#define TEST_CASE_LOOP_CONTINUE( testnum, testreg, code...) \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    RVTEST_BASEUPD(x20) \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \

// Then compare each element between `testreg` and v15, until `vl`
// vl should be set before calling `TEST_CASE_LOOP_VSLIDEUP()`
#define TEST_CASE_LOOP_VSLIDEUP( testnum, testreg, offset, code...) \
test_ ## testnum: \
    code; \
    li x29, offset; \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
    bge x31, x29, test_loop_vslide2_ ## testnum; \
test_loop_vslide1_ ## testnum: \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    blt x31, x29, test_loop_vslide1_ ## testnum; \
test_loop_vslide2_ ## testnum: \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    RVTEST_BASEUPD(x20) \
    vslidedown.vi testreg, testreg, 1; \
    addi x31, x31, 1; \
    blt x31, x30, test_loop_vslide2_ ## testnum; \

#define TEST_CASE_FP( testnum, testreg, val1, val2, code... ) \
test_ ## testnum: \
  li x7, 0; \
  vmv.v.x v14, x7; \
  li  TESTNUM, testnum; \
  la  a0, test_ ## testnum ## _data ;\
  code; \
  vfmv.f.s f3, testreg; \
  li a3, 1; \
  frflags a1; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
  .pushsection .data; \
  .align 2; \
  test_ ## testnum ## _data: \
  .word val1; \
  .word val2; \
  .popsection

#define TEST_CASE_LOOP_FP( testnum, testreg,  code...) \
test_ ## testnum: \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    li TESTNUM, testnum; \
    frflags x11; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
    RVTEST_BASEUPD(x20) \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \

#define TEST_CASE_LOOP_W_FP( testnum, testreg, code...) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW_4AVL \
    csrr x31, vstart; \
    csrr x30, vl; \
    frflags x11; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
    RVTEST_BASEUPD(x20) \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    bne x31, x30, 1b; \


// Use feq.d to compare correctval(f2) computed by fadd.d and answer(f3) computed by vfwadd
#define TEST_CASE_W_FP( testnum, testreg,  val1, val2, code... ) \
test_ ## testnum: \
  li x7, 0; \
  VSET_DOUBLE_VSEW \
  vmv.v.x v14, x7; \
  VSET_VSEW \
  li  TESTNUM, testnum; \
  la  a0, test_ ## testnum ## _data ;\
  code; \
  VSET_DOUBLE_VSEW \
  vfmv.f.s f3, testreg; \
  VSET_VSEW \
  li a3, 1; \
  frflags a1; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
  .pushsection .data; \
  .align 2; \
  test_ ## testnum ## _data: \
  .word val1; \
  .word val2; \
  .popsection

// Use feq.d to compare correctval(f2) computed by fadd.d and answer(f3) computed by vfwadd
#define TEST_CASE_WVWF_FP( testnum, testreg,  val1, val2, code... ) \
test_ ## testnum: \
  li x7, 0; \
  vmv.v.x v14, x7; \
  li  TESTNUM, testnum; \
  la  a0, test_ ## testnum ## _data ;\
  code; \
  VSET_DOUBLE_VSEW \
  vfmv.f.s f3, testreg; \
  VSET_VSEW \
  li a3, 1; \
  frflags a1; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
  .pushsection .data; \
  .align 2; \
  test_ ## testnum ## _data: \
  .dword val1; \
  .word val2; \
  .float 0; \
  .popsection


#define TEST_CASE_MASK_FP_4VL( testnum, testreg,  code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    VSET_VSEW_4AVL \
    vpopc.m x14, testreg; \
    VSET_VSEW \
    frflags a1; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \



#define TEST_VLSE_OP( testnum, inst, eew, result1, result2, stride, base ) \
  TEST_CASE_LOOP( testnum, v16,  \
    la  x1, base; \
    li  x2, stride; \
    inst v16, (x1), x2; \
    VSET_VSEW \
  )

#define TEST_VLXEI_OP( testnum, inst, index_eew, result1, result2, base_data, base_index ) \
  TEST_CASE_LOOP( testnum, v16, \
    la  x1, base_data; \
    la  x6, base_index; \
    vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \
    MK_VLE_INST(index_eew) v8, (x6); \
    VSET_VSEW_4AVL \
    inst v16, (x1), v8; \
    VSET_VSEW \
  )

#define TEST_VLE_OP( testnum, inst, eew, result1, result2, base ) \
  TEST_CASE_LOOP( testnum, v16,  \
    la  x1, base; \
    inst v16, (x1); \
    VSET_VSEW \
  )

#define TEST_VLEFF_OP( testnum, inst, eew, result1, result2, base ) \
  TEST_CASE_LOOP( testnum, v16, \
    la  x1, base; \
    inst v16, (x1); \
    csrr x30, vl; \
  )





#define TEST_VLRE2_OP( testnum, inst, eew, result1, result2, base ) \
  TEST_CASE_VLRE( testnum, eew, result1, result2,  \
    la  x1, base; \
    inst v16, (x1); \
  )

#define TEST_VLRE1_OP( testnum, inst, eew, base ) \
  TEST_CASE_LOOP( testnum, v16, \
    la  x1, base; \
    inst v16, (x1); \
  )



#define TEST_VSSE_OP( testnum, load_inst, store_inst, eew, result, stride, base ) \
  TEST_CASE_LOOP( testnum, v16, \
    la  x1, base; \
    li  x2, stride; \
    li  x3, result; \
    vmv.v.x v8, x3; \
    VSET_VSEW \
    store_inst v8, (x1), x2; \
    load_inst v16, (x1), x2; \
  )

#define TEST_VSE_OP( testnum, load_inst, store_inst, eew, result, base ) \
  TEST_CASE_LOOP( testnum, v16, \
    la  x1, base; \
    li  x3, result; \
    vmv.v.x v8, x3; \
    VSET_VSEW \
    store_inst v8, (x1); \
    load_inst v16, (x1); \
  )

#define TEST_VSXEI_OP( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \
  TEST_CASE_LOOP( testnum, v16,  \
    la  x1, base_data; \
    la  x6, base_index; \
    MK_VLE_INST(index_eew) v24, (x6); \
    li  x3, result; \
    vmv.v.x v8, x3; \
    store_inst v8, (x1), v24; \
    load_inst v16, (x1), v24; \
  )
#define TEST_VSRE2_OP( testnum, load_inst, store_inst, eew, result1, result2, base ) \
  TEST_CASE_VLRE( testnum, eew, result1, result2,  \
    la  x1, base; \
    li x7, MASK_EEW(result1, eew); \
    li x8, MASK_EEW(result2, eew); \
    vsetivli x31, 1, MK_EEW(eew), m1, tu, mu; \
    vmv.v.x v8, x7; \
    vmv.v.x v9, x8; \
    VSET_VSEW \
    store_inst v8, (x1); \
    load_inst v16, (x1); \
  )

#define TEST_VSRE1_OP( testnum, load_inst, store_inst, eew, result, base ) \
  TEST_CASE_LOOP( testnum, v16,  \
    la  x1, base; \
    li x7, MASK_EEW(result, eew); \
    vmv.v.x v8, x7; \
    VSET_VSEW \
    store_inst v8, (x1); \
    load_inst v16, (x1); \
  )


// For VF instruction that order of oprands is 'vd, rs1, vs2'(rs-vs), val1-rs1, val2-vs2
#define TEST_FP_VF_OP_RV( testnum, inst,  val1, val2 ) \
  TEST_CASE_FP( testnum, v24, val1, val2,     \
    flw f0, 0(a0); \
    flw f1, 4(a0); \
    vfmv.s.f v8, f0; \
    flw f2, 8(a0); \
    inst v24, f1, v8; \
  )


#define TEST_W_FP_VV_OP_NEGRESULT( testnum, inst,  val1, val2 ) \
  TEST_CASE_W_FP( testnum, v24,  val1, val2,     \
    flw f0, 0(a0); \
    flw f1, 4(a0); \
    vfmv.s.f v8, f0; \
    vfmv.s.f v16, f1; \
    fcvt.d.s f0, f0; \
    fcvt.d.s f1, f1; \
    fneg.d f2, f2; \
    inst v24, v8, v16; \
  )


#define TEST_W_FP_VF_OP_RV( testnum, inst,  val1, val2 ) \
  TEST_CASE_W_FP( testnum, v24, val1, val2,     \
    flw f0, 0(a0); \
    flw f1, 4(a0); \
    flw f4, 4(a0); \
    vfmv.s.f v8, f0; \
    fcvt.d.s f0, f0; \
    fcvt.d.s f4, f4; \
    inst v24, f1, v8; \
  )

#define TEST_W_FP_VF_OP_RV_NEGRESULT( testnum, inst,  val1, val2 ) \
  TEST_CASE_W_FP( testnum, v24,  val1, val2,     \
    flw f0, 0(a0); \
    flw f1, 4(a0); \
    flw f4, 4(a0); \
    vfmv.s.f v8, f0; \
    fcvt.d.s f0, f0; \
    fcvt.d.s f4, f4; \
    fneg.d f2, f2; \
    inst v24, f1, v8; \
  )


// For Widen-Floating instruction that order of oprands is 'vd(2*SEW), vs2(SEW), vs1(2*SEW)'
#define TEST_W_FP_WV_OP_DS( testnum, inst, val1, val2 ) \
  TEST_CASE_WVWF_FP( testnum, v24, val1, val2,  \
    fld f0, 0(a0); \
    flw f1, 8(a0); \
    flw f4, 8(a0); \
    VSET_DOUBLE_VSEW \
    vfmv.s.f v8, f0; \
    VSET_VSEW \
    vfmv.s.f v16, f1; \
    fcvt.d.s f4, f4; \
    inst v24, v16, v8; \
  )






//-----------------------------------------------------------------------
// Tests for Load Store instructions
//-----------------------------------------------------------------------


#define TEST_VMRL_OP( testnum, inst, sew,  src1_addr, src2_addr ) \
  TEST_CASE_MASK_4VL( testnum, v24,  \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    MK_VLE_INST(sew) v8, (x1); \
    la  x1, src2_addr; \
    MK_VLE_INST(sew) v16, (x1); \
    vmseq.vi v1, v8, 1; \
    vmseq.vi v2, v16, 1; \
    inst v24, v2, v1; \
    VSET_VSEW \
  )

#define TEST_VSFMB_OP( testnum, inst,  src1_addr ) \
  TEST_CASE_MASK_4VL( testnum, v16,  \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    vle8.v v8, (x1); \
    vmseq.vi v1, v8, 1; \
    inst v16, v1; \
    VSET_VSEW \
  )

#define TEST_VID_OP( testnum, inst, src1_addr ) \
  TEST_CASE_LOOP( testnum, v16, \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    vle8.v v8, (x1); \
    vmseq.vi v0, v8, 1; \
    inst v16, v0.t; \
  )


#define TEST_VMV_OP( testnum, result ) \
    li TESTNUM, testnum; \
    li x7, MASK_VSEW(result); \
    li x8, 0; \
    vmv.s.x v14, x7; \
    VMVXS_AND_MASK_VSEW( x8, v14 ) \
    RVTEST_SIGUPD(x20, x8);

#define TEST_VFMVS_OP( testnum, base ) \
    li TESTNUM, testnum; \
    la a0, base; \
    flw f7, 0(a0); \
    vfmv.s.f v14, f7; \
    vfmv.f.s f8, v14; \
    fcvt.w.s x8, f8; \
    fcvt.w.s x7, f7; \
    RVTEST_SIGUPD(x20, x8);

#define TEST_VFMVF_OP( testnum, base ) \
    li TESTNUM, testnum; \
    la a0, base; \
    flw f7, 0(a0); \
    vfmv.v.f v16, f7; \
    vfmv.f.s f8, v16; \
    fcvt.w.s x8, f8; \
    fcvt.w.s x7, f7; \
    RVTEST_SIGUPD(x20, x8);

