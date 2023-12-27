#----------------------------------------------------------------------------- 
    #-----------------------------------------------------------------------------
    #
    # test set vill and excute vector instruction
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
    li a7,4; 
    # sew=1xx is reserved now 
    li a3,4;
    li a4,0x38;
    vsetvl x31, a3,a4;
    vadd.vv	v24,v16,v6;
    li a3,4;
    li a4,0x20;
    vsetvl x31, a3,a4;
    vadd.vv	v24,v16,v6;
    li a3,4;
    li a4,0x28;
    vsetvl x31, a3,a4;
    vadd.vv	v24,v16,v6;
    li a3,4;
    li a4,0x30;
    vsetvl x31, a3,a4;
    vadd.vv	v24,v16,v6;
    # lmul=100 is reserved now
    li a3,4;
    li a4,0x4;
    vsetvl x31, a3,a4;
    vadd.vv	v24,v16,v6;



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
    

