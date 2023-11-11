#include "test_macros.h"
// See LICENSE for license details.

#ifndef __TEST_MACROS_VECTOR_H
#define __TEST_MACROS_VECTOR_H

//-----------------------------------------------------------------------
// Helper macros
//-----------------------------------------------------------------------

#define TESTNUM gp
#define RVTEST_VECTOR_ENABLE                                            \
  li a0, (MSTATUS_VS & (MSTATUS_VS >> 1)) |                             \
         (MSTATUS_FS & (MSTATUS_FS >> 1));                              \
  csrs mstatus, a0;                                                     \
  csrwi fcsr, 0;                                                        \
  csrwi vcsr, 0;
#define VECTOR_RVTEST_SIGUPD(basereg, vreg) vmv.x.s x1, vreg; RVTEST_SIGUPD(basereg, x1);
#define VECTOR_RVTEST_SIGUPD_F(basereg, vreg, flagreg) vfmv.f.s f1, vreg; RVTEST_SIGUPD_F(basereg, f1, flagreg);

#define RVTEST_VSET RVTEST_VECTOR_ENABLE; vsetivli x31, 1, e64, tu, mu;
#define __riscv_vsew 64
#define __e_riscv_vsew e64
#define __riscv_double_vsew 128
#define VSEW_MASK_BITS 0xffffffffffffffff
#define DOUBLE_VSEW_MASK_BITS 0xffffffffffffffff
#define VSET_VSEW vsetivli x31, 1, e64, tu, mu;
#define VSET_VSEW_4AVL vsetvli x31, x0, e64, tu, mu;
#define VSET_DOUBLE_VSEW vsetivli x31, 1, e64, tu, mu;

#define MASK_VSEW(x)        ((x) & ((1 << (__riscv_vsew - 1) << 1) - 1))
#define MASK_EEW(x, eew)    ((x) & ((1 << (eew - 1) << 1) - 1))
#define MASK_DOUBLE_VSEW(x) ((x) & ((1 << ((__riscv_vsew * 2) - 1) << 1) - 1))
#define MASK_HALF_VSEW(x)   ((x) & ((1 << ((__riscv_vsew / 2) - 1) << 1) - 1))
#define MASK_QUART_VSEW(x)  ((x) & ((1 << ((__riscv_vsew / 4) - 1) << 1) - 1))
#define MASK_EIGHTH_VSEW(x) ((x) & ((1 << ((__riscv_vsew / 8) - 1) << 1) - 1))
#define MASK_BITS(eew)      ((-1 << (64 - eew)) >> (64 - eew))
#define MK_EEW(eew_num) e##eew_num
#define MK_VLE_INST(eew_num) vle##eew_num.v
#define MK_VSE_INST(eew_num) vse##eew_num.v

#define SEXT_HALF_TO_VSEW(x)   ((x) | (-(((x) >> ((__riscv_vsew / 2) - 1)) & 1) << ((__riscv_vsew / 2) - 1)))
#define SEXT_QUART_TO_VSEW(x)  ((x) | (-(((x) >> ((__riscv_vsew / 4) - 1)) & 1) << ((__riscv_vsew / 4) - 1)))
#define SEXT_EIGHTH_TO_VSEW(x) ((x) | (-(((x) >> ((__riscv_vsew / 8) - 1)) & 1) << ((__riscv_vsew / 8) - 1)))
#define SEXT_DOUBLE_VSEW(x)    ((x) | (-(((x) >> ((__riscv_vsew * 2) - 1)) & 1) << (__riscv_vsew - 1)))
#define ZEXT_VSEW(x)           ((x) | (x) >> (__riscv_vsew - 1))
#define ZEXT_DOUBLE_VSEW(x)    ((x) | (x) >> ((__riscv_vsew * 2) - 1))

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

#define TEST_CASE( testnum, testreg, correctval, code... ) \
test_ ## testnum: \
    code; \
    li x7, MASK_VSEW(correctval); \
    li TESTNUM, testnum; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_W( testnum, testreg, correctval, code... ) \
test_ ## testnum: \
    code; \
    li x7, MASK_DOUBLE_VSEW(correctval); \
    li TESTNUM, testnum; \
    VSET_DOUBLE_VSEW \
    VMVXS_AND_MASK_DOUBLEVSEW(x14, testreg) \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_MASK( testnum, testreg, correctval, code... ) \
