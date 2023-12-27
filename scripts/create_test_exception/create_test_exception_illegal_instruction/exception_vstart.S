#----------------------------------------------------------------------------- 
    #-----------------------------------------------------------------------------
    #
    # Test reduction instruction,vcpop.m,vfirst,vmsbf,vmsif,vmsof,viota,vcompress when vstart is not zero.
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
    li a7,7;
    vsetivli x31, 1, e8, m2, ta, ma;
    # set vstart to non-zero
    li t0,2;
    csrw vstart,t0;
    # illegal instructions
    vredand.vs	v24,v16,v8;
    vcpop.m	a4,v24
    vfirst.m	a4,v14
    vmsbf.m	v14,v1
    vmsif.m	v14,v1
    vmsof.m	v14,v1
    viota.m	v14,v0
    vcompress.vm	v16,v8,v0
# should not reach here
    call other_exception;



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
    

