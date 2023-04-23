#----------------------------------------------------------------------------- 
    #-----------------------------------------------------------------------------
    #
    # Test lmul mismatch with vs register.
    #

    #include "model_test.h"
    #include "arch_test.h"
    #include "riscv_test.h"
    #include "test_macros_vector.h"

RVTEST_ISA("RV64RV64IMAFDCVZicsr")
    
    .section .text.init
    .globl rvtest_entry_point
    rvtest_entry_point:
    
    
    RVTEST_CASE(0,"//check ISA:=regex(.*64.*);check ISA:=regex(.*V.*);def TEST_CASE_1=True;",vadd)
    
    RVTEST_RV64UV
    RVMODEL_BOOT
    RVTEST_CODE_BEGIN
    RVTEST_VSET
# begin test here-----------------------------------------------------------------------------------
    li a0,59285;
    li a7,67
    vsetivli x31, 1, e32, m2, tu, mu;
    li	t2,1;
    vmv.v.x	v1,t2;
    vmv.v.x	v3,t2;
    vmv.v.x	v5,t2;
    vmv.v.x	v7,t2;
    vmv.v.x	v9,t2;
    vmv.v.x	v11,t2;
    vmv.v.x	v13,t2;
    vmv.v.x	v15,t2;
    vmv.v.x	v17,t2;
    vmv.v.x	v19,t2;
    vmv.v.x	v21,t2;
    vmv.v.x	v23,t2;
    vmv.v.x	v25,t2;
    vmv.v.x	v27,t2;
    vmv.v.x	v29,t2;
    vmv.v.x	v31,t2;
    vsetivli x31, 1, e32, m4, tu, mu;
    li	t2,1;
    vmv.v.x	v1,t2;
    vmv.v.x	v2,t2;
    vmv.v.x	v3,t2;
    vmv.v.x	v5,t2;
    vmv.v.x	v6,t2;
    vmv.v.x	v7,t2;
    vmv.v.x	v9,t2;
    vmv.v.x	v10,t2;
    vmv.v.x	v11,t2;
    vmv.v.x	v13,t2;
    vmv.v.x	v14,t2;
    vmv.v.x	v15,t2;
    vmv.v.x	v17,t2;
    vmv.v.x	v18,t2;
    vmv.v.x	v19,t2;
    vmv.v.x	v21,t2;
    vmv.v.x	v22,t2;
    vmv.v.x	v23,t2;
    vmv.v.x	v25,t2;
    vmv.v.x	v26,t2;
    vmv.v.x	v27,t2;
    vmv.v.x	v29,t2;
    vmv.v.x	v30,t2;
    vmv.v.x	v31,t2;
    vsetivli x31, 1, e32, m8, tu, mu;
    li	t2,1;
    vmv.v.x	v1,t2;
    vmv.v.x	v2,t2;
    vmv.v.x	v3,t2;
    vmv.v.x	v4,t2;
    vmv.v.x	v5,t2;
    vmv.v.x	v6,t2;
    vmv.v.x	v7,t2;
    vmv.v.x	v9,t2;
    vmv.v.x	v10,t2;
    vmv.v.x	v11,t2;
    vmv.v.x	v12,t2;
    vmv.v.x	v13,t2;
    vmv.v.x	v14,t2;
    vmv.v.x	v15,t2;
    vmv.v.x	v17,t2;
    vmv.v.x	v18,t2;
    vmv.v.x	v19,t2;
    vmv.v.x	v20,t2;
    vmv.v.x	v21,t2;
    vmv.v.x	v22,t2;
    vmv.v.x	v23,t2;
    vmv.v.x	v25,t2;
    vmv.v.x	v26,t2;
    vmv.v.x	v27,t2;
    vmv.v.x	v28,t2;
    vmv.v.x	v29,t2;
    vmv.v.x	v30,t2;
    vmv.v.x	v31,t2;
    
    


# end test here-------------------------------------------------------------------------------------
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)
    TEST_PASSFAIL

handle_illegal_instruction:                                                 
    li t0,59285;        
    beq x0,a7,pass_test;
    addi a7,a7,-1;
    csrr t2,mepc;
    addi t2,t2,4;
    csrw mepc,t2;
    mret    
pass_test:                                             
    beq a0,t0,pass;   
    call other_exception;  

handle_misaligned_load_store:
    call other_exception;

handle_misaligned_fetch:
    call other_exception;
    
handle_page_fault:
    call other_exception;

handle_access:
    call other_exception;
    RVTEST_CODE_END

    RVMODEL_HALT
    
    .data
    RVTEST_DATA_BEGIN
    
    TEST_DATA
 

    signature_x12_0:
        .fill 0,4,0xdeadbeef
    
    
    signature_x12_1:
        .fill 32,4,0xdeadbeef
    
    
    signature_x20_0:
        .fill 512,4,0xdeadbeef
    
    
    signature_x20_1:
        .fill 512,4,0xdeadbeef
    
    
    signature_x20_2:
        .fill 376,4,0xdeadbeef
    
    #ifdef rvtest_mtrap_routine
    
    mtrap_sigptr:
        .fill 128,4,0xdeadbeef
    
    #endif
    
    #ifdef rvtest_gpr_save
    
    gpr_save:
        .fill 32*(XLEN/32),4,0xdeadbeef
    
    #endif
    
    RVTEST_DATA_END
    