test_ ## testnum: \
    code; \
    li x7, correctval; \
    li TESTNUM, testnum; \
    vpopc.m x14, testreg; \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_MASK_4VL( testnum, testreg, correctval, code... ) \
test_ ## testnum: \
    code; \
    li x7, correctval; \
    li TESTNUM, testnum; \
    VSET_VSEW_4AVL \
    vpopc.m x14, testreg; \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_SCALAR_SETVSEW_AFTER( testnum, testreg, correctval, code... ) \
test_ ## testnum: \
    code; \
    li x7, correctval; \
    li TESTNUM, testnum; \
    VSET_VSEW \
    RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_AVG_VV( testnum, inst, testvs1, testreg, correctval00, correctval01, correctval10, correctval11, code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    csrwi vxrm, 0; \
    inst testreg, v8, testvs1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval00); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 1; \
    inst testreg, v8, testvs1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval01); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 2; \
    inst testreg, v8, testvs1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval10); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 3; \
    inst testreg, v8, testvs1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval11); \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_AVG_VX( testnum, inst, testreg, correctval00, correctval01, correctval10, correctval11, code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    csrwi vxrm, 0; \
    inst testreg, v8, x1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval00); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 1; \
    inst testreg, v8, x1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval01); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 2; \
    inst testreg, v8, x1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval10); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 3; \
    inst testreg, v8, x1; \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval11); \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

#define TEST_CASE_AVG_VI( testnum, inst, testreg, correctval00, correctval01, correctval10, correctval11, val2, code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    csrwi vxrm, 0; \
    inst v14, v2, (val2); \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval00); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 1; \
    inst v14, v2, (val2); \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval01); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 2; \
    inst v14, v2, (val2); \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval10); \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    csrwi vxrm, 3; \
    inst v14, v2, (val2); \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    li x7, MASK_VSEW(correctval11); \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

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
    VECTOR_RVTEST_SIGUPD(x20, testreg);



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

