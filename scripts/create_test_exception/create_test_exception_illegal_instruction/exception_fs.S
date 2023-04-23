#----------------------------------------------------------------------------- 
    #-----------------------------------------------------------------------------
    #
    # test when mstatus.FS or vsstatus.FS is closed, whether vfadd can raise exception
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
    csrr a2,misa;
    andi a2,a2,128;
    beq x0,a2,no_hyper;
    li a3,0xab
    # close FS in vsstatus
    li t5,24576
    csrrc a7, vsstatus,t5
    li a1,0x8000000800;
    csrrs a1,mstatus,a1;
    auipc a2, 0;
    addi a2,a2,16;
    csrw mepc,a2;
    mret;
    nop;
    vfadd.vf v24, v8, f1
    li t5,24576
    csrrs x0, vsstatus,t5
no_hyper:
    li a0,59285
    # close FS in mstatus
    li t0,24576
    csrrc x0, mstatus,t0
    vfadd.vf v24, v8, f1
# end test here-------------------------------------------------------------------------------------
    TEST_VV_OP_NOUSE(32766, vadd.vv, 2, 1, 1)
    TEST_PASSFAIL

handle_illegal_instruction: 
    li t0,0xab;
    bne t0,a3,handle_no_hyper;    
    li a3,0
    csrr t2,mepc;
    addi t2,t2,4;
    csrw mepc,t2;
    li a1,0x000001800;
    csrrs a1,mstatus,a1;
    mret
handle_no_hyper:                                            
    li t0,59285;                                                 
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
    