// Load from `correctval_addr_reg` to v15 as correctval_vec, compare each element with `testreg`; vl should be set before calling `TEST_CASE_LOOP()`
#define TEST_CASE_LOOP( testnum, testreg, correctval_addr_reg, code...) \
test_ ## testnum: \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    la x7, correctval_addr_reg; \
    vle64.v v8, (x7); \
    li TESTNUM, testnum; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VMVXS_AND_MASK_VSEW( x7, v8 ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    vslidedown.vi v8, v8, 1; \
    bne x31, x30, 1b; \
    VSET_VSEW; 

#define TEST_CASE_LOOP_CONTINUE( testnum, testreg, correctval_addr_reg, code...) \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    vle64.v v1, (correctval_addr_reg); \
    li TESTNUM, testnum; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VMVXS_AND_MASK_VSEW( x7, v1 ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    vslidedown.vi v1, v1, 1; \
    bne x31, x30, 1b; \
    VSET_VSEW; 

// Load from `correctval_addr_reg` to v15 as correctval_vec, read vstart to x31, add x31 until reach `offset`;
// Then compare each element between `testreg` and v15, until `vl`
// vl should be set before calling `TEST_CASE_LOOP_VSLIDEUP()`
#define TEST_CASE_LOOP_VSLIDEUP( testnum, testreg, correctval_addr_reg, offset, code...) \
test_ ## testnum: \
    code; \
    li x29, offset; \
    csrr x31, vstart; \
    csrr x30, vl; \
    vle32.v v15, (correctval_addr_reg); \
    li TESTNUM, testnum; \
    bge x31, x29, test_loop_vslide2_ ## testnum; \
test_loop_vslide1_ ## testnum: \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    blt x31, x29, test_loop_vslide1_ ## testnum; \
test_loop_vslide2_ ## testnum: \
    VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VMVXS_AND_MASK_VSEW( x7, v15 ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    vslidedown.vi testreg, testreg, 1; \
    vslidedown.vi v15, v15, 1; \
    addi x31, x31, 1; \
    blt x31, x30, test_loop_vslide2_ ## testnum; \
    VSET_VSEW; 

#define TEST_CASE_LOOP_64( testnum, testreg, correctval_addr_reg, code...) \
test_ ## testnum: \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    vle64.v v15, (correctval_addr_reg); \
    li TESTNUM, testnum; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VMVXS_AND_MASK_VSEW( x7, v15 ) \
    VECTOR_RVTEST_SIGUPD(x20, testreg); \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    vslidedown.vi v15, v15, 1; \
    bne x31, x30, 1b; \
    VSET_VSEW; 

#define TEST_CASE_FP( testnum, testreg, flags, result, val1, val2, code... ) \
test_ ## testnum: \
  li x7, 0; \
  vmv.v.x v14, x7; \
  li  TESTNUM, testnum; \
  la  a0, test_ ## testnum ## _data ;\
  code; \
  vfmv.f.s f3, testreg; \
  feq.d a0, f2, f3; \
  li a3, 1; \
  frflags a1; \
  li a2, flags; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
  .pushsection .data; \
  .align 2; \
  test_ ## testnum ## _data: \
  .dword val1; \
  .dword val2; \
  .dword result; \
  .popsection

#define TEST_CASE_LOOP_FP( testnum, testreg, fflag, correctval_addr_reg, correctval_reg, code...) \
test_ ## testnum: \
    code; \
    csrr x31, vstart; \
    csrr x30, vl; \
    la x7, correctval_addr_reg; \
    vle64.v correctval_reg, (x7); \
    li TESTNUM, testnum; \
    frflags x11; \
    li x12, fflag; \
1:  VMVXS_AND_MASK_VSEW( x14, testreg ) \
    VMVXS_AND_MASK_VSEW( x7, correctval_reg ) \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
    addi x31, x31, 1; \
    vslidedown.vi testreg, testreg, 1; \
    vslidedown.vi correctval_reg, correctval_reg, 1; \
    bne x31, x30, 1b; \
    VSET_VSEW; 

// Use feq.d to compare correctval(f2) computed by fadd.d and answer(f3) computed by vfwadd
#define TEST_CASE_W_FP( testnum, testreg, flags, val1, val2, code... ) \
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
  feq.d a0, f2, f3; \
  li a3, 1; \
  frflags a1; \
  li a2, flags; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
  .pushsection .data; \
  .align 2; \
  test_ ## testnum ## _data: \
  .dword val1; \
  .dword val2; \
  .popsection


// Use feq.d to compare correctval(f2) computed by fadd.d and answer(f3) computed by vfwadd
#define TEST_CASE_WVWF_FP( testnum, testreg, flags, val1, val2, code... ) \
test_ ## testnum: \
  li x7, 0; \
  vmv.v.x v14, x7; \
  li  TESTNUM, testnum; \
  la  a0, test_ ## testnum ## _data ;\
  code; \
  VSET_DOUBLE_VSEW \
  vfmv.f.s f3, testreg; \
  VSET_VSEW \
  feq.d a0, f2, f3; \
  li a3, 1; \
  frflags a1; \
  li a2, flags; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \
  .pushsection .data; \
  .align 2; \
  test_ ## testnum ## _data: \
  .dword val1; \
  .dword val2; \
  .float 0; \
  .popsection


#define TEST_CASE_MASK_FP_4VL( testnum, testreg, flags, correctval, code... ) \
test_ ## testnum: \
    code; \
    li TESTNUM, testnum; \
    li x7, correctval; \
    VSET_VSEW_4AVL \
    vpopc.m x14, testreg; \
    VSET_VSEW \
    frflags a1; \
    li a2, flags; \
  VECTOR_RVTEST_SIGUPD_F(x20, testreg, a1); \


//-----------------------------------------------------------------------
// Tests for instructions with vector-vector operand
//-----------------------------------------------------------------------







#define TEST_VLSE_OP( testnum, inst, eew, result1, result2, stride, base ) \
  TEST_CASE_LOAD( testnum, v14, eew, result1, result2, \
    la  x1, base; \
    li  x2, stride; \
    vsetivli x31, 4, MK_EEW(eew), tu, mu; \
    inst v14, (x1), x2; \
    VSET_VSEW \
  )

#define TEST_VLXEI_OP( testnum, inst, index_eew, result1, result2, base_data, base_index ) \
  TEST_CASE_LOAD( testnum, v16, __riscv_vsew, result1, result2, \
    la  x1, base_data; \
    la  x6, base_index; \
    vsetvli x31, x0, MK_EEW(index_eew), tu, mu; \
    MK_VLE_INST(index_eew) v8, (x6); \
    VSET_VSEW_4AVL \
    inst v16, (x1), v8; \
    VSET_VSEW \
  )

#define TEST_VLE_OP( testnum, inst, eew, result1, result2, base ) \
  TEST_CASE_LOAD( testnum, v14, eew, result1, result2, \
    la  x1, base; \
    vsetivli x31, 4, MK_EEW(eew), tu, mu; \
    inst v14, (x1); \
    VSET_VSEW \
  )

#define TEST_VLEFF_OP( testnum, inst, eew, result1, result2, base ) \
  TEST_CASE_LOAD( testnum, v14, eew, result1, result2, \
    la  x1, base; \
    vsetivli x31, 4, MK_EEW(eew), tu, mu; \
    inst v14, (x1); \
    csrr x30, vl; \
    RVTEST_SIGUPD(x20, x31); \
  )

#define TEST_VLSEG3_OP( testnum, inst, eew, result1, result2, result3, base ) \
  TEST_CASE_VLSEG3( testnum, v8, eew, result1, result2, result3,  \
    la  x1, base; \
    inst v8, (x1); \
  )

#define TEST_VLSEG1_OP( testnum, inst, eew, result, base ) \
  TEST_CASE( testnum, v8, result,  \
    la  x1, base; \
    inst v8, (x1); \
  )

#define TEST_VLRE2_OP( testnum, inst, eew, result1, result2, base ) \
  TEST_CASE_VLRE( testnum, eew, result1, result2,  \
    la  x1, base; \
    inst v16, (x1); \
  )

#define TEST_VLRE1_OP( testnum, inst, eew, result, base ) \
  TEST_CASE( testnum, v16, result,  \
    la  x1, base; \
    inst v16, (x1); \
  )

#define TEST_VLSSEG3_OP( testnum, inst, eew, result1, result2, result3, stride, base ) \
  TEST_CASE_VLSEG3( testnum, v8, eew, result1, result2, result3,  \
    la  x1, base; \
    li  x2, stride; \
    inst v8, (x1), x2; \
  )

#define TEST_VLSSEG1_OP( testnum, inst, eew, result, stride, base ) \
  TEST_CASE( testnum, v8, result,  \
    la  x1, base; \
    li  x2, stride; \
    inst v8, (x1), x2; \
  )

#define TEST_VLXSEG3_OP( testnum, inst, index_eew, result1, result2, result3, base_data, base_index ) \
  TEST_CASE_VLSEG3( testnum, v8, __riscv_vsew, result1, result2, result3,  \
    la  x1, base_data; \
    la  x6, base_index; \
    MK_VLE_INST(index_eew) v16, (x6); \
    inst v8, (x1), v16; \
  )

#define TEST_VLXSEG1_OP( testnum, inst, index_eew, result, base_data, base_index ) \
  TEST_CASE( testnum, v16, result,  \
    la  x1, base_data; \
    la  x6, base_index; \
    MK_VLE_INST(index_eew) v8, (x6); \
    inst v16, (x1), v8; \
  )




#define TEST_VSSEG1_OP( testnum, load_inst, store_inst, eew, result, base ) \
  TEST_CASE( testnum, v16, result,  \
    la  x1, base; \
    li x7, MASK_EEW(result, eew); \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    vmv.v.x v8, x7; \
    VSET_VSEW \
    store_inst v8, (x1); \
    load_inst v16, (x1); \
  )

// #define TEST_VSSSEG3_OP( testnum, load_inst, store_inst, eew, result1, result2, result3, stride, base ) \
//   TEST_CASE_VLSEG3( testnum, v8, eew, result1, result2, result3,  \
//     la  x1, base; \
//     li  x2, stride; \
//     li x7, MASK_EEW(result1, eew); \
//     li x8, MASK_EEW(result2, eew); \
//     li x9, MASK_EEW(result3, eew); \
//     vsetivli x31, 1, MK_EEW(eew), tu, mu; \
//     vmv.v.x v1, x7; \
//     vmv.v.x v2, x8; \
//     vmv.v.x v3, x9; \
//     VSET_VSEW \
//     store_inst v1, (x1), x2; \
//     load_inst v8, (x1), x2; \
//   )

#define TEST_VSSSEG1_OP( testnum, load_inst, store_inst, eew, result, stride, base ) \
  TEST_CASE( testnum, v16, result,  \
    la  x1, base; \
    li  x2, stride; \
    li x7, MASK_EEW(result, eew); \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    vmv.v.x v8, x7; \
    VSET_VSEW \
    store_inst v8, (x1), x2; \
    load_inst v16, (x1), x2; \
  )

// #define TEST_VSXSEG3_OP( testnum, load_inst, store_inst, index_eew, result1, result2, result3, base_data, base_index ) \
//   TEST_CASE_VLSEG3( testnum, v8, __riscv_vsew, result1, result2, result3,  \
//     la  x1, base_data; \
//     la  x6, base_index; \
//     MK_VLE_INST(index_eew) v5, (x6); \
//     li x7, MASK_VSEW(result1); \
//     li x8, MASK_VSEW(result2); \
//     li x9, MASK_VSEW(result3); \
//     vmv.v.x v1, x7; \
//     vmv.v.x v2, x8; \
//     vmv.v.x v3, x9; \
//     store_inst v1, (x1), v5; \
//     load_inst v8, (x1), v5; \
//   )

#define TEST_VSXSEG1_OP( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \
  TEST_CASE( testnum, v16, result,  \
    la  x1, base_data; \
    la  x6, base_index; \
    MK_VLE_INST(index_eew) v24, (x6); \
    li x7, MASK_VSEW(result); \
    vmv.v.x v8, x7; \
    store_inst v8, (x1), v24; \
    load_inst v16, (x1), v24; \
  )

#define TEST_VSSE_OP( testnum, load_inst, store_inst, eew, result, stride, base ) \
  TEST_CASE( testnum, v16, result, \
    la  x1, base; \
    li  x2, stride; \
    li  x3, result; \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    vmv.v.x v8, x3; \
    VSET_VSEW \
    store_inst v8, (x1), x2; \
    load_inst v16, (x1), x2; \
  )

#define TEST_VSE_OP( testnum, load_inst, store_inst, eew, result, base ) \
  TEST_CASE( testnum, v16, result, \
    la  x1, base; \
    li  x3, result; \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    vmv.v.x v8, x3; \
    VSET_VSEW \
    store_inst v8, (x1); \
    load_inst v16, (x1); \
  )

#define TEST_VSXEI_OP( testnum, load_inst, store_inst, index_eew, result, base_data, base_index ) \
  TEST_CASE( testnum, v16, result, \
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
  TEST_CASE( testnum, v16, result,  \
    la  x1, base; \
    li x7, MASK_EEW(result, eew); \
    vsetivli x31, 1, MK_EEW(eew), tu, mu; \
    vmv.v.x v8, x7; \
    VSET_VSEW \
    store_inst v8, (x1); \
    load_inst v16, (x1); \
  )




// For VF instruction that order of oprands is 'vd, rs1, vs2'(rs-vs), val1-rs1, val2-vs2
#define TEST_FP_VF_OP_RV( testnum, inst, flags, result, val1, val2 ) \
  TEST_CASE_FP( testnum, v14, flags, result, val1, val2,     \
    fld f0, 0(a0); \
    fld f1, 8(a0); \
    vfmv.s.f v1, f0; \
    fld f2, 16(a0); \
    inst v14, f1, v1; \
  )



#define TEST_W_FP_VV_OP_NEGRESULT( testnum, inst, finst, flags, val1, val2 ) \
  TEST_CASE_W_FP( testnum, v14, flags, val1, val2,     \
    fld f0, 0(a0); \
    fld f1, 8(a0); \
    vfmv.s.f v1, f0; \
    vfmv.s.f v2, f1; \
    fcvt.d.s f0, f0; \
    fcvt.d.s f1, f1; \
    finst f2, f0, f1; \
    fneg.d f2, f2; \
    inst v14, v1, v2; \
  )


#define TEST_W_FP_VF_OP_RV( testnum, inst, finst, flags, val1, val2 ) \
  TEST_CASE_W_FP( testnum, v14, flags, val1, val2,     \
    fld f0, 0(a0); \
    fld f1, 8(a0); \
    fld f4, 8(a0); \
    vfmv.s.f v1, f0; \
    fcvt.d.s f0, f0; \
    fcvt.d.s f4, f4; \
    finst f2, f0, f4; \
    inst v14, f1, v1; \
  )

#define TEST_W_FP_VF_OP_RV_NEGRESULT( testnum, inst, finst, flags, val1, val2 ) \
  TEST_CASE_W_FP( testnum, v14, flags, val1, val2,     \
    fld f0, 0(a0); \
    fld f1, 8(a0); \
    fld f4, 8(a0); \
    vfmv.s.f v1, f0; \
    fcvt.d.s f0, f0; \
    fcvt.d.s f4, f4; \
    finst f2, f0, f4; \
    fneg.d f2, f2; \
    inst v14, f1, v1; \
  )


// For Widen-Floating instruction that order of oprands is 'vd(2*SEW), vs2(SEW), vs1(2*SEW)'
#define TEST_W_FP_WV_OP_DS( testnum, inst, finst, flags, val1, val2 ) \
  TEST_CASE_WVWF_FP( testnum, v14, flags, val1, val2,  \
    fld f0, 0(a0); \
    fld f1, 8(a0); \
    fld f4, 8(a0); \
    VSET_DOUBLE_VSEW \
    vfmv.s.f v1, f0; \
    VSET_VSEW \
    vfmv.s.f v2, f1; \
    fcvt.d.s f4, f4; \
    finst f2, f0, f4; \
    inst v14, v2, v1; \
  )







#define TEST_VMRL_OP( testnum, inst, sew, result, src1_addr, src2_addr ) \
  TEST_CASE_MASK_4VL( testnum, v14, result, \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    MK_VLE_INST(sew) v5, (x1); \
    la  x1, src2_addr; \
    MK_VLE_INST(sew) v6, (x1); \
    vmseq.vi v1, v5, 1; \
    vmseq.vi v2, v6, 1; \
    inst v14, v1, v2; \
    VSET_VSEW \
  )

#define TEST_VSFMB_OP( testnum, inst, result, src1_addr ) \
  TEST_CASE_MASK_4VL( testnum, v14, result, \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    vle64.v v5, (x1); \
    vmseq.vi v1, v5, 1; \
    inst v14, v1; \
    VSET_VSEW \
  )

#define TEST_VSFMB_OP_64( testnum, inst, result, src1_addr ) \
  TEST_CASE_MASK_4VL( testnum, v14, result, \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    vle64.v v5, (x1); \
    vmseq.vi v1, v5, 1; \
    inst v14, v1; \
    VSET_VSEW \
  )


#define TEST_VID_OP( testnum, inst, result_addr, src1_addr ) \
  TEST_CASE_LOOP( testnum, v16, result_addr, \
    VSET_VSEW_4AVL \
    la  x1, src1_addr; \
    la  x7, result_addr; \
    vle64.v v8, (x1); \
    vmseq.vi v0, v8, 1; \
    inst v16, v0.t; \
  )




#define TEST_VPOPC_OP_64( testnum, inst, result, vm_addr ) \
    VSET_VSEW_4AVL \
    la  x2, vm_addr; \
    vle64.v v14, (x2); \
    li x7, result; \
    li TESTNUM, testnum; \
    inst x14, v14; \
    VSET_VSEW \
    VECTOR_RVTEST_SIGUPD(x20, testreg);

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
    fld f7, 0(a0); \
    vfmv.s.f v14, f7; \
    vfmv.f.s f8, v14; \
    fcvt.w.s x8, f8; \
    fcvt.w.s x7, f7; \
    RVTEST_SIGUPD(x20, x8);

#define TEST_VFMVF_OP( testnum, base ) \
    li TESTNUM, testnum; \
    la a0, base; \
    fld f7, 0(a0); \
    vfmv.v.f v14, f7; \
    vfmv.f.s f8, v14; \
    fcvt.w.s x8, f8; \
    fcvt.w.s x7, f7; \
    RVTEST_SIGUPD(x20, x8);




//-----------------------------------------------------------------------
// Pass and fail code (assumes test num is in TESTNUM)
//-----------------------------------------------------------------------



//-----------------------------------------------------------------------
// Test data section
//-----------------------------------------------------------------------

#define TEST_DATA

#endif
